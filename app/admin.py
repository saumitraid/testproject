from django.contrib import admin
from . models import CustomUser, Category, Clothes, Order

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Category)
admin.site.register(Clothes)
admin.site.register(Order)