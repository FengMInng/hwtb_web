'''
Created on Jun 27, 2016

@author: mfeng
'''
import math
def mean(l):
    m = .0
    for i in l:
        m+=i
    
    return m/len(l)

def variance(l):
    m = mean(l)
    a = 0
    for i in l:
        a += (i-m)**2
    return a/len(l)

def std_var(l):
    var = variance(l)
    return math.sqrt(var)