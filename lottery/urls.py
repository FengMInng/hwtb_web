'''
Created on Mar 29, 2016

@author: mfeng
'''
from django.conf.urls import url
from . import views

app_name='lottery'

urlpatterns = [
    url(r'^$', views.view_dlt, name='view_dlt'),
    url(r'^dlt/$', views.view_dlt, name='view_dlt'),
    url(r'^dlt/hist$', views.view_dlt_hist, name='view_dlt_hist'),
    url(r'^dc/$', None, name='view_dc')
    ]