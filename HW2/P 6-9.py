# -*- coding: utf-8 -*-
"""
Created on Wed May  5 14:53:08 2021

@author: M Sabbagh
"""

import numpy as np

def mul_GF(b,a):
    a = int.from_bytes(a, 'big')
    if b == 1:
        return a
    tmp = (a<<1) & 0xff
    if b == 2:
        return tmp if a < 127 else tmp^0x1b
    if b == 3:
        return tmp^a if a < 127 else (tmp^0x1b)^a
    
MixCol = np.array([[2, 3, 1, 1],
                   [1, 2, 3, 1],
                   [1, 1, 2, 3,],
                   [3, 1, 1, 2]])

S1_column1 = np.array([['A1'],
                      ['B2'],
                      ['C3'],
                      ['D4']])

S1_bin = np.array([[bytes.fromhex('A1')],
                      [bytes.fromhex('B2')],
                      [bytes.fromhex('C3')],
                      [bytes.fromhex('D4')]])

out1 = np.zeros((4, S1_column1.shape[1]))

for i in range(S1_column1.shape[0]):
    for j in range(S1_column1.shape[1]):
        
         out1[i][j] = mul_GF(MixCol[i][0], S1_bin[0][j]) ^ mul_GF(MixCol[i][1], S1_bin[1][j]) ^ mul_GF(MixCol[i][2], S1_bin[2][j]) ^ mul_GF(MixCol[i][3], S1_bin[3][j])

S2_column1 = np.array([['A3'],
                      ['B2'],
                      ['C3'],
                      ['D4']])

S2_bin = np.array([[bytes.fromhex('A3')],
                      [bytes.fromhex('B2')],
                      [bytes.fromhex('C3')],
                      [bytes.fromhex('D4')]])

out2 = np.zeros((4, S2_column1.shape[1]))

for i in range(S2_column1.shape[0]):
    for j in range(S2_column1.shape[1]):
        
         out2[i][j] = mul_GF(MixCol[i][0], S2_bin[0][j]) ^ mul_GF(MixCol[i][1], S2_bin[1][j]) ^ mul_GF(MixCol[i][2], S2_bin[2][j]) ^ mul_GF(MixCol[i][3], S2_bin[3][j])

m0 = int(out1[0][0]) ^ int(out2[0][0])
m1 = int(out1[1][0]) ^ int(out2[1][0])
m2 = int(out1[2][0]) ^ int(out2[2][0])
m3 = int(out1[3][0]) ^ int(out2[3][0])

s0 = '{0:08b}'.format(m0)
s1 = '{0:08b}'.format(m1)
s2 = '{0:08b}'.format(m2)
s3 = '{0:08b}'.format(m3)
s = s0 + s1 + s2 + s3

C = 0

for i in range(32):
    if s[i] == '1':
        C = C + 1
    
print('MixColumn =\n',MixCol)
print('state matrix 1\n =', S1_column1)
print('integer format of output 1 =\n', out1)
print('state matrix 2 =\n', S2_column1)
print('integer format of output 1 =\n', out2)
print('changed bits:', s0, s1, s2, s3)
print('#changed bits =', C)

