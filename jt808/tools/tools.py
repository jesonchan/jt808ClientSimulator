import binascii
import os
import time


class Tools:

    # 字符串转16进制
    def StrToHex(self, tempStr):
        s = ''
        for each in tempStr:
            s += hex(ord(each))[2:]
        return s.upper()

    # 16进制转8位的2进制
    def HexStrTo8Bin1(self, tempHex):
        res = ''
        for each in bytes.fromhex(tempHex):
            sBin = bin(each)[2:]
            eightNum = 8 - len(sBin)
            if (0 != eightNum):
                sBin = eightNum * '0' + sBin
            res += sBin
        return res

    # 整形转16进制，缺位补0
    def IntToHex(self, tempInt, digit):
        if tempInt >= 0:
            sHex = hex(tempInt)[2:]
            num = digit - len(sHex)
            if (0 != num):
                sHex = num * '0' + sHex
        else:
            sHex = hex(tempInt & 0xFFFF)[2:]
        return sHex

    # 中文转16进制
    def ChrToHex(self, tempChr):
        sHex = str(binascii.b2a_hex(tempChr.encode('gbk')))[2:-1].upper()
        return sHex

    # 16进制转中文
    def HexToChr(self, tempHex):
        chr = binascii.a2b_hex(tempHex).decode('gbk')
        return chr

    # bytes转16进制
    def ByteToHex(self, bins):
        return ''.join(["%02X" % x for x in bins]).strip()

    # image转16进制

    def ImageToHex(self, filepath):
        file = filepath
        with open(file, 'rb') as f:
            content = f.read()
        sBin = binascii.hexlify(content)
        sHex = str(sBin)[2:-1]
        return sHex

    # 返回字节流的十六进制字节流
    def BinToHex(self, content):
        sBin = binascii.hexlify(content)
        sHex = str(sBin)[2:-1]
        return sHex

    # 获取文件大小，转16进制

    def getDocSizeToHex(self, filepath):
        size = os.path.getsize(filepath)  # 获取文件大小
        sHex = hex(size)[2:]
        return sHex

    # 获取文件名称，转16进制
    def getDocNameToHex(self, filepath):
        filename = os.path.basename(filepath)  # 获取文件路径，文件名称
        # file_base = filename.split('.')[0]
        # file_type = filename.split('.')[1]
        # # print(file_base, file_type)
        # localtime = time.strftime("%y%m%d%H%M%S", time.localtime())
        # filename_time = file_base + localtime + '.' + file_type
        # print(filename_time)
        sHex = self.StrToHex(filename)
        return sHex

    # 16进制转字符串
    def HexToStr(self, tempHex):
        content = binascii.a2b_hex(tempHex).decode("utf8")
        return content

    # print(bytes(b'~\x81\x00\x00\t\x01Rpa\x11\x11$c\x00\x01\x00vmsgps\x80~').decode('ascii'))


if __name__ == '__main__':
    t = Tools()
    print(t.ImageToHex('../../attachment/52204.jpg'))
    print(t.getDocSizeToHex('../../attachment/52204.jpg'))
    print(t.getDocNameToHex('../../attachment/52204.jpg'))
    print(t.HexToStr("35323230342E6A7067"))
    num = -55
    print(t.IntToHex(num, 8))
    print(t.ChrToHex('浙'))
    print(t.HexToChr('B2E2CAD4'))


