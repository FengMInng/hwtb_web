# -*- coding: utf-8 -*- 
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from django.core.paginator import Paginator, PageNotAnInteger

from config import PC_STYLE_COLOR
from models import ProductCatalog, Product
from www.config import SITE_URL
from www.models import News, Job, Roll, OnlineService, ImageStore, AboutUs,\
    FriendLink, Solution, Driver
from django.http.response import HttpResponseRedirect, HttpResponse
# Create your views here.

def get_roll():
    return Roll.objects.all().order_by('-create_date')[:3]

def get_base_content():
    web_content= {
                 'site_url':SITE_URL,
                 'pc_style_color':PC_STYLE_COLOR,
                 'online_servers':Online_servers(),
            }
    
    web_content['rolls'] = Roll.objects.all().order_by('create_date')[:3]    
    web_content['catalogs']=get_product_catalogs_all()
    web_content['products']=get_product_all()
    web_content['solutions']=get_solitions_all()
    return web_content

def get_product_catalogs_all():
    return ProductCatalog.objects.filter(show_start__lte = timezone.now(),
                                    show_end__gte = timezone.now(),
                                    is_delete = False).order_by('show_start')
    
def get_product_all():
    return Product.objects.filter(show_start__lte = timezone.now(),
                                    show_end__gte = timezone.now(),
                                    is_delete = False).order_by('show_start')

def get_promote_product():
    return Product.objects.filter(show_start__lte = timezone.now(),
                                    show_end__gte = timezone.now(),
                                    is_delete = False).order_by('-show_start')[:10]
def get_solitions_all():
    return Solution.objects.filter(show_start__lte = timezone.now(),
                                    show_end__gte = timezone.now()).order_by('-show_start')
#online servers for view
class Online_servers:
    def __init__(self):
        self.qqlist = OnlineService.objects.filter(type = 'QQ')
        self.weixin= OnlineService.objects.filter(type = 'weixin')
        self.wangwang=OnlineService.objects.filter(type = 'wangwang')
        #self.ali=""
        self.tel = OnlineService.objects.filter(type = 'tel')

def index(request):
    web_content = get_base_content()
    web_content['rolls'] = get_roll()
    
    web_content['promotions'] = get_promote_product()
    web_content['news_summurys']=News.objects.all().order_by('-create_date')[0:3]
    web_content['friendlink']=FriendLink.objects.all()
    
    return render(request, 'www/index.html', web_content)

def roll_view(request, roll_id):
    web_content = get_base_content()
    roll = get_object_or_404(Roll, pk=roll_id)
    web_content['roll'] = roll
    return render(request, 'www/roll.html', web_content)

def catalog(request):
    web_content = get_base_content()
    
    return render(request, 'www/catalog.html', web_content)

def catalog_list(request, catalog_id):
    recode_per_page=11
    curpage = 1
    if request.method == 'GET':
        curpage=request.GET.get('page')
        pass
    else:
        pass
    web_content = get_base_content()
    
    catalog= get_object_or_404(ProductCatalog, pk=catalog_id)
    products = Product.objects.filter(catalog_id=catalog.id,
                                    show_start__lte = timezone.now(),
                                    show_end__gte = timezone.now(),
                                    is_delete=False)
    web_content['show_catalog']=catalog
    
    p = Paginator(products, recode_per_page)
    try:
        web_content['show_products']=p.page(curpage)
    except PageNotAnInteger:
        web_content['show_products']=p.page(1)
    web_content['pages']=p
    return render(request, 'www/catalog_list.html', web_content)

def product(request, product_id):
    web_content = get_base_content()
    web_content['show_product']=get_object_or_404(Product, pk=product_id)
    
    return render(request, 'www/product.html', web_content)

def aboutus(request):
    web_content = get_base_content()
    jobs = Job.objects.filter(pub_date__lt=timezone.now(),
                            end_date__gt=timezone.now())[:5]
    
    web_content['jobs']=jobs
    intro=AboutUs.objects.filter(type = 'introduction')
    if intro:
        web_content['introduction'] = intro[0]
    calture = AboutUs.objects.filter(type = 'calture')
    if calture:
        web_content['calture']=calture[0]
    
    return render(request, 'www/aboutus.html', web_content)

def introduction(request):
    web_content = get_base_content()
    intro=AboutUs.objects.filter(type = 'introduction')
    if intro:
        web_content['introduction'] = intro[0]
    return render(request, 'www/introduction.html', web_content)

def calture(request):
    web_content = get_base_content()
    calture = AboutUs.objects.filter(type = 'calture')
    if calture:
        web_content['calture']=calture[0]
    return render(request, 'www/calture.html', web_content)

def carriar(request):
    recode_per_page = 10
    web_content = get_base_content()
    jobs = Job.objects.filter(pub_date__lt=timezone.now(),
                            end_date__gt=timezone.now())
    if request.method == 'GET':
        curpage=request.GET.get('page')
        pass
    else:
        pass
    p = Paginator(jobs, recode_per_page)
    try:
        web_content['jobs']=p.page(curpage)
    except PageNotAnInteger:
        web_content['jobs']=p.page(1)
    web_content['pages']=p
    return render(request, 'www/carriar.html', web_content)

def job_detail(request, job_id):
    web_content = get_base_content()
    job = get_object_or_404(Job, pk=job_id)
    web_content['job']=job
    return render(request, 'www/job.html', web_content)

def contactus(request):
    web_content = get_base_content()
    return render(request, 'www/contactus.html', web_content)

def news(request):
    recode_per_page=11
    curpage = 1
    if request.method == 'GET':
        curpage=request.GET.get('page')
        pass
    else:
        pass
    web_content = get_base_content()
    news_list = News.objects.order_by('type')
    p = Paginator(news_list, recode_per_page)
    try:
        web_content['news']=p.page(curpage)
    except PageNotAnInteger:
        web_content['news']=p.page(1)
    web_content['pages']=p
    return render(request, 'www/news.html', web_content)

def news_detail(request, news_id):
    web_content = get_base_content()
    web_content['news']=get_object_or_404(News, pk=news_id)
    return render(request, 'www/news_detail.html', web_content)

@csrf_exempt
def upload(request):
    if request.method == 'POST':
        callback = request.GET.get('CKEditorFuncNum')
        img = ImageStore(title=request.FILES['upload'].name,\
                          img=request.FILES['upload'])
        img.save()
        res = r"<script>window.parent.CKEDITOR.tools.callFunction("+callback+",'http://"+SITE_URL+img.img.url+"', '');</script>"
        return HttpResponse(res)
    return HttpResponseRedirect(img.img.url)

def browser(request, path):
    return HttpResponseRedirect(SITE_URL + path)

def service(request):
    web_content = get_base_content()
    web_content['drivers']=Driver.objects.all().order_by('create_time')
    return render(request, 'www/service.html', web_content)
    pass

def solution(request):
    web_content = get_base_content()
    return render(request, 'www/solution.html', web_content)
    pass

def solution_detail(request, so_id):
    web_content = get_base_content()
    web_content['show_solution']=get_object_or_404(Solution, pk=so_id)
    return render(request, 'www/solution_detail.html', web_content)
    pass