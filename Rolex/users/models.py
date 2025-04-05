from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.db import models
from PIL import Image
from django.utils import timezone
from decimal import Decimal
from product.models import Watch


# Create your models here.
class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class BasketItem(models.Model):
    product = models.ForeignKey(Watch, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    added_date = models.DateTimeField(default=timezone.now)
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='images/')
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.user.username}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
            super().save(update_fields=['image'])


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    date = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=5)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='pending')
    order_number = models.CharField(max_length=50, unique=True)

    class Meta:
        get_latest_by = 'date'

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f'ORD-{timezone.now().strftime("%Y%m%d%H%M%S")}-{self.id}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number

    @property
    def tax(self):
        return self.price * Decimal('0.15')

    @property
    def shipping_cost(self):
        return self.price * Decimal('0.20')

    @property
    def total(self):
        return self.price + self.tax + self.shipping_cost



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE,related_name='orderitems')
    product = models.ForeignKey(Watch, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    @property
    def subtotal(self):
        return self.product.price * self.quantity


class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
