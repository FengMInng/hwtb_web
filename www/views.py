# -*- coding: utf-8 -*- 
from django.shortcuts import render, get_object_or_404
from django.utils import timezone

from config import Online_servers,PC_STYLE_COLOR, BMap
from models import ProductCatalog, Product
from www.config import SITE_URL
from www.models import News, Job
# Create your views here.

def get_base_content():
    web_content= {
                 'site_url':SITE_URL,
                 'pc_style_color':PC_STYLE_COLOR,
                 'online_servers':Online_servers(),
                 'bmap': BMap()
            }
        
    return web_content

def get_product_catalogs_all():
    return ProductCatalog.objects.filter(show_start__lte = timezone.now(),
                                    show_end__gte = timezone.now()).order_by('show_start')
    
def get_product_all():
    return Product.objects.filter(show_start__lte = timezone.now(),
                                    show_end__gte = timezone.now()).order_by('show_start')
    
def index(request):
    web_content = get_base_content()
    web_content['catalogs']=get_product_catalogs_all()
    web_content['products']=get_product_all()
    
    return render(request, 'www/index.html', web_content)

def catalog(request):
    web_content = get_base_content()
    web_content['catalogs']=get_product_catalogs_all()
    web_content['products']=get_product_all()
    
    return render(request, 'www/catalog.html', web_content)

def catalog_list(request, catalog_id):
    web_content = get_base_content()
    
    catalog= get_object_or_404(ProductCatalog, catalog_id)
    products = Product.objects.filter(catalog_id=catalog.id,
                                    show_start__lte = timezone.now(),
                                    show_end__gte = timezone.now())
    web_content['products'] = products
    return render(request, 'www/catalog_list.html', web_content)

def product(request, product_id):
    web_content = get_base_content()
    
    return render(request, 'www/product.html', web_content)

def aboutus(request):
    web_content = get_base_content()
    jobs = Job.objects.filter(pub_date__lt=timezone.now(),
                            end_date__gt=timezone.now())[:5]
    
    web_content['jobs']=jobs
    return render(request, 'www/aboutus.html', web_content)

def introduction(request):
    web_content = get_base_content()
    return render(request, 'www/introduction.html', web_content)

def calture(request):
    web_content = get_base_content()
    return render(request, 'www/calture.html', web_content)

def carriar(request):
    web_content = get_base_content()
    jobs = Job.objects.filter(pub_date__lt=timezone.now(),
                            end_data__gt=timezone.now())
    web_content['jobs']=jobs
    return render(request, 'www/carriar.html', web_content)

def job_detail(request, job_id):
    web_content = get_base_content()
    job = get_object_or_404(Job, job_id)
    web_content['job']=job
    return render(request, 'www/job.html', web_content)

def contactus(request):
    web_content = get_base_content()
    return render(request, 'www/contactus.html', web_content)

def news(request):
    web_content = get_base_content()
    news_list = News.objects.order_by('new_type')
    web_content['news']=news_list
    return render(request, 'www/news.html', web_content)
