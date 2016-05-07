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
        dc.pub_date=h.pub_date
        dc.type = type
        dc.no = h.no
        hist_list[h.no]=dc
    return hist_list
@celery_app.task
def guess(type='dlt', do_test=False):
    hist_list=read_history(type)
    lotteryguess.calculate_hist(hist_list.values())
    if type=='dlt':
        lot = lotteryguess.method1(hist_list.values(), range(1,36), 5, range(1,13), 2, lotteryguess.Condition(45,145,1,4,1,4,0,4,13), 2,2)
    else:
        lot = lotteryguess.method1(hist_list.values(), range(1,34), 6, range(1,17), 1, lotteryguess.Condition(45,145,1,5,1,5,0,4,13), 2, 1)
    
    if do_test:
        return lot
    
    for n in lot:
        lg = Guess()
        lg.type = type
        for r in n.red:
            lg.red +=str(r)+" "
        for b in n.blue:
            lg.blue +=str(b)+" "
        lg.save()
        
    return lot

def LotGsValidDlt(lot, l):
    level = 0
    td = lot.pub_date - l.create_time
    if (lot.pub_date.date().isoweekday() in [1,3] and td.days <2) or (lot.pub_date.date().isoweekday() in [6] and td.days <3):
        rl = l.red.split(' ')
        for i in rl:
            for j in lot.red:
                if i == j:
                    level +=1
        
        bl = l.blue.split(' ')
        for i in bl:
            for j in lot.blue:
                if i == j:
                    level +=6
        if level==17:
            #5+2
            l.level = 1
        elif level == 11:
            #5+1
            l.level = 2
        elif level in [5 ,16]:
            #5+0
            #4+2
            l.level=3
        elif level in [10,15]:
            #4+1
            #3+2
            l.level=4
        elif level in [4,9,14]:
            #4+0
            #3+1
            #2+2
            l.level = 5
        elif level in [3,8,13,12]:
            #3+0
            #2+1
            #1+2
            #0+2
            l.level=6
        else:
            l.level=0

def LotGsValidDc(lot, l):
    level=0
    td = lot.pub_date - l.create_time
    if (lot.pub_date.date().isoweekday() in [2,4] and td.days <2) or (lot.pub_date.date().isoweekday() in [7] and td.days <3):
        rl = l.red.split(' ')
        for i in rl:
            for j in lot.red:
                if i == j:
                    level +=1
        
        bl = l.blue.split(' ')
        for i in bl:
            for j in lot.blue:
                if i == j:
                    level +=7
        if level in [13]:
            #6+1
            l.level = 1
        elif level in [ 6]:
            #6+0
            l.level = 2
        elif level in [12]:
            #5+1
            l.level=3
        elif level in [5,11]:
            #5+0
            #4+1
            l.level=4
        elif level in [4,10]:
            #4+0
            #3+1
            l.level = 5
        elif level in [7,8,9]:
            #2+1
            #1+1
            #0+1
            l.level=6
        else:
            l.level=0
def LotGsValid(type,is_force=False):
    hists=read_history(type)
    lgs=Guess.objects.filter(type=type)
    if is_force is False:
        lgs=lgs.filter(validno="")
    for l in lgs:
        for lot in hists.values():
            if l.create_time > lot.pub_date:
                continue
            if lot.type=='dlt':
                LotGsValidDlt(lot, l)
            else:
                LotGsValidDc(lot, l)
            l.validno = lot.no
            l.save()
    pass

@celery_app.task
def collect(type='dlt'):
    lot = Lot(type)
    lot.m_hist = read_history(type)
    lot.run()
    for n in lot.new_hist:
        l = lot.m_hist[n]
        
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
    LotGsValid(type)
    
    return 

@celery_app.task
def collect_dlt():
    return collect('dlt')

@celery_app.task
def collect_dc():
    return collect('dc')

@celery_app.task
def Collect():
    ts=['dlt', 'dc']
    for t in ts:
        collect(t)

@celery_app.task
def GuessB():
    ts=['dlt', 'dc']
    for t in ts:
        guess(t)