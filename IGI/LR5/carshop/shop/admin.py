from django.contrib import admin
from django.urls import path
from .models import News, CompanyInfo, FAQ, Client

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