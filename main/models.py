# -*- coding: utf-8 -*- 
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.admin.options import ModelAdmin
from time import timezone
# Create your models here.

class ProductCatalog(models.Model):
    '''
    this model is for product catalog, which catalog have some  product
    '''
    # product catalog name
    name = models.CharField('name',max_length=100)
    # product descriptor
    descriptor = models.TextField('description')
    # create date and time
    create_date = models.DateTimeField('createtime', null=True, blank = True)
    #create user
    create_user = models.ForeignKey(User, verbose_name='createuser', null=True, blank = True)
    
    last_modify_user = models.ForeignKey(User, related_name='%(app_label)s_%(class)s_modify_user', verbose_name='last_modify_user',null=True, blank = True)
    last_modify_date = models.DateTimeField(verbose_name='laster_modify_time',null=True, blank = True)
    
    #validate date
    show_from = models.DateField('show_from',null=True, blank = True)
    show_end = models.DateField('show_end',null=True, blank = True)
    
    #if delete, remain
    is_delete = models.BooleanField(False)
    
    def __unicode__(self):
        return self.name

class ProductCatalogAdmin(ModelAdmin):
    list_display = ('name', 'show_from', 'show_end', 'is_delete')
    search_fields = ('name','show_from')
    list_filter =('name', 'create_date')
    date_hierarchy = 'create_date'
    fields = ('name', 'descriptor', 'show_from', 'show_end', 'is_delete')
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'create_user', None) is None:
            obj.create_user = request.user
        obj.last_modify_user = request.user
        #obj.last_modify_date = timezone.now()
        obj.save()
    pass

class Product(models.Model):
    '''
    this model is for product
    '''
    #show name
    name = models.CharField(max_length=100)
    #parent catalog
    catalog = models.ForeignKey(ProductCatalog,on_delete=models.CASCADE)
    
    descriptor = models.TextField()
    
    price = models.FloatField(default=0.00)
    
    show_from = models.DateField(null=True, blank = True)
    show_end = models.DateField(null=True, blank = True)
    # create date and time
    create_date = models.DateTimeField(null=True, blank = True,auto_now_add=True)
    #create user
    create_user = models.ForeignKey(User, verbose_name='createuser', null=True, blank = True)
    
    last_modify_user = models.ForeignKey(User, related_name='%(app_label)s_%(class)s_modify_user', verbose_name='last_modify_user',null=True, blank = True)
    last_modify_date = models.DateTimeField(verbose_name ='laster_modify_time',null=True, blank = True, auto_now=True)
    
    def __unicode__(self):
        return self.name
    

class ProductAdmin(ModelAdmin):
    list_display = ('name', 'show_from', 'show_end')
    search_fields = ('name','show_from')
    list_filter =('name', 'create_date')
    date_hierarchy = 'create_date'
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'create_user', None) is None:
            obj.create_user = request.user
        obj.last_modify_user = request.user
        #obj.last_modify_date = timezone.now()
        obj.save()
    pass