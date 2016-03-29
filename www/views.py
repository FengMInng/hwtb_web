# -*- coding: utf-8 -*- 
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from config import PC_STYLE_COLOR
from models import ProductCatalog, Product
from www.config import SITE_URL
from www.models import News, Job, Roll, OnlineService, Description
from django.http.response import HttpResponseRedirect
# Create your views here.

def get_roll():
    return Roll.objects.all().order_by('-create_date')[:3]

def get_base_content():
    web_content= {
                 'site_url':SITE_URL,
                 'pc_style_color':PC_STYLE_COLOR,
                 'online_servers':Online_servers(),
            }
        
    return web_content

def get_product_catalogs_all():
    return ProductCatalog.objects.filter(show_start__lte = timezone.now(),
                                    show_end__gte = timezone.now()).order_by('show_start')
    
def get_product_all():
    return Product.objects.filter(show_start__lte = timezone.now(),
                                    show_end__gte = timezone.now()).order_by('show_start')

def get_online_service_qqlist():
    return OnlineService.objects.filter(type = 'QQ')

#online servers for view
class Online_servers:
    def __init__(self):
        self.qqlist = get_online_service_qqlist()
        self.weixin= OnlineService.objects.filter(type = 'weixin')
        self.wangwang=OnlineService.objects.filter(type = 'wangwang')
        #self.ali=""
        self.tel = OnlineService.objects.filter(type = 'tel')

def index(request):
    web_content = get_base_content()
    web_content['rolls'] = get_roll()
    web_content['catalogs']=get_product_catalogs_all()
    web_content['products']=get_product_all()
    web_content['news_summurys']=News.objects.all().order_by('-create_date')[0:3]
    
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
    news_list = News.objects.order_by('type')
    web_content['news']=news_list
    return render(request, 'www/news.html', web_content)

def news_detail(request, news_id):
    web_content = get_base_content()
    web_content['news']=get_object_or_404(News, pk=news_id)
    return render(request, 'www/news_detail.html', web_content)

@csrf_exempt
def upload(request):
    print request
    if request.method == 'POST':
        img = Description(title=request.FILES['upload'].name,\
                          img=request.FILES['upload'])
        img.save()
        pass
    
    return HttpResponseRedirect(img.img.url)