from django.shortcuts import render

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
    catalogs = ProductCatalog.objects.order_by('show_from')
    web_content = get_base_content()
    web_content['catalogs']=catalogs
    products = Product.objects.order_by('catalog')
    web_content['products']=products
    
    return render(request, 'main/index.html', web_content)
