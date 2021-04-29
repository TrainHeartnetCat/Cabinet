#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils import *
import random

class AESInputError(Exception):
    pass

class AESPaddingError(Exception):
    pass

class AESDataError(Exception):
    pass


class AES:
    def __init__(self, keylen, key=None):

        self.keylen = keylen
        self.key = key

        if key == None: #random.randrange(0,0,1)
            if  keylen == 128 or keylen == 192 or keylen == 256:
                key = random.randrange(0,2**keylen,1)
                self.genekey = key
            else:
                raise AESInputError
            

        if (type(keylen) != int):
            raise AESInputError

        if keylen == 128 or keylen == 192 or keylen == 256:
            pass
        else:
            raise AESInputError

        if (type(key) != int) or (key < 0) or (key >= 2**keylen):#应该不用写范围? cannot fit in `keylen` bits?
            raise AESInputError

        self.lb = list(key.to_bytes(int(keylen/8), 'big'))
        self.keymatrix = matrix_of_key(self.lb,keylen)#128位密钥的4x4矩阵，如果密钥长度大于128位，我知道依然是分割成4*4，但剩下的部分要怎么加密？
        self.exkey = key_expansion(self.keymatrix,keylen)



    def enc(self, msg):#key矩阵：self.keymatrix，msg矩阵：self.msgmatrix
        self.msg = msg

        if (type(self.msg) != int) or (self.msg < 0) or (self.msg >= 2**128):
            raise AESInputError

        self.lm = list(msg.to_bytes(16, 'big'))
        self.msgmatrix = matrix_of_plaintxt(self.lm)#128位明文的4x4矩阵
        if self.keylen == 128:
            n = 0
            a = AddRoundKey(self.msgmatrix,key_take(self.exkey,n))
            while n != 9:
                n = n + 1
                a = byte_subdtitution(a)
                a = row_shift(a)
                a = mix_column(a)
                a = AddRoundKey(a,key_take(self.exkey,n))
            a = byte_subdtitution(a)
            a = row_shift(a)
            a = AddRoundKey(a,key_take(self.exkey,n+1))
            l = []
            for i in range(len(a)):
                l.append(a[0][i])
                l.append(a[1][i])
                l.append(a[2][i])
                l.append(a[3][i])
            b = bytes(l)
            x = int.from_bytes(b, 'big')
            return x
        if self.keylen == 192:#再de吧，应该KE有问题吧
            n = 0
            a = AddRoundKey(self.msgmatrix,key_take(self.exkey,n))
            while n != 11:
                n = n + 1
                a = byte_subdtitution(a)
                a = row_shift(a)
                a = mix_column(a)
                a = AddRoundKey(a,key_take(self.exkey,n))
            a = byte_subdtitution(a)
            a = row_shift(a)
            a = AddRoundKey(a,key_take(self.exkey,n+1))
            l = []
            for i in range(len(a)):
                l.append(a[0][i])
                l.append(a[1][i])
                l.append(a[2][i])
                l.append(a[3][i])
            b = bytes(l)
            x = int.from_bytes(b, 'big') 
            return x
        if self.keylen == 256:
            n = 0
            a = AddRoundKey(self.msgmatrix,key_take(self.exkey,n))
            while n != 13:
                n = n + 1
                a = byte_subdtitution(a)
                a = row_shift(a)
                a = mix_column(a)
                a = AddRoundKey(a,key_take(self.exkey,n))
            a = byte_subdtitution(a)
            a = row_shift(a)
            a = AddRoundKey(a,key_take(self.exkey,n+1))
            l = []
            for i in range(len(a)):
                l.append(a[0][i])
                l.append(a[1][i])
                l.append(a[2][i])
                l.append(a[3][i])
            b = bytes(l)
            x = int.from_bytes(b, 'big')
            return x

    def dec(self, ciph):#将ciphanw 解密回msg
        self.ciph = ciph

        if (type(self.ciph) != int) or (self.ciph < 0) or (self.ciph >= 2**128):
            raise AESInputError

        self.lc = list(ciph.to_bytes(16, 'big'))
        self.ciphmatrix = matrix_of_ciph(self.lc)
        if self.keylen == 128:
            n = 10
            a = AddRoundKey(self.ciphmatrix,key_take(self.exkey,n))#
            while n != 1:
                n = n - 1
                a = R_row_shift(a)
                a = R_byte_subdtitution(a)     
                a = AddRoundKey(a,key_take(self.exkey,n))
                a = R_mix_column(a)#
            a = R_row_shift(a)
            a = R_byte_subdtitution(a)
            a = AddRoundKey(a,key_take(self.exkey,n-1))
            l = []
            for i in range(len(a)):
                l.append(a[0][i])
                l.append(a[1][i])
                l.append(a[2][i])
                l.append(a[3][i])
            b = bytes(l)
            x = int.from_bytes(b, 'big')
            return x
        if self.keylen == 192:
            n = 12
            a = AddRoundKey(self.ciphmatrix,key_take(self.exkey,n))#
            while n != 1:
                n = n - 1
                a = R_row_shift(a)
                a = R_byte_subdtitution(a)     
                a = AddRoundKey(a,key_take(self.exkey,n))
                a = R_mix_column(a)#
            a = R_row_shift(a)
            a = R_byte_subdtitution(a)
            a = AddRoundKey(a,key_take(self.exkey,n-1))
            l = []
            for i in range(len(a)):
                l.append(a[0][i])
                l.append(a[1][i])
                l.append(a[2][i])
                l.append(a[3][i])
            b = bytes(l)
            x = int.from_bytes(b, 'big')
            return x
        if self.keylen == 256: 
            n = 14
            a = AddRoundKey(self.ciphmatrix,key_take(self.exkey,n))#
            while n != 1:
                n = n - 1
                a = R_row_shift(a)
                a = R_byte_subdtitution(a)     
                a = AddRoundKey(a,key_take(self.exkey,n))
                a = R_mix_column(a)#
            a = R_row_shift(a)
            a = R_byte_subdtitution(a)
            a = AddRoundKey(a,key_take(self.exkey,n-1))
            l = []
            for i in range(len(a)):
                l.append(a[0][i])
                l.append(a[1][i])
                l.append(a[2][i])
                l.append(a[3][i])
            b = bytes(l)
            x = int.from_bytes(b, 'big')
            return x
    def getkey(self):
        return self.genekey

