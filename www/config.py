# -*- coding: utf-8 -*- 
'''
Created on Feb 19, 2016

@author: mfeng
'''
SITE_URL='www.bjhwtb.com'

# product catalog


# pc style color
PC_STYLE_COLOR=6

class QQ:
    def __init__(self, number, name):
        self.number = number
        self.name = name
#online servers
class Online_servers:
    def __init__(self):
        self.serverlistp='left'
        self.template = 'www/servers_metro_color.html'
        self.qqlist = [QQ(94096251, 'ming'),QQ(87125162, 'feng')]
        #self.weixin_pic=""
        #self.wangwang=""
        #self.ali=""
        #self.skype=""
        self.tel = '010-1234567'
        if self.serverlistp =='right':
            self.servers_serverlistpcss='left'
            self.servers_float = 'right:0;'
            self.servers_float1 = 'left:-160px;'
        elif self.serverlistp =='left':
            self.servers_serverlistpcss='right'
            self.servers_float = 'left:0;'
            self.servers_float1 = 'right:-160px;'
        else:
            self._serverlistpcss ='left'

#map position
class BMap:
    def __init__(self):
        self.ditu_center_left = 116.4
        self.ditu_center_right = 40
        self.ditu_level = 12
        self.ditu_maker_left = 116
        self.ditu_maker_right = 40
        

