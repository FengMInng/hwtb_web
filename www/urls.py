# -*- coding: utf-8 -*- 
'''
Created on 2016年1月19日

@author: fangfang
'''
from django.conf.urls import url

from . import views

app_name='main'

urlpatterns = [
    url(r'^news', views.news, name='news'),
    url(r'^contactus', views.contactus, name='contactus'),
    url(r'^carriar', views.carriar, name='carriar'),
    url(r'^calture', views.calture, name='calture'),
    url(r'^introduction', views.introduction, name='introduction'),
    url(r'^aboutus', views.aboutus, name='aboutus'),
    url(r'^$', views.index, name='index'),
    url(r'^catalogs/', views.catalog, name='catalog'),
]