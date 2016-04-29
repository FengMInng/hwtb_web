from __future__ import unicode_literals

from django.db import models
from celery.worker.strategy import default
from datetime import datetime

# Create your models here.

class Base(models.Model):
    TYPES=(('dlt', 'dlt'), ('dc', 'dc'))
    type=models.CharField(max_length=10, choices=TYPES)
    red=models.CharField(max_length=100)
    blue=models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.red +" " + self.blue
    
    class Meta:
        abstract = True

class Guess(Base):
    validno=models.CharField(max_length=100,default="")
    level=models.IntegerField(default=0)
    create_time=models.DateTimeField(auto_now_add = True)
    
class History(Base):
    no = models.CharField(max_length=20)
    pub_date = models.DateTimeField()
    