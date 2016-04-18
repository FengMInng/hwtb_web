'''
Created on Apr 18, 2016

@author: mfeng
'''
from __future__ import absolute_import

from celery import shared_task

@shared_task
def add(x, y):
    return x + y