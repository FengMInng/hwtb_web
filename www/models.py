# -*- coding: utf-8 -*- 
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.admin.options import ModelAdmin
from django.utils.translation import ugettext as _
from ckeditor.fields  import RichTextField
# Create your models here.
class Description(models.Model):
    title = models.CharField(verbose_name=_('title'), max_length=100, unique=True)
    content = models.TextField(_('content'))
    img = models.ImageField(upload_to = 'img/%Y%m%d')
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = _('description')


class Roll(models.Model):
    title = models.CharField(verbose_name=_('title'), max_length=100)
    photo = models.ImageField(verbose_name=_('photo'), upload_to = 'roll/%Y%m%d')
    page = models.FileField(verbose_name = _('static page'), upload_to='roll/%Y%m%d')
    
    # create date and time
    create_date = models.DateTimeField(_('createtime'), auto_now_add = True, editable=False, null=True)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = _('roll photo')

class AbstractProduct(models.Model):
    '''
    this model is for model base
    '''
    # product catalog name
    name = models.CharField(_('name'), max_length=100)
    # product descriptor
    descriptor = RichTextField(_('description'))
    
    #pic
    imgs = models.ManyToManyField(Description)
    
    # create date and time
    create_date = models.DateTimeField(_('createtime'), auto_now_add = True, editable=False)
    #create user
    create_user = models.ForeignKey(User, verbose_name=_('createuser'), null=True, blank = True)
    
    last_modify_user = models.ForeignKey(User, related_name='%(app_label)s_%(class)s_modify_user', verbose_name=_('last_modify_user'),null=True, blank = True)
    last_modify_date = models.DateTimeField(verbose_name=_('laster modify time'), auto_now=True)
    
    #validate date
    show_start = models.DateField(verbose_name=_('show start'),null=True, blank = True)
    show_end = models.DateField(verbose_name=_('show end'),null=True, blank = True)
    
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
        verbose_name_plural=_('product catalog')

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
    
    def delete_model(self, request, obj):
        obj.is_delete = True
        obj.last_modify_user = request.user
        obj.save()

class Product(AbstractProduct):
    '''
    this model is for product
    '''
    #parent catalog
    catalog = models.ForeignKey(ProductCatalog,on_delete=models.CASCADE)
    
    
    price = models.DecimalField(verbose_name=_('price'),max_digits=20, decimal_places=2,default=0.00)
    
    class Meta:
        verbose_name_plural = _('product')
    

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
    
    def delete_model(self, request, obj):
        obj.is_delete = True
        obj.last_modify_user = request.user
        obj.save()

class Solution(models.Model):
    title = models.CharField(verbose_name=_('title'), max_length=100, unique = True)
    photo = models.ImageField(verbose_name=_('photo'), upload_to='img/%Y%m%d')
    descriptions = models.ManyToManyField(Description,verbose_name=_('description'))
    photo = models.ImageField(upload_to = 'img/%Y%m%d', null=True)
    page = models.FileField(verbose_name=_('static page'), upload_to='solution/%Y%m%d', max_length=100, null=True)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = _('solution')

class News(models.Model):
    NEWS_TYPE=((_('dynamics'), _('dynamics')), (_('honor'), _('honor')))
    title = models.CharField(verbose_name = _('title'), max_length=100)
    contont = models.TextField(verbose_name = _('content'))
    type = models.CharField(choices=NEWS_TYPE, verbose_name = _('news type'), max_length=100)
    page = models.FileField(verbose_name=_('static page'), upload_to='news/%Y%m%d', max_length=100, null=True, blank=True)
    imgs = models.ManyToManyField(Description, verbose_name=_('photo'))
    # create date and time
    create_date = models.DateTimeField(_('createtime'), null=True, blank = True, editable=False, auto_now_add = True)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = _('new')
        

class Job(models.Model):
    LOCATIONS=(('bj', _('beijing')),
               ('sh', _('shanghai')))
    title = models.CharField(verbose_name=_('title'), max_length=100)
    position = models.CharField(verbose_name=_('position'), max_length=100)
    pub_date=models.DateField(verbose_name = _('publish date'))
    end_date=models.DateField(verbose_name=_('end date'))
    location = models.CharField(verbose_name=_('location'), choices=LOCATIONS, max_length=100)
    recruiting_numbers = models.IntegerField(verbose_name=_('recruiting numbers'), default = 1)
    responsibilitie = models.TextField(verbose_name=_('responsibilitie'))
    qualification = models.TextField(verbose_name = _('qualification'))
    
    
    class Meta:
        verbose_name_plural = _('job')
    
    
    def __unicode__(self):
        return self.title
    
class OnlineService(models.Model):
    TYPE = (('QQ', 'QQ'), ('weixin', _('weixin')), ('wangwang', _('wangwang')), ('tel', _('tel')))
    type = models.CharField(verbose_name=_('type'), choices=TYPE, max_length=100)
    account = models.CharField(verbose_name=_('account'), max_length=100)
    name = models.CharField(verbose_name=_('name'), max_length=100)
    qrcode = models.ImageField(upload_to = 'img/qrcode', verbose_name=_('qrcode'), null=True, blank=True)
    
    class Meta:
        verbose_name_plural = _('online service')
        
    def __unicode__(self):
        return self.type +":"+self.name
    
