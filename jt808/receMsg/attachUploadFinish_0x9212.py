from jt808.tools import tools


class ReceiveUploadFinishMsg:
    def __init__(self, message):
        self.msg = message
        self.t = tools.Tools()
        self.content = []
        self.result = []  # 消息结果

    def explanation(self):
        content_bin = self.t.BinToHex(self.msg)  # 二进制转16进制
        # print(content_bin)
        message_header = content_bin[2:26]  # 消息头
        message_body = content_bin[26:-4]  # 消息体
        self.content = [message_header, message_body]
        msg_ID = message_header[:4]  # 消息ID
        name_length = int(message_body[:2], 16)  # 文件名称长度
        file_name_hex = message_body[2:(name_length * 2 + 2)]  # 文件名称
        file_name = self.t.HexToStr(file_name_hex)
        file_type = message_body[(name_length * 2 + 2)
                                  :(name_length * 2 + 4)]  # 文件类型
        msg_result = message_body[(name_length * 2 + 4):(name_length * 2 + 6)]
        self.result.append(int(msg_result))
        print(
            '消息ID: %s 文件名称: %s  文件类型: %s 应答结果：%s' %
            (msg_ID,
             file_name,
             file_type,
             self.answer_result(
                 int(msg_result))))
        if int(msg_result) != 0:  # 需要补传
            supple = message_body[(name_length * 2 + 6):]
            data_offset = supple[:8]  # 数据偏移量
            data_length = supple[8:]  # 数据长度
            self.result.append([data_offset, data_length])
        return self.result

    def answer_result(self, num):
        reason_dict = {0: '完成', 1: '需要补传'}
        return reason_dict[num]


if __name__ == '__main__':
    msg0 = b'~\x92\x12\x00\r\x013"!!"\x00\x04\t52204.jpg\x00\x00\x00\xd0~'
    rcm = ReceiveUploadFinishMsg(msg0)
    print(rcm.explanation())
    print(rcm.content)
