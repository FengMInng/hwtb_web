from __future__ import unicode_literals

from django.db import models

# Create your models here.

class LotteryGuess(models.Model):
    TYPES=(('dlt', 'dlt'), ('dc', 'dc'))
    type=models.CharField(max_length=10, choices=TYPES)
    red=models.CharField(max_length=100)
    blue=models.CharField(max_length=100)
    validno=models.CharField(max_length=100,default="")
    level=models.IntegerField(default=0)
    creat_time=models.DateTimeField(auto_now_add = True)
    
