from jt808.tools import tools


class ReceiveUploadMsg:
    def __init__(self, message):
        self.msg = message
        self.t = tools.Tools()
        self.content = []

    def explanation(self):
        content_bin = self.t.BinToHex(self.msg)  # 二进制转16进制
        # print(content_bin)
        message_header = content_bin[2:26]  # 消息头
        message_body = content_bin[26:-4]  # 消息体
        self.content = [message_header, message_body]
        msg_ID = message_header[:4]  # 消息ID
        ip_length = message_body[:2]  # 附件服务器 IP 地址长度
        length = int(ip_length, 16)
        hostHex = message_body[2:(2 + length * 2)]  # 附件服务器 IP 地址
        host = self.t.HexToStr(hostHex)
        portHex = message_body[(2 + length * 2):(2 + length * 2 + 4)]  # 附件服务器端口（TCP）
        port = int(portHex, 16)
        alarm_sign = message_body[(2 + length * 2 + 8):(2 + length * 2 + 40)]  # 报警标识号
        print('报警标识号%s' % alarm_sign)
        alarm_code = message_body[(2 + length * 2 + 40):(2 + length * 2 + 104)]  # 报警编号
        print('报警编号%s' % alarm_code)
        print('消息ID: %s IP地址: %s 服务器端口: %s' % (msg_ID, host, port))
        return host, port


if __name__ == '__main__':
    msg1 = b'~\x92\x08\x00S\x013"!!"\x00\x0b\x0e218.108.32.170\x047\x00\x002233200\x19\t\x12\x17\x11\x06\x00\x03\x00\x013"!!"2233200\x19\t\x12\x17\x11\x06\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xe4~'
    rcm = ReceiveUploadMsg(msg1)
    print(rcm.explanation())
    # print(rcm.content)
