from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
import json
import requests
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CompanyInfo, News, FAQ
from django.views.generic import FormView
from .forms import RegisterForm
from .models import Client


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

class RegisterView(FormView):
    model = User
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = '/'

    def form_valid(self, form):
        user = form.save()

        dob = form.cleaned_data.get('date_of_birth')
        phone = form.cleaned_data.get('phone_number')
        
        client = Client(user=user, date_of_birth=dob, phone_number=phone)
        client.save()

        return super().form_valid(form)