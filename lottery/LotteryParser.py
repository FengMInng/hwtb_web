'''
Created on 2015-5-25

@author: Administrator
'''

import urllib2
from HTMLParser import HTMLParser
import re

class DltHTMLParser(HTMLParser):
    def __init__(self,pn):
        HTMLParser.__init__(self)
        self.m_stack=list()
        self.m_hist=list()
        self.m_str=None
        self.m_pn = pn
        self.m_html=self.gethtml(pn)
        if self.m_html:
            self.feed(self.m_html)
        pass
    
    def gethtml(self,p):
        url = "http://www.lottery.gov.cn/lottery/dlt/History.aspx?p="+str(p)
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
        if len(self.m_hist) >= 50:
            return
        if tag=='tr':
            for (variable, value)  in attrs:
                if variable == 'bgcolor':
                    if (value=='#ffffff' or value=='#f4f4f4'):
                        self.m_stack.append(tag)
        if tag == 'td':
            if(len(self.m_stack)>0):
                if(self.m_stack[-1] == 'tr'):
                    self.m_stack.append(tag)
        if tag == 'b':
            if(len(self.m_stack)>0):
                if(self.m_stack[-1] == 'td'):
                    self.m_stack.append(tag)
        if tag == 'font':
            if(len(self.m_stack)>0):
                if(self.m_stack[-1] == 'b'):
                    self.m_stack.append(tag)
        pass
    
    def handle_data(self, data):
        if '/'.join(self.m_stack) == 'tr/td' and len(data.strip()) == 5 :
            if self.m_str is None:
                self.m_str = data.strip()
                self.m_step=0
        if '/'.join(self.m_stack) == 'tr/td/b/font':
            if self.m_str:
                self.m_step=1
                self.m_str = self.m_str + " " + data.strip()
                if len(data.strip())==5:
                    self.m_step=2
                    
        if '/'.join(self.m_stack) == 'tr/td' and len(data.strip()) == 10 :
            if self.m_step == 2:
                self.m_str = self.m_str + " " + data.strip()
                self.m_hist.append(unicode(self.m_str, 'utf8'))
            self.m_str = None
    
    def handle_endtag(self,tag):
        if len(self.m_stack) > 0 and self.m_stack[-1] == tag:
            self.m_stack.pop()
        pass

class SsqHTMLParser(HTMLParser):
    def __init__(self,pn,url):
        HTMLParser.__init__(self)
        self.m_stack=list()
        self.m_hist=list()
        self.m_str=None
        self.m_url=url
        self.m_pn = pn
        self.m_html=self.gethtml(pn)
        if self.m_html:
            self.feed(self.m_html)
        pass
    
    def gethtml(self,year):
        url = self.m_url.format(str(year))
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
        pass
    
    def handle_data(self, data):
        
        if '/'.join(self.m_stack) == 'table/tr/td/a' and len(data.strip()) == 7:
            self.m_str = data.strip()
        if '/'.join(self.m_stack) == 'table/tr/td':
            
            if self.m_str:
                self.m_str = self.m_str + " " + data.strip()
                if len(self.m_str)==46:
                    self.m_hist.append(unicode(self.m_str, 'utf8'))
                    self.m_str = None
                
    
    def handle_endtag(self,tag):
        if len(self.m_stack) > 0 and self.m_stack[-1] == tag:
            self.m_stack.pop()
        pass
        
class Lottery:
    def __init__(self,):
        self.no=None
    def parser(self, s):
        r = re.compile('\d+')
        l = r.findall(s)
        if len(l)==8:
            self.no = l[0]
            self.red=l[1:6]
            self.blue =l[6:8]
    
    @staticmethod
    def parse_dlt(s):
        lot = Lottery
        lot.no = s[0:5]
        r = re.compile('\d+')
        l = r.findall(s[6:27])
        if len(l)==7:
            lot.red=l[0:5]
            lot.blue =l[5:7]
        lot.pub_date=s[27:]
        return lot
    @staticmethod
    def parse_ssq(s):
        lot = Lottery
        r = re.compile('\d+')
        l = r.findall(s)
        if len(l)==8:
            lot.no = l[0]
            lot.red=l[1:7]
            lot.blue =l[7:8]
        return lot
    
    def get(self,date):
        pass
    def tostring(self):
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
            htmlparser = SsqHTMLParser(1)
        conti=1
        
        while(len(htmlparser.m_hist)and conti):
            print htmlparser.m_pn, len(htmlparser.m_hist)
            for line in htmlparser.m_hist:
                if self.lot_type == 'dlt':
                    lottery = Lottery.parse_dlt(line)
                else:
                    lottery = Lottery.parse_ssq(line)
                    
                if lottery.no not in self.m_hist.keys():
                    self.m_hist[lottery.no]=lottery
                    self.new_hist.append(lottery.no)
                else:
                    conti=0
                    break
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
    pass