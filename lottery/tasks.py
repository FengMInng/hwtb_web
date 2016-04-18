'''
Created on Mar 23, 2016

@author: mfeng
'''

from __future__ import absolute_import

from datetime import datetime

from celery import shared_task
from hwtb import celery_app


from .LotteryParser import Lot
from time import time
from lottery import lotteryguess
from .models import LotteryGuess
@celery_app.task
def guess(type, idx):
    hist = lot_hist[type] 
    if type=='dlt':
        lot = lotteryguess.method1(hist, range(1,36), 5, range(1,13), 2, lotteryguess.Condition(), 1)
        lg = LotteryGuess()
        lg.type = type
        lg.red = " ".join(lot[0].red)
        lg.blue = " ".join(lot[1].blue)
        lg.save()
    pass

def LotGsValidDlt(lot, l):
    pub_date = datetime.strptime(lot.pub_date, '%Y-%m-%d');
    if l.create_time > pub_date:
        continue;
    td = pub_date - l.create_time
    if (pub_date.date().isoweekday() in [1,3] and td.day <2) or (pub_date.date().isoweekday() in [6] and td.day <2):
        rl = l.red.split(' ')
        for i in rl:
            for j in lot.red:
                if i == j:
                    l.level +=1
        
        bl = l.blue.split(' ')
        for i in bl:
            for j in lot.blue:
                if i == j:
                    l.level +=6
    l.valid = lot.pub_date

def LotGsValidDc(lot, l):
    pass

def LotGsValid(lot):
    lgs=LotteryGuess.objects.filter(validno="", type=lot.type)
    for l in lgs:
        if lot.type=='dlt':
            LotGsValidDlt(lot, l)
        else:
            LotGsValidDc(lot, l)
        l.save()
    pass

@celery_app.task
def collect(type):
    global lot_hist
    lot = Lot(type)
    lot.run()
    lot_hist[type]=lot
    if lot.new_count >0:
        for i in range(0, lot.new_count):
            LotGsValid(lot.m_hist[-1-i])
            pass
        pass
    
    return 