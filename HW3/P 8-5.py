# -*- coding: utf-8 -*-
"""
Created on Tue May 11 01:35:39 2021

@author: M Sabbagh
"""

import random
import sys
import math

def gcd(x,y):
    
    if x == y:
        return abs(x)
    if x == 0:
        return abs(y)
    if y == 0:
        return abs(x)
    if abs(x) > abs(y):
        a = x
        b = y
    else:
        a = y
        b = x
    
   
    while True:
        r = a % b
        a = b
        b = r
        if r == 0:
            break
    return a

c = 0
iteration = 10000

for i in range(iteration):
    x = random.randint(0, sys.maxsize)
    y = random.randint(0, sys.maxsize)
    if gcd(x,y) == 1:
        c = c + 1

pi = math.sqrt(6 * iteration / c) 
print('pi =', pi)
    
    
        