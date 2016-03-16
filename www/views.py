# -*- coding: utf-8 -*- 
from django.shortcuts import render
from django.utils import timezone

from config import Online_servers,PC_STYLE_COLOR, BMap
from models import ProductCatalog, Product
from www.config import SITE_URL
from www.models import News
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
    
    return render(request, 'www/index.html', web_content)

def catalog(request):
    web_content = get_base_content()
    
def aboutus(request):
    web_content = get_base_content()
    return render(request, 'www/aboutus.html', web_content)

def introduction(request):
    web_content = get_base_content()
    return render(request, 'www/introduction.html', web_content)

def calture(request):
    web_content = get_base_content()
    return render(request, 'www/calture.html', web_content)

def carriar(request):
    web_content = get_base_content()
    return render(request, 'www/carriar.html', web_content)

def contactus(request):
    web_content = get_base_content()
    return render(request, 'www/contactus.html', web_content)

def news(request):
    web_content = get_base_content()
    news_list = News.objects.order_by('new_type')
    return render(request, 'www/news.html', web_content)
