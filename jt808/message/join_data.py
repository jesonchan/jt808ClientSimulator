from jt808.tools import tools


class JoinData:
    def __init__(self, sim):
        self.t = tools.Tools()
        if 12 == len(sim):
            self.sim = sim
        else:
            self.sim = '0' + sim

    # 完整拼报 = 消息头 + 内容包 + 尾部校验

    def getFullData(self, iID, bodyData):
        # self.dataHead = self.setHead_Data(iID)
        self.dataHead = self.setHead_Data(iID, bodyData)
        print('消息头 ', self.dataHead)
        self.dataBody = bodyData
        print('内容包', self.dataBody)
        self.dataTail = self.setTail_Data(self.dataHead, self.dataBody)
        formatData = (
                             self.dataHead +
                             self.dataBody +
                             self.dataTail).upper()[
                     2:-
                     2]
        # formatData = formatData.replace('7D', '7D01')
        # formatData = formatData.replace('7E', '7D02')
        # Hex 转 Byte
        formatDataBin = bytes.fromhex(formatData)
        # Byte替换, 先将字节 7E 替换成 7D02, 再将字节7D 替换成 7D01
        # 7D BYTE类型 为 b'}', 7E BYTE类型 为 b'~'
        ReplaceData = formatDataBin.replace(b'}',b'}\x02')
        formatData = ReplaceData.replace(b'~',b'}\x01')
        # Byte 转 Hex
        formatData = bytes.hex(formatData)
        fullData = '7E' + formatData + '7E'
        return fullData

    # 设置消息头
    # def setHead_Data(self, iID):
    def setHead_Data(self, iID, bodyData):
        self.info_Head = '7E'
        self.info_ID = iID  # 数据类型WORD
        self.info_Attribute = self.head_attribute(bodyData)  # 16字节   数据类型WORD
        self.info_SIM = self.sim
        self.info_Serial = '0000'  # 数据类型WORD
        self.dataHead = self.info_Head + self.info_ID + \
                        self.info_Attribute + self.info_SIM + self.info_Serial
        return self.dataHead

    # 消息体属性
    def head_attribute(self, bodyData):
        attribute_h1 = '00'  # 保留 分包 数据加密方式
        attribute_body_len = int(len(bodyData) / 2)
        # print('消息体长度 ', attribute_body_len)
        attribute_body_len_sHex = self.t.IntToHex(attribute_body_len, 2)
        attribute = attribute_h1 + attribute_body_len_sHex
        # print('消息体属性 ', attribute)
        return attribute

    # 设置消息尾

    def setTail_Data(self, dataHead, dataBody):
        self.calc = dataHead + dataBody
        self.code = self.checksum(self.calc)
        return self.code + '7E'

    # 尾部计算校验
    def checksum(self, dataStr):
        res = 0
        index = 0
        list1 = []
        for each in bytes.fromhex(dataStr)[1:]:
            index += 1
            list1.append(each)

        for each in list1:
            # print('res = {}, each = {}'.format(res, each))
            if index == 0:
                res = each
            else:
                res = res ^ each

        res = hex(res)[2:]

        if 1 == len(res):
            res = '0' + res

        return res


if __name__ == '__main__':
    hex0 = '7E7E7D 7D01 7D02 77D1'
    bin = bytes.fromhex(hex0)
    print(bin)
    print(bytes.hex(bin))
    fmt = bin.replace(b'}',b'}\x02')
    fmt = fmt.replace(b'~',b'}\x01')
    print(fmt)
    print(bytes.hex(fmt))


