from django.shortcuts import render

from config import serverlistp,SERVERS_TEMPLATE,PC_STYLE_COLOR
from models import ProductCatalog
from main.config import SERVERS_QQ1, SERVERS_QQ1_NAME, SERVERS_QQ2,SERVERS_QQ2_NAME
# Create your views here.

def get_base_content():
    web_content= {
                 'pc_style_color':PC_STYLE_COLOR,
                 'servers_template':SERVERS_TEMPLATE,
                 'qq1':SERVERS_QQ1,
                 'qq1name':SERVERS_QQ1_NAME,
                 'qq2':SERVERS_QQ2,
                 'qq2name':SERVERS_QQ2_NAME
            }
    if serverlistp =='right':
        web_content['servers_serverlistpcss']='left'
        web_content['servers_float'] = 'right:0;'
        web_content['servers_float1'] = 'left:-160px;'
    elif serverlistp =='left':
        web_content['servers_serverlistpcss']='right'
        web_content['servers_float'] = 'left:0;'
        web_content['servers_float1'] = 'right:-160px;'
    else:
        web_content['_serverlistpcss']='left'
        
    return web_content
def index(request):
    catalogs = ProductCatalog.objects.order_by('show_from')
    web_content = get_base_content()
    web_content['catalogs']=catalogs
    
    return render(request, 'main/index.html', web_content)
