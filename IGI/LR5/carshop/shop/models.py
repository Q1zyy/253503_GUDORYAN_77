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

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
  
class Detail(models.Model):
    article = models.IntegerField()
    name = models.CharField(max_length=100)
    description = models.TextField()
    suppliers = models.ManyToManyField(Supplier, through='SupplierDetail', through_fields=('detail', 'supplier'))
    
class SupplierDetail(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    detail = models.ForeignKey(Detail, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    quantity = models.IntegerField()
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    supplier_detail = models.ForeignKey(SupplierDetail, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=2)
    photo = models.ImageField(upload_to='employee_photos', null=True, blank=True)
    
    class Meta:
        permissions = [
            ('employee', 'Can view suppliers list'),
        ]
    
    
class Store(models.Model):
    detail = models.ForeignKey(Detail, on_delete=models.CASCADE, related_name='store_items')
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"{self.detail.name} - {self.quantity}"


class Promocode(models.Model):
    code = models.CharField(max_length=10)
    discount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.code
    
class Location(models.Model):
    name = models.CharField(max_length=100)
    
class StoreOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='store_orders')
    quantity = models.PositiveIntegerField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='store_orders')
    promo = models.ForeignKey(Promocode, on_delete=models.CASCADE, related_name='store_orders')
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)