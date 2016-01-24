from django.contrib import admin

# Register your models here.

from .models import ProductCatalog, Product

admin.site.register(ProductCatalog)

admin.site.register(Product)