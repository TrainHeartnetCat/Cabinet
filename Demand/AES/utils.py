#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# S-Box
S_BOX = (
    [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
    [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
    [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
    [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
    [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
    [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
    [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
    [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
    [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
    [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
    [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
    [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],
    [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
    [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
    [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
    [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]
)

# inverse S-Box
INV_S_BOX = (
    [0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb],
    [0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb],
    [0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e],
    [0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25],
    [0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92],
    [0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84],
    [0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06],
    [0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b],
    [0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73],
    [0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e],
    [0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b],
    [0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4],
    [0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f],
    [0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef],
    [0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61],
    [0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d]
)

# x^(i-1) values for Rcon, starts at 1
RCON_VAL = (None, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36, 0x6c, 0xd8, 0xab, 0x4d, 0x9a, 0x2f)
#print(RCON_VAL)

def byte_mul(a, b):
    ''' Return the multiplication of two bytes `a` and `b`. '''
    res = 0
    while b > 0:
        if b & 1:
            res ^= a
        if a & 0x80:
            a = (a << 1) ^ 0x11b
        else:
            a <<= 1
        b >>= 1
    return res

def matrix_of_plaintxt(lm):
    matrix = [[],[],[],[]]
    for i in range(4):
        for j in range(4):
            matrix[i].append(lm[4*j+i])
    return matrix#已测

def matrix_of_ciph(lc):
    matrix = [[],[],[],[]]
    for i in range(4):
        for j in range(4):
            matrix[i].append(lc[4*j+i])
    return matrix

def matrix_of_key(lb, kl):
    if kl == 128:
        matrix = [[],[],[],[]]
        for i in range(4):
            for j in range(4):
                matrix[i].append(lb[4*j+i])
        return matrix

    if kl == 192:#lb=[00,01,02,03,04,05,06,07,08,09,0a,0b,0c,0d,0e,0f,10,11,12,13,14,15,16,17]
        matrix = [[],[],[],[]]#
        for i in range(4):#[[00, 04, 08, 12, 16, 20], [01, 05, 09, 13, 17, 21], [02, 06, 0a, 14, 18, 22], [03, 07, 0b, 15, 19, 23]]
            for j in range(6):
                matrix[i].append(lb[4*j+i])
        return matrix

    if kl == 256:
        matrix = [[],[],[],[]]
        for i in range(4):
            for j in range(8):
                matrix[i].append(lb[4*j+i])
        return matrix#已测

def byte_subdtitution(msgm1): #字节代还 #已测
    matrix = [[1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4]]
    for i in range(4):
        for j in range(4):
            y = msgm1[i][j]&0x0f
            x = int((msgm1[i][j]&0xf0)/16)
            matrix[i][j] = S_BOX[x][y]    
    return matrix

def byte_subdtitution_single(a): #已测
    y = a&0x0f
    x = int((a&0xf0)/16)
    b = S_BOX[x][y]
    return b

def R_byte_subdtitution(chip1):#逆代换 #已测
    matrix = [[1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4]]
    for i in range(4):
        for j in range(4):
            y = chip1[i][j]&0x0f
            x = int((chip1[i][j]&0xf0)/16)
            matrix[i][j] = INV_S_BOX[x][y]    
    return matrix

def row_shift(msgm2):#行位移
    a = msgm2[1].pop(0)
    msgm2[1].append(a)

    b = msgm2[2].pop(0)
    msgm2[2].append(b)
    c = msgm2[2].pop(0)
    msgm2[2].append(c)

    d = msgm2[3].pop(0)
    msgm2[3].append(d)
    e = msgm2[3].pop(0)
    msgm2[3].append(e)
    f = msgm2[3].pop(0)
    msgm2[3].append(f)

    return msgm2#已测

def R_row_shift(chip2):#行逆位移
    for i in range(1):
        chip2[1].insert(0,chip2[1].pop())

    for i in range(2):
        chip2[2].insert(0,chip2[2].pop())

    for i in range(3):
        chip2[3].insert(0,chip2[3].pop())

    return chip2


def mix_column(msgm3):#列混合 已测试
    matrix = [[1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4]]
    for i in range(4):
        matrix[0][i] = byte_mul(0x02, msgm3[0][i])^byte_mul(0x03, msgm3[1][i])^byte_mul(0x01, msgm3[2][i])^byte_mul(0x01, msgm3[3][i])
        matrix[1][i] = byte_mul(0x01, msgm3[0][i])^byte_mul(0x02, msgm3[1][i])^byte_mul(0x03, msgm3[2][i])^byte_mul(0x01, msgm3[3][i])
        matrix[2][i] = byte_mul(0x01, msgm3[0][i])^byte_mul(0x01, msgm3[1][i])^byte_mul(0x02, msgm3[2][i])^byte_mul(0x03, msgm3[3][i])
        matrix[3][i] = byte_mul(0x03, msgm3[0][i])^byte_mul(0x01, msgm3[1][i])^byte_mul(0x01, msgm3[2][i])^byte_mul(0x02, msgm3[3][i])

    return matrix

def R_mix_column(chip3):#列混合
    matrix = [[1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4]]
    for i in range(4):
        matrix[0][i] = byte_mul(0x0E, chip3[0][i])^byte_mul(0x0B, chip3[1][i])^byte_mul(0x0D, chip3[2][i])^byte_mul(0x09, chip3[3][i])
        matrix[1][i] = byte_mul(0x09, chip3[0][i])^byte_mul(0x0E, chip3[1][i])^byte_mul(0x0B, chip3[2][i])^byte_mul(0x0D, chip3[3][i])
        matrix[2][i] = byte_mul(0x0D, chip3[0][i])^byte_mul(0x09, chip3[1][i])^byte_mul(0x0E, chip3[2][i])^byte_mul(0x0B, chip3[3][i])
        matrix[3][i] = byte_mul(0x0B, chip3[0][i])^byte_mul(0x0D, chip3[1][i])^byte_mul(0x09, chip3[2][i])^byte_mul(0x0E, chip3[3][i])

    return matrix

def AddRoundKey(msorci,key):#轮密钥加,已测
    matrix = [[1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4]]
    for i in range(4):
        matrix[0][i] = msorci[0][i]^key[0][i]
        matrix[1][i] = msorci[1][i]^key[1][i]
        matrix[2][i] = msorci[2][i]^key[2][i]
        matrix[3][i] = msorci[3][i]^key[3][i]
    return matrix

def key_expansion(key,keylen):#这部分没问题
    if keylen == 128:
        for i in range(4,44):
            if i % 4 != 0:
                a = key[0][i-4]^key[0][i-1]
                key[0].append(a)
                b = key[1][i-4]^key[1][i-1]
                key[1].append(b)
                c = key[2][i-4]^key[2][i-1]
                key[2].append(c)
                d = key[3][i-4]^key[3][i-1]
                key[3].append(d)
            if i % 4 == 0:
                a = key[0][i-4]^(byte_subdtitution_single(key[1][i-1])^RCON_VAL[int(i/4)])
                key[0].append(a)
                b = key[1][i-4]^byte_subdtitution_single(key[2][i-1])
                key[1].append(b)
                c = key[2][i-4]^byte_subdtitution_single(key[3][i-1])
                key[2].append(c)
                d = key[3][i-4]^byte_subdtitution_single(key[0][i-1])       
                key[3].append(d)
        return key
    if keylen == 192:
        for i in range(6,52):
            if i % 6 != 0:
                a = key[0][i-6]^key[0][i-1]
                key[0].append(a)
                b = key[1][i-6]^key[1][i-1]
                key[1].append(b)
                c = key[2][i-6]^key[2][i-1]
                key[2].append(c)
                d = key[3][i-6]^key[3][i-1]
                key[3].append(d)
            if i % 6 == 0:
                a = key[0][i-6]^(byte_subdtitution_single(key[1][i-1])^RCON_VAL[int(i/6)])
                key[0].append(a)
                b = key[1][i-6]^byte_subdtitution_single(key[2][i-1])
                key[1].append(b)
                c = key[2][i-6]^byte_subdtitution_single(key[3][i-1])
                key[2].append(c)
                d = key[3][i-6]^byte_subdtitution_single(key[0][i-1])       
                key[3].append(d)
        return key
    if keylen == 256:# If Nk=8 and i−4i-4i−4 is a multiple of Nk, then SubWord() is applied to w[i−1]w[i-1]w[i−1] prior to the XOR.
        for i in range(8,60):
            if i % 8 == 0:
                a = key[0][i-8]^(byte_subdtitution_single(key[1][i-1])^RCON_VAL[int(i/8)])
                key[0].append(a)
                b = key[1][i-8]^byte_subdtitution_single(key[2][i-1])
                key[1].append(b)
                c = key[2][i-8]^byte_subdtitution_single(key[3][i-1])
                key[2].append(c)
                d = key[3][i-8]^byte_subdtitution_single(key[0][i-1]) 
                key[3].append(d)
            elif i % 8 == 4:
                a = key[0][i-8]^byte_subdtitution_single(key[0][i-1])
                key[0].append(a)
                b = key[1][i-8]^byte_subdtitution_single(key[1][i-1])
                key[1].append(b)
                c = key[2][i-8]^byte_subdtitution_single(key[2][i-1])
                key[2].append(c)
                d = key[3][i-8]^byte_subdtitution_single(key[3][i-1])
                key[3].append(d)
            else:
                a = key[0][i-8]^key[0][i-1]
                key[0].append(a)
                b = key[1][i-8]^key[1][i-1]
                key[1].append(b)
                c = key[2][i-8]^key[2][i-1]
                key[2].append(c)
                d = key[3][i-8]^key[3][i-1]
                key[3].append(d)
        return key

def key_take(exkey,n):
    matrix = [[],[],[],[]]
    for i in range(4):
        matrix[0].append(exkey[0][4*n+i])
        matrix[1].append(exkey[1][4*n+i])
        matrix[2].append(exkey[2][4*n+i])
        matrix[3].append(exkey[3][4*n+i])
    return matrix


def pad_jude(list1): #a是final
    list2 = []
    if list1[-1] > 16:
        return False

    if list1 == []:
        return False
    if list1[-1] == 1:
        if list1[-2] == 1:
            return False
        else:
            return True
    if list1[-1] != 1:
        if list1[-1-list1[-1]] == list1[-1]:
            return False
        else:
            for i in range(list1[-1]):
                if list1[-1-i] == list1[-1]:
                    list2.append(1)
            if list2 == [1]*list1[-1]:
                return True
            else:
                return False

