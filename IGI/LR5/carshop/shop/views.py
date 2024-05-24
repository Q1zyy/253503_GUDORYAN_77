from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
import json
import requests
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CompanyInfo, News, FAQ, Detail, Supplier, SupplierDetail, Order, Store, Promocode, Location, StoreOrder, Review, Employee, Job
from django.views.generic import FormView
from .forms import RegisterForm
from .models import Client
from django.db.models import Sum, Count
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
import logging
from django.utils import timezone
import calendar
import tzlocal
import datetime
import pytz
from datetime import datetime
from django.db.models import Avg, Min, Max
import matplotlib.pyplot as plt
import os
from django.conf import settings

logger = logging.getLogger('shop')

def index(request):
    logger.info('index')
    response = requests.get('https://catfact.ninja/fact')
    if response.status_code == 200:
        cat_fact = response.json()
    response = requests.get('https://dog.ceo/api/breeds/image/random')
    if response.status_code == 200:
        dog_photo = response.json()
        
    latest_news = News.objects.order_by('-id').first()
        
    tz = tzlocal.get_localzone()
    local_time = datetime.now(tz)
    now_time = datetime.now(tz)
    utc_time = datetime.now(tz=pytz.timezone('UTC'))
    text_cal = calendar.month(local_time.year, local_time.month)
    
    context = {
        'latest_news': latest_news,
        'cat_fact': cat_fact,
        'dog_image': dog_photo,
        'user_timezone': tz,
        'current_date_formatted': now_time.strftime("%m-%d-%Y %H:%M:%S %Z"),
        'calendar_text': text_cal,
        'utc_time': utc_time.strftime("%m-%d-%Y %H:%M:%S %Z"),
    }
    
    return render(request, 'index.html', context)

def about(request): 
    logger.info('about')
    info = CompanyInfo.objects.first()
    return render(request, 'about.html', {'info': info})

def news(request):
    logger.info('news')
    news_list = News.objects.all()
    return render(request, 'news.html', {'news': news_list})

def faq(request):
    logger.info('faq')
    faq_list = FAQ.objects.all()
    return render(request, 'faq.html', {'faq': faq_list})

@login_required
def profile(request):
    logger.info('profile')
    store_orders = request.user.store_orders.all()
    context = {
        'store_orders': store_orders
    }
    return render(request, 'profile.html', context)


@login_required
@permission_required('shop.employee', raise_exception=False)
def supplier_list(request):
    logger.info('supplier_list')
    suppliers = Supplier.objects.all()
    supplier_detail = SupplierDetail.objects.select_related('supplier', 'detail')
    
    if request.method == 'POST':
        supplier_detail_id = request.POST.get('supplier_detail_id')
        quantity = int(request.POST.get('quantity'))
        supplier_detail = SupplierDetail.objects.get(id=supplier_detail_id)

        if quantity > 0 and quantity <= supplier_detail.quantity:
            total_price = quantity * supplier_detail.price
            order = Order.objects.create(
                user=request.user,
                supplier_detail=supplier_detail,
                quantity=quantity,
                total_price=total_price
            )
            print(quantity, supplier_detail.price)
            store_item, created = Store.objects.get_or_create(
                detail=supplier_detail.detail,
                price=0,
                defaults={'quantity': 0}
            )
            store_item.quantity += quantity
            store_item.save()
            
            supplier_detail.quantity -= quantity
            supplier_detail.save()
            return redirect('supplier_list')
    
    context = {
        'suppliers': suppliers,
        'supplier_details': supplier_detail
    }
    return render(request, 'supplier_list.html', context)

class RegisterView(FormView):
    model = User
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = '/'

    def form_valid(self, form):
        user = form.save()

        dob = form.cleaned_data.get('date_of_birth')
        phone = form.cleaned_data.get('phone_number')
        fn = form.cleaned_data.get('first_name')
        ln = form.cleaned_data.get('last_name')
        
        client = Client(user=user, first_name=fn, last_name=ln, date_of_birth=dob, phone_number=phone)
        client.save()

        return super().form_valid(form)

@login_required
@permission_required('shop.employee', raise_exception=False)
def orders_supplier(request):
    orders = Order.objects.filter(user__is_superuser=True)
    context = {
        'orders': orders
    }
    return render(request, 'orders_supplier.html', context)     

def store_view(request):
    min_price = request.GET.get('min_price', None)
    max_price = request.GET.get('max_price', None)
    sort = request.GET.get('sort', None)

    store_items = Store.objects.all()

    if min_price:
        store_items = store_items.filter(price__gte=min_price)
    if max_price:
        store_items = store_items.filter(price__lte=max_price)

    if sort == 'quantity':
        store_items = store_items.order_by('quantity')
    elif sort == 'price':
        store_items = store_items.order_by('price')

    context = {
        'store_items': store_items,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'store.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')

