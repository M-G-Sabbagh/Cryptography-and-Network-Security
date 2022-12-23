# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 19:03:21 2021

@author: M Sabbagh
"""

import numpy as np

alphabet = 'abcdefghijklmnopqrstuvwxyz'

relative_freq = [8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.996, 0.153, 
                 0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056,
                 2.758, 0.978, 2.360, 0.150, 1.974, 0.074]

relative_freq = np.array(relative_freq)


def lett_to_num(letter):
    
    """ a ---> 0, ..., z ---> 25 """
    letternumber = ord(letter) - ord(alphabet[0])
    return letternumber

def num_to_lett(number):
    """ 0 ---> a, ..., 25 ---> z """
    number = number % len(alphabet) 
    number = number + ord(alphabet[0]) 
    return chr(number) 

def shift(letter, key):
    
    number = lett_to_num(letter)
    number = number + key  
    return num_to_lett(number)  

def decryption(message, key):
    decrypted = ''

    for letter in message: 
        if letter in alphabet:  
                letter = shift(letter, key)  
        decrypted += letter  

    return decrypted

def count(message):
    
    counter = np.zeros(len(alphabet))
    freq = np.zeros(len(alphabet))
    c = 0
    
    for letter in message:
        if letter in alphabet:
            lnum = lett_to_num(letter)
            counter[lnum] = counter[lnum] + 1
            c = c + 1
            
    
    return c, counter

def rotate_r(arr, k):
    
    for i in range(k):
        last = arr[len(arr) - 1]
        for j in range(len(arr) - 1, -1, -1):
            arr[j] = arr[j -1]
        arr[0] = last
    
    return arr


message = """qv kzgxbwozixpg, i kimaiz kqxpmz, itaw svwev ia kimaiz'a kqxpmz, bpm apqnb kqxpmz, kimaiz'a kwlm wz kimaiz apqnb, qa wvm wn bpm aquxtmab ivl uwab eqlmtg svwev mvkzgxbqwv bmkpvqycma. 
qb qa i bgxm wn acjabqbcbqwv kqxpmz qv epqkp mikp tmbbmz qv bpm xtiqvbmfb qa zmxtikml jg i tmbbmz awum nqfml vcujmz wn xwaqbqwva lwev bpm itxpijmb.
nwz mfiuxtm, eqbp i tmnb apqnb wn 3, l ewctl jm zmxtikml jg i, m ewctl jmkwum j, ivl aw wv. bpm umbpwl qa viuml inbmz rctqca kimaiz, epw caml qb qv pqa xzqdibm kwzzmaxwvlmvkm.
"""



[c, counter] = count(message)

corr = np.zeros(26)
store = np.zeros(26)

temp1 = 0
temp2 = 0
temp3 = 0
key1 = 0
key2 = 0
key3 = 0

for k in range(26):
    
    corr[k] = np.dot(relative_freq, rotate_r(counter*100/c, k))
    store[k] = corr[k]
    
    if corr[k] > temp1:
        temp1 = corr[k]
        key1 = k
        
store[key1] = 0

for k in range(26):
    if store[k] > temp2:
        temp2 = corr[k]
        key2 = k
        
store[key2] = 0

for k in range(26):
    if store[k] > temp3:
        temp3 = corr[k]
        key3 = k
        
print('Cipher text:', message)

print('key1 =', key1, 'key2 =', key2, 'key3 =', key3)


print('Decrypted text with key1:', decryption(message, key1)) 
print('Decrypted text with key2:', decryption(message, key2) ) 
print('Decrypted text with key3:', decryption(message, key3) ) 



    
