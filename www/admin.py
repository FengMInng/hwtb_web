# -*- coding: utf-8 -*- 
from django.contrib import admin

# Register your models here.

from .models import ProductCatalog, ProductCatalogAdmin, Product, ProductAdmin
from main.models import News, Solution

admin.site.register(ProductCatalog, ProductCatalogAdmin)

admin.site.register(Product,ProductAdmin)

admin.site.register(News)

admin.site.register(Solution)