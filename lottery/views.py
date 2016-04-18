from django.shortcuts import render
from lottery.models import LotteryGuess

# Create your views here.

def view_dlt(request):
    web_content={}
    web_content['lots']=LotteryGuess.objects.filter(validno="")
    return render(request, 'lottery/view.html', web_content)

def view_dlt_hist(request):
    web_content={}
    web_content['lots']=LotteryGuess.objects.filter().order_by('-create_time ')
    return render(request, 'lottery/view.html', web_content)