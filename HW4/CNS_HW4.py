# -*- coding: utf-8 -*-
"""
Created on Thu May 20 21:40:17 2021

@author: M Sabbagh
"""


def binexpansion(x):
    b = []
    c = [0]
    while x > 0:
        c[0] = x % 2
        b = c + b 
        x = x// 2
    return b


def modexp(a,b,n):
    b = binexpansion(b)
    f = 1
    for bit in (b):
        f = f * f % n
        if bit == 1:
            f = f * a % n
    return f

N = 31189420800514467447616631563
e = 2887920783636036798964123603   
M = 711
print('Message =', M, '\nCipher text =', modexp(M,e,N))      

