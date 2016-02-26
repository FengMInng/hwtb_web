# -*- coding: utf-8 -*- 
from django.shortcuts import render
from django.utils import timezone

from config import Online_servers,PC_STYLE_COLOR, BMap
from models import ProductCatalog, Product
from main.config import SITE_URL
# Create your views here.

def get_base_content():
    web_content= {
                 'site_url':SITE_URL,
                 'pc_style_color':PC_STYLE_COLOR,
                 'online_servers':Online_servers(),
                 'bmap': BMap()
            }
        
    return web_content
def index(request):
    catalogs = ProductCatalog.objects.filter(
                show_start__lte = timezone.now(),
                show_end__gte = timezone.now()
                ).order_by('show_start')
    web_content = get_base_content()
    web_content['catalogs']=catalogs
    products = Product.objects.order_by('catalog')
    web_content['products']=products
    
    return render(request, 'main/index.html', web_content)

def catalog(request):
    web_content = get_base_content()