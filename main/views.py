from django.shortcuts import render

# Create your views here.

def index(request):
    web_content={'pc_style_color':1}
    return render(request, 'main/index.html', web_content)
