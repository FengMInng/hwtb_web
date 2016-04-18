'''
Created on 2015-5-25

@author: Administrator
'''

import datetime
import urllib2
from HTMLParser import HTMLParser
import re

class MyHTMLParser(HTMLParser):
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
    def __init__(self):
        self.no=None
    def parser(self, s):
        r = re.compile('\d+')
        l = r.findall(s)
        if len(l)==14:
            self.no = l[0]
            self.red=l[1:7]
            self.blue =l[13:]
        elif len(l)==8:
            self.no = l[0]
            self.red=l[1:7]
            self.blue =l[7:]
        
    def get(self,date):
        pass
    def tostring(self):
        s = (self.no)
        for n in self.red:
            s += " "+str(n)
        for n in self.blue:
            s+= " "+str(n)
        return s
    
    
class Lot:
    def __init__(self, filename="115.txt"):
        self.m_hist=self.openhist(filename)
        self.p10nolist=list()
        self.p3nolist=list()
        self.filename=filename
        self.first={}
        self.second={}
        self.third={}
        self.run()
        self.save()
        pass    
            
    def run(self):
        print len(self.m_hist)
        if len(self.m_hist)==0:
            date = datetime.date.today()
            htmlparser = MyHTMLParser(date.year,"http://tubiao.zhcw.com/tubiao/ssqNew/ssqInc/ssq_hq_general_dataTuAsckj_year={0}.html")
            
            while(len(htmlparser.m_hist)):
                print htmlparser.m_pn, len(htmlparser.m_hist)
                for line in htmlparser.m_hist:
                    lottery = Lottery()
                    lottery.parser(line)
                    if lottery.no not in self.m_hist.keys():
                        self.m_hist[lottery.no]=lottery
                htmlparser.getnextpage()
            htmlparser.close()
        else:
            htmlparser = MyHTMLParser(50,"http://tubiao.zhcw.com/tubiao/ssqNew/ssqInc/ssq_hq_general_dataTuAscselect={0}.html")
            
            for line in htmlparser.m_hist:
                lottery = Lottery()
                lottery.parser(line)
                if lottery.no not in self.m_hist.keys():
                    self.m_hist[lottery.no]=lottery
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
    
    lot =Lot("dc.txt")        
    pass