from django.shortcuts import render
from lottery.models import Guess

# Create your views here.

def view_lot(request, type):
    if type is None or len(type) ==0:
        type='dlt'
    web_content={}
    web_content['type']=type
    web_content['lots']=Guess.objects.filter(validno="", type=type)
    return render(request, 'lottery/view.html', web_content)

def view_lot_default(request):
    return view_lot(request, 'dlt')

def view_lot_hist(request, type):
    if type is None or len(type) ==0:
        type='dlt'
    web_content={}
    web_content['type']=type
    web_content['lots']=Guess.objects.filter().order_by('-create_time ')
    return render(request, 'lottery/view.html', web_content)