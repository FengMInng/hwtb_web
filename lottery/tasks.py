'''
Created on Mar 23, 2016

@author: mfeng
'''

from __future__ import absolute_import

from datetime import datetime, date
from django.utils import timezone

from hwtb import celery_app


from .LotteryParser import Lot
from time import time
from lottery import lotteryguess
from .models import Guess, History

def read_history(type):
    hist_list={}
    hist = History.objects.filter(type=type).order_by('-pub_date')
    for h in hist:
        dc = lotteryguess.DC()
        for r in h.red.split():
            dc.append_red(int(r))
        for b in h.blue.split():
            dc.append_blue(int(b))
        hist_list[h.no]=dc
    return hist_list
@celery_app.task
def guess(type, idx):
    hist_list=read_history(type)
    lotteryguess.calculate_hist(hist_list)
    if type=='dlt':
        lot = lotteryguess.method1(hist_list, range(1,36), 5, range(1,13), 2, lotteryguess.Condition(45,145,1,4,1,4,0,4,13), 1)
        lg = Guess()
        lg.type = type
        lg.red = " ".join(lot[0].red)
        lg.blue = " ".join(lot[1].blue)
        lg.save()
    pass

def LotGsValidDlt(lot, l):
    pub_date = datetime.strptime(lot.pub_date, '%Y-%m-%d');
    if l.create_time > pub_date:
        return
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

def LotGsValid(lot, type):
    lgs=Guess.objects.filter(validno="", type=type)
    for l in lgs:
        if lot.type=='dlt':
            LotGsValidDlt(lot, l)
        else:
            LotGsValidDc(lot, l)
        l.save()
    pass

@celery_app.task
def collect(type='dlt'):
    lot = Lot(type)
    lot.m_hist = read_history(type)
    lot.run()
    for n in lot.new_hist:
        l = lot.m_hist[n]
        LotGsValid(l, type)
        try:
            hist = History.objects.get(no=l.no) 
        except Exception:
            hist = History()
        hist.no = l.no
        hist.type = type
        hist.red  = ' '.join(l.red)
        hist.blue = ' '.join(l.blue)
        hist.pub_date = timezone.template_localtime(datetime.strptime(l.pub_date, '%Y-%m-%d'))
        try:
            hist.save()
        except Exception as e:
            print e
            print hist.type, hist.red,hist.blue, hist.pub_date
            return
    pass
    
    return 