def promocodes(request):
    
    promos = Promocode.objects.all()
    
    context = {
        'promos': promos
    }
    
    return render(request, 'promocodes.html', context)

@login_required
def purchase_view(request):
    locations = Location.objects.all()
    promocodes = Promocode.objects.all()
    store_items = Store.objects.all()

    if request.method == 'POST':
        location_id = request.POST.get('location')
        promocode_id = request.POST.get('promocode')
        items = request.POST.getlist('items[]')
        quantities = [int(q) for q in request.POST.getlist('quantities[]')]

        location = Location.objects.get(id=location_id)
        promocode = Promocode.objects.get(id=promocode_id) if promocode_id else None

        total_price = 0
        quantity = 0
        for i, item_id in enumerate(items):
            item = Store.objects.get(id=item_id)
            total_price += item.price * quantities[i]
            if items[i]:
                quantity += 1

        if promocode:
            total_price *= (1 - promocode.discount / 100)

        store_order = StoreOrder.objects.create(
            user=request.user,
            quantity=quantity,
            location=location,
            promo=promocode,
            total_price=total_price
        )

        for i, item_id in enumerate(items):
            item = Store.objects.get(id=item_id)
            item.quantity -= quantities[i]
            item.save()

        store_order.save()

        return redirect('profile')

    context = {
        'locations': locations,
        'promocodes': promocodes,
        'store_items': store_items
    }
    return render(request, 'purchase.html', context)

@login_required
@permission_required('shop.employee', raise_exception=False)
def all_orders(request):
    store_orders = StoreOrder.objects.all()
    context = {
        'store_orders': store_orders
    }
    return render(request, 'all_orders.html', context)


@login_required
def review_create(request):
    if request.method == 'POST':
        rating = int(request.POST['rating'])
        review_text = request.POST['review_text']
        review = Review.objects.create(
            user=request.user,
            rating=rating,
            text=review_text,
        )
        review.save()
        return redirect('reviews')
    else:
        ratings = range(1, 6)
        return render(request, 'review_create.html', {'ratings': ratings})
    
def review_list(request):
    reviews = Review.objects.all()
    return render(request, 'reviews.html', {'reviews': reviews})

@login_required
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if review.user == request.user:
        review.delete()
    return redirect('reviews')

@login_required
def review_update(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if review.user == request.user:
        if request.method == 'POST':
            review.rating = request.POST['rating']
            review.text = request.POST['review_text']
            review.save()
            return redirect('reviews')
        else:
            ratings = range(1, 6)
            return render(request, 'review_update.html', {'review': review, 'ratings': ratings})
    else:
        return redirect('reviews')
    
def employee_list(request):
    employees = Employee.objects.all()
    return render(request, 'employee_list.html', {'employees': employees})

def job_list_view(request):
    jobs = Job.objects.all().order_by('title')
    context = {
        'jobs': jobs
    }
    return render(request, 'job_list.html', context)


def stats(request):
    user_orders_stats = (
        StoreOrder.objects.values('user__username')
        .annotate(
            total_quantity=Sum('quantity'),
            total_spent=Sum('total_price')
        )
        .order_by('-total_spent')
    )
    
    average_order_price = StoreOrder.objects.aggregate(Avg('total_price'))['total_price__avg']
    min_order_price = StoreOrder.objects.aggregate(min_price=Min('total_price'))['min_price']
    max_order_price = StoreOrder.objects.aggregate(max_price=Max('total_price'))['max_price']
    
        
    price_ranges = [
        (0, 10),
        (10, 20),
        (20, 30),
        (30, 50),
        (50, 100),
        (100, 1000)
    ]

    orders_by_price_range = []
    for min_price, max_price in price_ranges:
        count = StoreOrder.objects.filter(total_price__gte=min_price, total_price__lt=max_price).count()
        orders_by_price_range.append({
            'range': f'{min_price} - {max_price if max_price != float("inf") else "∞"}',
            'count': count
        })

    x = [order['range'] for order in orders_by_price_range]
    y = [order['count'] for order in orders_by_price_range]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(x, y)
    ax.set_xlabel('Ценовой диапазон')
    ax.set_ylabel('Количество заказов')
    ax.set_title('Статистика заказов по ценовым диапазонам')
    plt.xticks(rotation=90)

    graph_path = os.path.join(settings.MEDIA_ROOT, 'orders_by_price_range.png')
    plt.savefig(graph_path)


    context = {
        'user_orders_stats': user_orders_stats,
        'average_order_price': average_order_price,
        'min_order_price': min_order_price,
        'max_order_price': max_order_price,
        'plot_url': os.path.join(settings.MEDIA_URL, 'orders_by_price_range.png')
    }
    return render(request, 'stats.html', context)