class AESCBC(AES):
    def encfile(self, infile, outfile, iv=0, pad=True):
        if (type(infile) != str):
            raise AESInputError

        if (type(outfile) != str):
            raise AESInputError

        if (type(iv) != int) or (iv < 0) or (iv >= 2**128):
            raise AESInputError

        if (type(pad) != bool):
            raise AESInputError



        with open(infile, 'rb') as infi:
            inbytes = infi.read()


        if inbytes == b'': #ok
            linb = list(inbytes)
            if pad == True:
                for i in range(16):
                    linb.append(16)

                m  = int(len(linb)/16)
                planlist = []
                for i in range(m): #m=0~14
                    planlist.append(linb[i*16:(i+1)*16])

                finallist = []
                n = -1
                while n != (len(planlist) - 1):
                    n = n + 1
                    b = bytes(planlist[n])
                    b = int.from_bytes(b, 'big')^iv
                    a = self.enc(b)
                    iv = a
                    workinglist = list(a.to_bytes(16, 'big'))
                    finallist.extend(workinglist)
                outbytes = bytes(finallist)

            if pad == False: #ok
                if len(inbytes)%16 != 0:
                    raise AESPaddingError
                if len(inbytes)%16 == 0:
                    outbytes = inbytes

            

        if inbytes != b'':
            linb = list(inbytes)
            if pad == True:#然后pad  #pad value = 16 - len(inbytes)%16, 关键是怎么pad，我觉得直接list append就好了，还是得分开一下
                if len(inbytes) % 16 == 0:
                    for i in range(16):
                        linb.append(16)
                else:
                    for i in range(16 - (len(inbytes) % 16)):
                        linb.append(16 - (len(inbytes) % 16))

                m  = int(len(linb)/16)
                planlist = []
                for i in range(m): #m=0~14
                    planlist.append(linb[i*16:(i+1)*16])      

                finallist = []
                n = -1
                while n != (len(planlist) - 1):
                    n = n + 1
                    b = bytes(planlist[n])
                    b = int.from_bytes(b, 'big')^iv
                    a = self.enc(b)
                    iv = a
                    workinglist = list(a.to_bytes(16, 'big'))
                    finallist.extend(workinglist)
                outbytes = bytes(finallist)


            if pad == False:
                if len(inbytes) % 16 != 0:
                    raise AESPaddingError 

                if len(inbytes) % 16 == 0:
                    m  = int(len(linb)/16)
                    planlist = []
                    for i in range(m): #m=0~14
                        planlist.append(linb[i*16:(i+1)*16])      

                    finallist = []
                    ans = []
                    n = -1
                    while n != (len(planlist) - 1):
                        n = n + 1
                        b = bytes(planlist[n])
                        b = int.from_bytes(b, 'big')^iv
                        a = self.enc(b)
                        iv = a
                        workinglist = list(a.to_bytes(16, 'big'))
                        finallist.extend(workinglist)
                    outbytes = bytes(finallist)

        with open(outfile, 'wb') as outfi:
            outfi.write(outbytes)

    def decfile(self, infile, outfile, iv=0, pad=True):
        if (type(infile) != str):
            raise AESInputError

        if (type(outfile) != str):
            raise AESInputError

        if (type(iv) != int) or (iv < 0) or (iv >= 2**128):
            raise AESInputError

        if (type(pad) != bool):
            raise AESInputError

        with open(infile, 'rb') as infi:
            inbytes = infi.read()

        if inbytes == b'':
            if len(inbytes) % 16 != 0:
                raise AESDataError
            if len(inbytes) % 16 == 0:                
                if pad == True:
                    raise AESPaddingError
                
                if pad == False:
                    outbytes = inbytes

        if inbytes != b'':
            if len(inbytes) % 16 != 0:
                raise AESDataError

            if len(inbytes) % 16 == 0:
                linb = list(inbytes)
                m  = int(len(linb)/16)
                ciphlist = []
                for i in range(m): #m=0~14
                    ciphlist.append(linb[i*16:(i+1)*16])
                ans = []
                n = -1
                while n != (len(ciphlist) - 1):
                    n = n + 1
                    b = bytes(ciphlist[n])
                    b = int.from_bytes(b, 'big')
                    a = self.dec(b)
                    a = a^iv
                    iv = b            
                    workinglist = list(a.to_bytes(16, 'big'))
                    ans.extend(workinglist)



            #关于pad，我怎么知道原文是一个31位，pad后变成32位，还是一个本身就是32位，末尾为x01的数？
            #不可能31位，必定偶数
            #如果末尾是x01/x02,我怎么知道是pad错误，还是原本长度就是这样
            #先假设不会发生这样的情况吧
            #去除pad 包含三部分 验证尾数是否是pad，pad正确性，去除pad

            if pad == True:
                if pad_jude(ans) == False:
                    raise AESPaddingError

                if pad_jude(ans) == True:
                    for i in range(ans[-1]):
                        ans.pop()

            if pad == False:
                pass


            outbytes = bytes(ans)

        with open(outfile, 'wb') as outfi:
            outfi.write(outbytes)

