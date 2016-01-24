from __future__ import unicode_literals

from django.db import models

# Create your models here.

class ProductCatalog(models.Model):
    '''
    this model is for product catalog, which catalog have some  product
    '''
    # product catalog name
    name = models.CharField(max_length=100)
    # product descriptor
    descriptor = models.CharField(max_length=500)
    # create date and time
    create_date = models.DateTimeField()
    #create user
    create_user = models.CharField(max_length=100)
    
    #validate date
    show_from = models.DateField()
    show_end = models.DateField()
    
    #if delete, remain
    is_delete = models.BooleanField(False)
    
    def __unicode__(self):
        return self.name
    

class Product(models.Model):
    '''
    this model is for product
    '''
    #parent catalog
    catalog = models.ForeignKey(ProductCatalog,on_delete=models.CASCADE)
    
    #show name
    name = models.CharField(max_length=100)
    descriptor = models.CharField(max_length=500)