'''
Created on 2015-5-25

@author: Administrator
'''

import urllib2, datetime
from HTMLParser import HTMLParser
import re


class DltHTMLParser(HTMLParser):
    def __init__(self,pn):
        HTMLParser.__init__(self)
        self.m_stack=list()
        self.m_hist=list()
        self.m_str=None
        self.m_pn = pn
        self.m_debug =  False
        self.m_html=self.gethtml(pn)
        if self.m_html:
            self.feed(self.m_html)
        pass
    
    def gethtml(self,p):
        url = "http://chart.lottery.gov.cn/dltBasicZongHeTongJi.do?typ=1&issueTop=100"
        if self.m_debug:
            print url
        try:
            page = urllib2.urlopen(url)
            return page.read()
        except Exception as e:
            print e  
            return None 
                     
    def getnextpage(self):
        self.m_hist = list()
        self.m_pn +=1
        self.m_html = self.gethtml(self.m_pn)
        if self.m_html:
            self.feed(self.m_html)
        pass
        
    def handle_starttag(self, tag, attrs):
        if tag == 'tr':
            for (variable, value)  in attrs:
                if variable=='class' and value =='r1':
                    self.m_stack.append(tag)
        elif tag == 'td':
            if(len(self.m_stack)>0) and (self.m_stack[-1] == 'tr'):
                for (variable, value)  in attrs:
                    if variable=='class' and (value in ['EndTime','Issue']):
                        self.m_stack.append(tag)
        pass
    
    def handle_data(self, data):
        if '/'.join(self.m_stack) == 'tr/td':
            if len(data.strip()) == 10 :
                self.m_str = data.strip()
                self.m_step=0
            else:
                self.m_str += " " + data
                self.m_step +=1
                
            if self.m_step == 2:
                self.m_hist.append(unicode(self.m_str, 'utf8'))
                self.m_str = None
    
    def handle_endtag(self,tag):
        if len(self.m_stack) > 0 and self.m_stack[-1] == tag:
            self.m_stack.pop()
        pass

class SsqHTMLParser(HTMLParser):
    def __init__(self,pn):
        HTMLParser.__init__(self)
        self.m_stack=list()
        self.m_hist=list()
        self.m_str=None
        self.m_url='http://tubiao.zhcw.com/tubiao/ssqNew/ssqInc/ssq_hq_general_dataTuAsckj_year={0}.html'
        self.m_pn = pn
        self.m_debug = False
        self.m_html=self.gethtml(pn)
        if self.m_html:
            self.feed(self.m_html)
        pass
    
    def gethtml(self,year):
        url = self.m_url.format(str(year))
        if self.m_debug:
            print url
        try:
            page = urllib2.urlopen(url)
            return page.read()
        except Exception as e:
            print e  
            return None 
                     
    def getnextpage(self):
        self.m_hist = list()
        self.m_pn -=1
        self.m_html = self.gethtml(self.m_pn)
        if self.m_html:
            self.feed(self.m_html)
        pass
        
    def handle_starttag(self, tag, attrs):
        if tag=='table':
            for (variable, value)  in attrs:
                if variable == 'id' and value=='table_ssq':
                    self.m_stack.append(tag)
        if tag=='tr':
            if(len(self.m_stack)>0) and self.m_stack[-1]=='table':
                self.m_stack.append(tag)
        if tag == 'td':
            if(len(self.m_stack)>0) and (self.m_stack[-1] == 'tr'):
                for (variable, value)  in attrs:
                    if variable=='class' and (value=='qh8 bjcolor1 td_b td_rb' or value=='qh8 bjcolor1 td_bb td_rb' or value=='lfx3t bjcolor1r12 td_b td_rb' or value=='lfx3t bjcolor1r12 td_bb td_rb' or value=='tq bjcolor1r13 td_b td_rb' or value == 'tq bjcolor1r13 td_bb td_rb'):
                        self.m_stack.append(tag)
        if tag == 'a':
            if(len(self.m_stack)>0) and (self.m_stack[-1] == 'td'):
                    self.m_stack.append(tag)
            for (variable, value)  in attrs:
                if variable == 'title':
                    self.kjrq = unicode(value, 'utf8')[-10:]
        pass
    
    def handle_data(self, data):
        
        if '/'.join(self.m_stack) == 'table/tr/td/a' and len(data.strip()) == 7:
            self.m_str = data.strip()
        if '/'.join(self.m_stack) == 'table/tr/td':
            if self.m_str:
                self.m_str = self.m_str + " " + data.strip()
                if len(self.m_str)==46:
                    self.m_hist.append(unicode(self.m_str, 'utf8') + " " + self.kjrq)
                    self.m_str = None
                
    
    def handle_endtag(self,tag):
        if len(self.m_stack) > 0 and self.m_stack[-1] == tag:
            self.m_stack.pop()
        pass
        
class Lottery:
    @staticmethod
    def parse_dlt(s):
        lot = Lottery()
        lot.pub_date = s[:10]
        lot.no = s[11:18]
        r = re.compile('\d+')
        l = r.findall(s[19:])
        if len(l)==7:
            lot.red=l[0:5]
            lot.blue =l[5:7]
        return lot
    @staticmethod
    def parse_ssq(s):
        lot = Lottery()
        lot.no = s[0:7]
        r = re.compile('\d+')
        l = r.findall(s[7:47])
        lot.red=l[0:6]
        lot.blue =l[12]
        lot.pub_date = s[47:]
        return lot
    
    def __str__(self):
        s = (self.no)
        for n in self.red:
            s += " "+str(n)
        s+=" +"
        for n in self.blue:
            s+= " "+str(n)
        return s
    
    
class Lot:
    def __init__(self, lot_type):
        self.lot_type = lot_type
        self.m_hist={}
        self.p10nolist=list()
        self.p3nolist=list()
        self.first={}
        self.second={}
        self.third={}
        self.new_hist=[]
        pass    
            
    def run(self):
        if self.lot_type == 'dlt':
            htmlparser = DltHTMLParser(1)
        else:
            htmlparser = SsqHTMLParser(datetime.date.today().year)
        conti=1
        
        while(len(htmlparser.m_hist)and conti):
            print htmlparser.m_pn, len(htmlparser.m_hist)
            for line in htmlparser.m_hist:
                print line
                if self.lot_type == 'dlt':
                    lottery = Lottery.parse_dlt(line)
                else:
                    lottery = Lottery.parse_ssq(line)
                
                print lottery
                if lottery.no not in self.m_hist.keys():
                    self.m_hist[lottery.no]=lottery
                    self.new_hist.append(lottery.no)
                else:
                    conti=0
            if conti >0:
                htmlparser.getnextpage()
        htmlparser.close()
                    
    def save(self):
        wfile = open(self.filename, "w")
        plist = sorted(self.m_hist.keys())
        for n in range(0,len(plist)):
            wfile.write(self.m_hist[plist[-1-n]].tostring()+"\n")
            wfile.flush()
        wfile.close()
        
    def openhist(self,filename):
        rt={}
        f = open(filename)
    
        for line in f:
            lot = Lottery()
            lot.parser(line)
            if lot.no:
                rt[lot.no]=lot
        f.close()
        return rt
       
            
if __name__ == '__main__':
    
    lot =Lot('dlt')       
    lot.run() 
    for k,v in lot.m_hist.iteritems():
        print k, v.pub_date, v.red
    pass