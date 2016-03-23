# -*- coding: utf-8 -*- 
from django.contrib import admin

# Register your models here.

from .models import ProductCatalog, ProductCatalogAdmin, Product, ProductAdmin
from .models import News, Solution, Description, Roll

admin.site.register(Roll)

admin.site.register(ProductCatalog, ProductCatalogAdmin)

admin.site.register(Product,ProductAdmin)

admin.site.register(Description)

admin.site.register(News)

admin.site.register(Solution)