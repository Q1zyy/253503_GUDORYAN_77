from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
import json
import requests
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CompanyInfo, News, FAQ, Detail, Supplier, SupplierDetail, Order, Store, Promocode, Location, StoreOrder
from django.views.generic import FormView
from .forms import RegisterForm
from .models import Client
from django.db.models import Sum, Count
from django.contrib.auth.decorators import login_required, permission_required



def index(request):
    return render(request, 'index.html')

def about(request):
    info = CompanyInfo.objects.first()
    return render(request, 'about.html', {'info': info})

def news(request):
    news_list = News.objects.all()
    return render(request, 'news.html', {'news': news_list})

def faq(request):
    faq_list = FAQ.objects.all()
    return render(request, 'faq.html', {'faq': faq_list})

@login_required
def profile(request):
    return render(request, 'profile.html')


@login_required
@permission_required('shop.employee', raise_exception=False)
def supplier_list(request):
    suppliers = Supplier.objects.all()
    supplier_detail = SupplierDetail.objects.select_related('supplier', 'detail')
    
    if request.method == 'POST':
        supplier_detail_id = request.POST.get('supplier_detail_id')
        print('-------------HERE----------', supplier_detail_id)
        quantity = int(request.POST.get('quantity'))
        print('-------------BUUUUUY----------', quantity)
        supplier_detail = SupplierDetail.objects.get(id=supplier_detail_id)

        if quantity > 0 and quantity <= supplier_detail.quantity:
            total_price = quantity * supplier_detail.price
            order = Order.objects.create(
                user=request.user,
                supplier_detail=supplier_detail,
                quantity=quantity,
                total_price=total_price
            )
            
            store_item, created = Store.objects.get_or_create(
                detail=supplier_detail.detail,
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
        for i, item_id in enumerate(items):
            item = Store.objects.get(id=item_id)
            total_price += item.price * quantities[i]

        if promocode:
            total_price *= (1 - promocode.discount / 100)

        store_order = StoreOrder.objects.create(
            user=request.user,
            quantity=sum(quantities),
            location=location,
            total_price=total_price
        )

        for i, item_id in enumerate(items):
            item = Store.objects.get(id=item_id)
            item.quantity -= quantities[i]
            item.save()

        store_order.save()

        return redirect('purchase_success')

    context = {
        'locations': locations,
        'promocodes': promocodes,
        'store_items': store_items
    }
    return render(request, 'purchase.html', context)