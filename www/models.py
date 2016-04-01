# -*- coding: utf-8 -*- 
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.admin.options import ModelAdmin
from django.utils.translation import ugettext as _
from ckeditor_uploader.fields  import RichTextUploadingField
from hwtb.settings import CKEDITOR_EXTRAPLUGS_CONFIG

# Create your models here.
class ImageStore(models.Model):
    title = models.CharField(verbose_name=_('title'), max_length=100, unique=True)
    img = models.ImageField(upload_to = 'img/%Y%m%d')
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = _('image')


class Roll(models.Model):
    title = models.CharField(verbose_name=_('title'), max_length=100)
    photo = models.ImageField(verbose_name=_('photo'), upload_to = 'roll/%Y%m%d')
    descriptor = RichTextUploadingField(_('description'), \
                                extra_plugins=CKEDITOR_EXTRAPLUGS_CONFIG)
    
    # create date and time
    create_date = models.DateTimeField(_('createtime'), auto_now_add = True, editable=False, null=True)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = _('roll')

class AbstractProduct(models.Model):
    '''
    this model is for model base
    '''
    # product catalog name
    name = models.CharField(_('name'), max_length=100)
    ##photo for index
    photo = models.ImageField(verbose_name=_('photo'), upload_to='img/%Y%m%d')
    # product descriptor
    descriptor = RichTextUploadingField(_('description'), \
                                extra_plugins=CKEDITOR_EXTRAPLUGS_CONFIG)
    
    
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
    fields = ('name', 'photo', 'descriptor', 'show_start', 'show_end', 'is_delete', 'catalog', 'price')
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
    descriptions = RichTextUploadingField(_('description'), \
                                extra_plugins=CKEDITOR_EXTRAPLUGS_CONFIG)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = _('solution')

class News(models.Model):
    NEWS_TYPE=((_('dynamics'), _('dynamics')), (_('honor'), _('honor')))
    title = models.CharField(verbose_name = _('title'), max_length=100)
    contont = RichTextUploadingField(_('contont'), \
                                extra_plugins=CKEDITOR_EXTRAPLUGS_CONFIG)
    type = models.CharField(choices=NEWS_TYPE, verbose_name = _('news type'), max_length=100)
    # create date and time
    create_date = models.DateTimeField(_('createtime'), null=True, blank = True, editable=False, auto_now_add = True)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = _('new')
        
class Location(models.Model):
    city = models.CharField(verbose_name=_('city'), max_length=100)
    state = models.CharField(verbose_name=_('state'), max_length=100)
    country=models.CharField(verbose_name=_('country'), max_length=100)
    
    def __unicode__(self):
        return "%s %s %s" % (self.city, self.state, self.country)
    
    class Meta:
        verbose_name_plural = _('location')
        
class Job(models.Model):
    #
    position = models.CharField(verbose_name=_('position'), max_length=100)
    pub_date=models.DateField(verbose_name = _('publish date'))
    end_date=models.DateField(verbose_name=_('end date'))
    location = models.ForeignKey(Location, verbose_name=_('location'),  max_length=100)
    recruiting_numbers = models.IntegerField(verbose_name=_('recruiting numbers'), default = 1)
    responsibilitie = models.TextField(verbose_name=_('responsibilitie'))
    qualification = models.TextField(verbose_name = _('qualification'))
    
    
    class Meta:
        verbose_name_plural = _('job')
    
    
    def __unicode__(self):
        return self.position
    
class OnlineService(models.Model):
    TYPE = (('QQ', 'QQ'), ('weixin', _('weixin')), ('wangwang', _('wangwang')), ('tel', _('tel')))
    type = models.CharField(verbose_name=_('type'), choices=TYPE, max_length=100)
    account = models.CharField(verbose_name=_('account'), max_length=100)
    name = models.CharField(verbose_name=_('name'), max_length=100)
    qrcode = models.ImageField(upload_to = 'img/qrcode', verbose_name=_('qrcode'), null=True, blank=True)
    
    class Meta:
        verbose_name_plural = _('online service')
        
    def __unicode__(self):
        return "%s %s" %(self.type , self.name)
    
class AboutUs(models.Model):
    ABOUT_US_TYPE=(('introduction', _('introdution')),
                   ('calture', _('calture')),
                   ('address', _('address')))
    type = models.CharField(verbose_name=_('type'), max_length = 100, unique=True, choices= ABOUT_US_TYPE)
    content = RichTextUploadingField(verbose_name = _('content'),extra_plugins=CKEDITOR_EXTRAPLUGS_CONFIG)
    
    def __unicode__(self):
        return self.type
    
    class Meta:
        verbose_name_plural = _('about us')
        

class FriendLink(models.Model):
    name = models.CharField(verbose_name=_('name'), max_length = 100)
    url = models.CharField(verbose_name=_('url'), max_length=100)
    logo = models.ImageField(verbose_name=_('logo'), upload_to='friendlink')
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = _('friend link')
        