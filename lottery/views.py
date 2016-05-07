from django.shortcuts import render
from lottery.models import Guess
from tasks import guess

# Create your views here.


def view_lot_default(request):
    web_content={}
    type = request.GET.get('type') or 'dlt'
    web_content['lots']=guess(type)
    return render(request, 'lottery/view.html', web_content)

def view_lot_hist(request):
    type = request.GET.get('type') or 'dlt'
    web_content={}
    web_content['type']=type
    web_content['lots']=Guess.objects.filter(type=type).order_by('-create_time')
    return render(request, 'lottery/view.html', web_content)