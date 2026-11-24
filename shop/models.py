from django.db import models
from django.contrib.auth.models import User
import os
import shutil
from django.conf import settings


# Product Model #
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('products', 'Products'),
        ('services', 'Services'),
        ('time_services', 'Time Services')]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    youtube_link = models.CharField(max_length=200, null=True, blank=True)
    short_desc = models.TextField()
    long_desc = models.TextField(null=True, blank=True)
    discount = models.IntegerField(default=0)
    stock = models.IntegerField(null=True, blank=True, help_text="Only for products category")
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        try:
            images_folder = os.path.join(settings.MEDIA_ROOT, "product_images", str(self.id))
            if os.path.exists(images_folder):
                shutil.rmtree(images_folder)
        except Exception:
            ...
        super().delete(*args, **kwargs)


# Function generates product image path #
def generate_image_path(instance, filename):
    return os.path.join("product_images", str(instance.product.id), filename)


# Product Image Model #
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=generate_image_path)


# Order Model #
class Order(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('finished', 'Finished'),
        ('cancelled', 'Cancelled')]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    address_1 = models.CharField(max_length=50)
    address_2 = models.CharField(max_length=50, null=True, blank=True)
    zip_code = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="in_progress")


# Order Item Model (ORDER-PRODUCT N:M table) #
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    price_at_order_time = models.DecimalField(max_digits=10, decimal_places=2)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.product.name if self.product else "DELIVERY"


# Delivery Cost Model #
class DeliveryCost(models.Model):
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return "Delivery cost"