'''
Created on Mar 29, 2016

@author: mfeng
'''
from django.conf.urls import url
from . import views

app_name='lottery'

urlpatterns = [
    url(r'^$', views.view_lot_default, name='view_dlt'),
    url(r'^hist/$', views.view_lot_hist, name='view_dlt_hist'),
    ]