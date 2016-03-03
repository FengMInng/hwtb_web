# -*- coding: utf-8 -*- 
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.admin.options import ModelAdmin
from django.utils.translation import ugettext as _
# Create your models here.

class AbstractProduct(models.Model):
    '''
    this model is for model base
    '''
    # product catalog name
    name = models.CharField(_('name'),max_length=100)
    # product descriptor
    descriptor = models.TextField(_('description'))
    # create date and time
    create_date = models.DateTimeField(_('createtime'), null=True, blank = True)
    #create user
    create_user = models.ForeignKey(User, verbose_name=_('createuser'), null=True, blank = True)
    
    last_modify_user = models.ForeignKey(User, related_name='%(app_label)s_%(class)s_modify_user', verbose_name=_('last_modify_user'),null=True, blank = True)
    last_modify_date = models.DateTimeField(verbose_name=_('laster_modify_time'),null=True, blank = True)
    
    #validate date
    show_start = models.DateField(_('show_start'),null=True, blank = True)
    show_end = models.DateField(_('show_end'),null=True, blank = True)
    
    #if delete, remain
    is_delete = models.BooleanField(False)
    
    class Meta:
        abstract = True
    
    def __unicode__(self):
        return self.name
    
    
class ProductCatalog(AbstractProduct):
    '''
    this model is for product catalog, which catalog have some  product
    '''
    
    class Meta:
        verbose_name=_('product_catalog')

class ProductCatalogAdmin(ModelAdmin):
    list_display = ('name', 'show_start', 'show_end', 'is_delete')
    search_fields = ('name','show_start')
    list_filter =('name', 'create_date')
    date_hierarchy = 'create_date'
    fields = ('name', 'descriptor', 'show_start', 'show_end', 'is_delete')
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'create_user', None) is None:
            obj.create_user = request.user
        obj.last_modify_user = request.user
        obj.save()
    pass

class Product(AbstractProduct):
    '''
    this model is for product
    '''
    #parent catalog
    catalog = models.ForeignKey(ProductCatalog,on_delete=models.CASCADE)
    
    price = models.FloatField(default=0.00)
    
    class Meta:
        verbose_name = _('product')
    

class ProductAdmin(ModelAdmin):
    list_display = ('name', 'show_start', 'show_end')
    search_fields = ('name','show_start')
    list_filter =('name', 'create_date')
    date_hierarchy = 'create_date'
    fields = ('name', 'descriptor', 'show_start', 'show_end', 'is_delete', 'catalog', 'price')
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'create_user', None) is None:
            obj.create_user = request.user
        obj.last_modify_user = request.user
        obj.save()
    pass