def test():
    key = 0x2b7e151628aed2a6abf7158809cf4f3c
    msg = 0x3243f6a8885a308d313198a2e0370734
    ciph_ans = 0x3925841d02dc09fbdc118597196a0b32#
    aes = AES(128, key)
    ciph = aes.enc(msg)
    assert ciph == ciph_ans
    msg2 = aes.dec(ciph)
    assert msg == msg2#

    key = 0x000102030405060708090a0b0c0d0e0f1011121314151617
    msg = 0x00112233445566778899aabbccddeeff
    ciph_ans = 0xdda97ca4864cdfe06eaf70a0ec0d7191#
    aes = AES(192, key)
    ciph = aes.enc(msg)
    assert ciph == ciph_ans
    msg2 = aes.dec(ciph)
    assert msg == msg2#

    key = 0x000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f
    msg = 0x00112233445566778899aabbccddeeff
    ciph_ans = 0x8ea2b7ca516745bfeafc49904b496089#
    aes = AES(256, key)
    ciph = aes.enc(msg)
    assert ciph == ciph_ans
    msg2 = aes.dec(ciph)
    assert msg == msg2

def test2():
    msg_file = 'file.m'
    ciph_file = 'file.c'
    msg2_file = 'file2.m'
    key = 0x2b7e151628aed2a6abf7158809cf4f3c
    msg = 0x3243f6a8885a308d313198a2e0370734face
    ciph_ans = 0x3925841d02dc09fbdc118597196a0b32f4a3358aa7c61ced508f3435fe67f854#
    aes = AESCBC(128, key)
    with open(msg_file, 'wb') as f:
        f.write(msg.to_bytes(18, 'big'))#
    aes.encfile(msg_file, ciph_file)
    with open(ciph_file, 'rb') as f:
        ciph = int.from_bytes(f.read(), 'big')
    assert ciph == ciph_ans#
    aes.decfile(ciph_file, msg2_file)
    with open(msg2_file, 'rb') as f:
        msg2 = int.from_bytes(f.read(), 'big')
    assert msg == msg2#

