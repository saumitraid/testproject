from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class CustomUser(AbstractUser):

    mobile = models.CharField(
        max_length=12,
        blank=True,
        null=True
    )

    is_email_verified = models.BooleanField(
        default=False
    )

    def __str__(self):
        return self.first_name + " " + self.last_name
    
class Category(models.Model):
    category_name=models.CharField(max_length=255, unique=True, verbose_name="Name of Category")
    about=models.CharField(max_length=200)

    def __str__(self):
        return self.category_name

class Clothes(models.Model):
    category=models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )
    name=models.CharField(max_length=255)
    brand=models.CharField(max_length=255)
    size=models.CharField(max_length=10,choices=[
        ('XS', 'Extra Smsll'),
        ('S','Small'),
        ('M','Medium'),
        ('L','Large'),
        ('XL','Extra Large'),
        ('XXL','Double Extra Large')
    ])
    color=models.CharField(max_length=50)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    stock=models.PositiveIntegerField()
    description=models.TextField()
    image=models.ImageField(upload_to='clothes/')
    is_available=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class CartItem(models.Model):
    product=models.ForeignKey(Clothes, on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=0)
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.name}x{self.quantity}'


class Order(models.Model):
    product = models.ForeignKey(Clothes, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    payment_status=models.CharField(max_length=255)
    payment_id=models.CharField(max_length=255)
    address=models.TextField()