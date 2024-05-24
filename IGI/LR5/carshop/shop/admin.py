from django.contrib import admin
from django.urls import path
from .models import News, CompanyInfo, FAQ, Client, Supplier, Detail, SupplierDetail, Order, Store, Employee
from django.contrib.auth.models import Permission


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'content')
    search_fields = ('title', 'content')
    
    
@admin.register(CompanyInfo)
class NewsAdmin(admin.ModelAdmin):
    pass

@admin.register(FAQ)
class NewsAdmin(admin.ModelAdmin):
    pass

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('user_username', 'first_name', 'last_name', 'user_email')
    search_fields = ('first_name', 'last_name', 'user_email')

    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = 'Email'

    def user_username(self, obj):
        return obj.user.username

    user_username.short_description = 'Username' 
    
@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'phone']
    search_fields = ['name']
    
    
@admin.register(Detail)
class DetailAdmin(admin.ModelAdmin):
    list_display = ['article', 'name']
    search_fields = ['article', 'name']
    
@admin.register(SupplierDetail)
class SupplierDetailAdmin(admin.ModelAdmin):
    list_display = ['supplier', 'detail', 'price', 'quantity']
    search_fields = ['supplier__name', 'detail__article', 'detail__name']
    raw_id_fields = ['supplier', 'detail']
    

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'supplier_detail', 'quantity', 'total_price', 'created_at')
    list_filter = ('user', 'supplier_detail', 'created_at')
    search_fields = ('user__username', 'supplier_detail__detail__name')
    readonly_fields = ('created_at',)

admin.site.register(Order, OrderAdmin)

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('detail', 'quantity')
    search_fields = ('detail__name',)
    list_filter = ('detail',)
    
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user_username', 'user_first_name', 'user_last_name', 'user_email')
    search_fields = ('user_username', 'user_first_name', 'user_last_name', 'user_email')
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        supplier_list, created = Permission.objects.get_or_create(
            codename='employee',
            defaults={
                'name': 'employee',
                'content_type': None 
            }
        )
        
        obj.user.user_permissions.add(supplier_list)
        print(obj.user.username, obj.user.user_permissions.all())
    
    def user_email(self, obj):
        return obj.user.email

    user_email.short_description = 'Email'

    def user_username(self, obj):
        return obj.user.username

    user_username.short_description = 'Username' 
    
    def user_first_name(self, obj):
        return obj.user.first_name

    user_first_name.short_description = 'First name' 
    
    def user_last_name(self, obj):
        return obj.user.last_name

    user_first_name.short_description = 'Last name' 