#    msg_file = 'file.m'
#    ciph_file = 'file.c'
#    msg2_file = 'file2.m'
#    key = 0x000102030405060708090a0b0c0d0e0f1011121314151617
#    msg = 0x3243f6a8885a308d313198a2e0370734face
#    ciph_ans = 85138470862944168965410964486563953865929508384769408676084492330778758202697
#    aes = AESCBC(192, key)
#    with open(msg_file, 'wb') as f:
#        f.write(msg.to_bytes(18, 'big'))
#    aes.encfile(msg_file, ciph_file)
#    with open(ciph_file, 'rb') as f:
#        ciph = int.from_bytes(f.read(), 'big')
#    print(ciph)
#    print('a')
#    print(msg)
#    assert ciph == ciph_ans#

#    aes.decfile(ciph_file, msg2_file)
#    with open(msg2_file, 'rb') as f:
#        msg2 = int.from_bytes(f.read(), 'big')
#    assert msg == msg2#

#    msg_file = 'file.m'
#    ciph_file = 'file.c'
#    msg2_file = 'file2.m'
#    key = 0x000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f
#    msg = 0x00112233445566778899aabbccddeeff
#    ciph_ans = 0x8ea2b7ca516745bfeafc49904b496089#
#    aes = AESCBC(256, key)
#    with open(msg_file, 'wb') as f:
#        f.write(msg.to_bytes(18, 'big'))#
#    aes.encfile(msg_file, ciph_file)
#    with open(ciph_file, 'rb') as f:
#        ciph = int.from_bytes(f.read(), 'big')
#    print(ciph)
#    print('a')
#    print(msg)
    #assert ciph == ciph_ans#

#    aes.decfile(ciph_file, msg2_file)
#    with open(msg2_file, 'rb') as f:
#        msg2 = int.from_bytes(f.read(), 'big')
#    assert msg == msg2

#def test3():
#    key = 0x2b7e151628aed2a6abf7158809cf4f3c
#    aes = AESCBC(128, key)
#    with open(r'C:\Users\TrainHeartnetCat\Desktop\msg.txt', 'rb') as f:
#    msg = f.read()#

#    aes.encfile(, r'C:\Users\TrainHeartnetCat\Desktop\ciph.txt')
#    with open(ciph_file, 'rb') as f:
#        ciph = int.from_bytes(f.read(), 'big')
#    assert ciph == ciph_ans#
#    aes.decfile(ciph_file, msg2_file)
#    with open(msg2_file, 'rb') as f:
#        msg2 = int.from_bytes(f.read(), 'big')
#    assert msg == msg2

def test4():
    key = 0x2b7e151628aed2a6abf7158809cf4f3c
    msg = 0x3243f6a8885a308d313198a2e0370734
    ciph_ans = 0x3925841d02dc09fbdc118597196a0b32#
    aes = AES(128, key)
    ciph = aes.enc(msg)
    assert ciph == ciph_ans
    msg2 = aes.dec(ciph)
    assert msg == msg2#
    key = 0x000102030405060708090a0b0c0d0e0f1011121314151617
    msg = 0x00112233445566778899aabbccddeeff
    ciph_ans = 0xdda97ca4864cdfe06eaf70a0ec0d7191#
    aes = AES(192, key)
    ciph = aes.enc(msg)
    assert ciph == ciph_ans
    msg2 = aes.dec(ciph)
    assert msg == msg2#

if __name__ == '__main__':
    test()
    test2()
    #test3()
    #test4()
