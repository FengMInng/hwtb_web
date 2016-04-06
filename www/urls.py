# -*- coding: utf-8 -*- 
'''
Created on 2016年1月19日

@author: fangfang
'''
from django.conf.urls import url

from . import views

app_name='www'

urlpatterns = [
    url(r'^roll/(?P<catalog_id>[0-9]+)/$', views.roll_view, name='roll_view'),
    url(r'^news/(?P<news_id>[0-9]+)/$', views.news_detail, name='news_detail'),
    url(r'^news$', views.news, name='news'),
    url(r'^contactus$', views.contactus, name='contactus'),
    url(r'^carriar$', views.carriar, name='carriar'),
    url(r'^calture$', views.calture, name='calture'),
    url(r'^introduction$', views.introduction, name='introduction'),
    url(r'^aboutus$', views.aboutus, name='aboutus'),
    url(r'^$', views.index, name='index'),
    url(r'^catalogs/$', views.catalog, name='catalog'),
    url(r'^catalogs/(?P<catalog_id>[0-9]+)/$', views.catalog_list, name='catalog_list'),
    url(r'^prodcuts/(?P<product_id>[0-9]+)/$', views.product, name='product'),
    url(r'^job/(?P<job_id>[0-9]+)/$', views.job_detail, name='job_detail'),
    url(r'^upload/', views.upload, name='upload'),
    url(r'^browser/(?P<path>[\w]+)$', views.browser, name='browser')
]