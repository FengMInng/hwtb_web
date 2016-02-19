from django.shortcuts import render

from models import ProductCatalog
# Create your views here.

def get_base_content():
    web_content={
                 'pc_style_color':1,
                 'servers_template':'main/servers_metro_color.html'
                 }
    return web_content
def index(request):
    catalogs = ProductCatalog.objects.order_by('show_from')
    web_content = get_base_content()
    web_content['catalogs']=catalogs
    
    return render(request, 'main/index.html', web_content)
