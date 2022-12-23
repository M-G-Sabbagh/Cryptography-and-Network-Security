# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 21:36:13 2021

@author: User
"""

from hashlib import sha256
import random

iteration = 10000
m = [0] * iteration

for k in range(0, iteration):
    seen = {}
    i = 1
    while True:
        
        rint = random.randint(0, 2**27 - 1)
        
        rbyte = rint.to_bytes(4, byteorder='big')
    
        y = sha256(rbyte).hexdigest()
    
        h = y[59:65]
        
        if h in seen:
            m[k] = i
            break
        
        else:
            seen[h] = i
            i = i + 1
            
ave = sum(m)/len(m)      
print(ave)

