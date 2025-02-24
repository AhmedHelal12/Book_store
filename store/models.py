from django.db import models
from django.contrib.sessions.models import Session
from book_store import settings
from checkout.models import Transaction

class Category(models.Model):
    name = models.CharField(max_length=255)
    featured = models.BooleanField(default=False)
    order = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    short_description = models.CharField(max_length=255)
    pdf_file = models.FileField(null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Author,on_delete=models.SET_NULL,null=True)
    category = models.ForeignKey(Category,on_delete=models.PROTECT)
    price = models.FloatField()
    image = models.ImageField()
    featured = models.BooleanField(default=False)

    @property
    def pdf_url(self):
        return settings.SITE_URL+ self.pdf_file.url
    
    def __str__(self):
        return self.name


class Cart(models.Model):
    cart_items = models.JSONField(default=dict)
    session = models.ForeignKey(Session,on_delete=models.CASCADE)

    
class Order(models.Model):
    transaction = models.OneToOneField(Transaction,on_delete=models.PROTECT,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.id)

class OrderProduct(models.Model):
    order = models.ForeignKey(Order,on_delete=models.PROTECT)
    product = models.ForeignKey(Product,on_delete=models.PROTECT,null=True)
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

class Slider(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.TextField(max_length=500)
    image = models.ImageField(null=True)
    order = models.IntegerField(default=1)

    def __str__(self):
        return self.title
    