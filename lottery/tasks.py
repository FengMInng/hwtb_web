'''
Created on Mar 23, 2016

@author: mfeng
'''

from __future__ import absolute_import

import pytz
from datetime import datetime, timedelta

from hwtb import celery_app


from .LotteryParser import Lot
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
    lotteryguess.calculate_hist(hist_list.values())
    if type=='dlt':
        lot = lotteryguess.method1(hist_list.values(), range(1,36), 5, range(1,13), 2, lotteryguess.Condition(45,145,1,4,1,4,0,4,13), 1,idx)
    else:
        lot = lotteryguess.method1(hist_list.values(), range(1,34), 6, range(1,17), 1, lotteryguess.Condition(45,145,1,5,1,5,0,4,13), 1, idx)
        lg = Guess()
        lg.type = type
        for n in lot:
            for r in n.red:
                lg.red +=str(r)+" "
            for b in n.blue:
                lg.blue +=str(b)+" "
        lg.save()
        
    pass

def LotGsValidDlt(lot, l):
    
    td = lot.pub_date - l.create_time
    if (lot.pub_date.date().isoweekday() in [1,3] and td.day <2) or (lot.pub_date.date().isoweekday() in [6] and td.day <2):
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
    td = lot.pub_date - l.create_time
    if (lot.pub_date.date().isoweekday() in [2,4] and td.day <2) or (lot.pub_date.date().isoweekday() in [7] and td.day <2):
        rl = l.red.split(' ')
        for i in rl:
            for j in lot.red:
                if i == j:
                    l.level +=1
        
        bl = l.blue.split(' ')
        for i in bl:
            for j in lot.blue:
                if i == j:
                    l.level +=7
    l.valid = lot.pub_date

def LotGsValid(lot, type):
    lgs=Guess.objects.filter(validno="", type=type)
    for l in lgs:
        if l.create_time > lot.pub_date:
            continue
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
        hist = History()
        hist.no = n
        hist.type = type
        hist.red  = ' '.join(l.red)
        hist.blue = ' '.join(l.blue)
        pub_date = datetime.strptime(l.pub_date, '%Y-%m-%d')
        hist.pub_date = pub_date.replace(tzinfo=pytz.utc).astimezone(pytz.timezone('Asia/Shanghai')) + timedelta(hours=20)
        try:
            hist.save()
        except Exception as e:
            print e
            print hist.type, hist.red,hist.blue, hist.pub_date
            continue
    pass
    
    return 

@celery_app.task
def collect_dlt():
    return collect('dlt')

@celery_app.task
def collect_dc():
    return collect('dc')
