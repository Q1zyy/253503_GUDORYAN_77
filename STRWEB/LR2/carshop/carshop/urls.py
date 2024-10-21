"""
URL configuration for carshop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from shop import views
from django.conf import settings
from django.conf.urls.static import static
from shop.views import RegisterView
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('logout', views.logout_view, name='logout'),
    path('profile', views.profile, name='profile'),
    path('home', views.index, name='home'),
    path('about', views.about, name='about'),
    path('news', views.news, name='news'),
    path('faq', views.faq, name='faq'),
    path('register', RegisterView.as_view(), name='register'),
    path('suppliers', views.supplier_list, name='supplier_list'),
    path('store', views.store_view, name='store'),
    path('orders_supplier', views.orders_supplier, name='orders_supplier'),
    path('promocodes', views.promocodes, name='promocodes'),
    path('purchase/', views.purchase_view, name='purchase'),
    path('all_orders/', views.all_orders, name='all_orders'),
    path('review_create', views.review_create, name='review_create'),
    path('reviews/', views.review_list, name='reviews'),
    path('reviews/<int:pk>/delete/', views.review_delete, name='review_delete'),
    path('reviews/<int:pk>/update/', views.review_update, name='review_update'),
    path('employees', views.employee_list, name='employees'),
    path('jobs', views.job_list_view, name='job_list'),
    path('stats', views.stats, name='stats'),
    path("detail/<int:id>", views.detail, name='detail'),
    path('cart', views.cart, name='cart'),
    path('payment', views.payment, name='payment'),
    path('news/<int:id>', views.news_detail, name='single_news'),
    path('faq/<int:id>', views.faq_detail, name='single_faq'),
    path('privacy', views.privacy, name='privacy')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
