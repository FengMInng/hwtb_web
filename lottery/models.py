from __future__ import unicode_literals

from django.db import models
from celery.worker.strategy import default
from datetime import datetime
from lotteryguess import DC

# Create your models here.

class Base(models.Model):
    TYPES=(('dlt', 'dlt'), ('dc', 'dc'))
    type=models.CharField(max_length=10, choices=TYPES)
    red=models.CharField(max_length=100)
    blue=models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.red +" " + self.blue
    
    def __str__(self):
        return "{0} {1} {2}".format(self.type, self.red, self.blue)
    
    def toDC(self):
        rl = self.red.split()
        bl = self.blue.split()
        dc = DC()
        for r in rl:
            dc.append_red(int(r))
        for b in bl:
            dc.append_blue(int(b))
        pass
    class Meta:
        abstract = True

class Guess(Base):
    validno=models.CharField(max_length=100,default="")
    level=models.IntegerField(default=0)
    create_time=models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        s =  Base.__str__(self)
        return "{0} {1} {2} {3}".format(s, self.validno, self.level, self.create_time)
    
class History(Base):
    no = models.CharField(max_length=20)
    pub_date = models.DateTimeField()
    
    def __str__(self):
        s = Base.__str__(self)
        return "{0} {1} {2}".format(s, self.no, self.pub_date)