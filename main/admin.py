# -*- coding: utf-8 -*- 
from django.contrib import admin

# Register your models here.

from .models import ProductCatalog, ProductCatalogAdmin, Product

admin.site.register(ProductCatalog, ProductCatalogAdmin)

admin.site.register(Product)