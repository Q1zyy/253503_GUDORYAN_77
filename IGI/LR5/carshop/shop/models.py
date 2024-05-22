from django.db import models
from django.contrib.auth.models import User, Group

class News(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='articles/')
    
class CompanyInfo(models.Model):
    text = models.TextField()

class FAQ(models.Model):
    question = models.TextField()
    answer = models.TextField()
    date_added = models.DateField(auto_now_add=True)
    
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=2)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True) 
    phone_number = models.CharField(max_length=20, default='', blank=True) 

    def __str__(self):
        return f"{self.user.username}"

    class Meta:
        ordering = ["last_name", "first_name"]

    def save(self, *args, **kwargs):
        Group.objects.get_or_create(name='Clients')
        super().save(*args, **kwargs)
        group = Group.objects.get(name='Clients')
        self.user.groups.add(group)