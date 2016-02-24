# -*- coding: utf-8 -*- 
'''
Created on 2016年1月19日

@author: fangfang
'''
from django.conf.urls import url

from . import views

app_name='main'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^catagory/', views.catalog, name='catalog')
]