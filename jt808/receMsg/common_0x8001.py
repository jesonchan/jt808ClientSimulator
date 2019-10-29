from jt808.tools import tools


class ReceiveCommonMsg:
    def __init__(self, message):
        self.msg = message
        self.t = tools.Tools()
        self.content = []

    def explanation(self):
        content_bin = self.t.BinToHex(self.msg)  # 二进制转16进制
        # print(content_bin)
        message_header = content_bin[2:26]  # 消息头
        message_body = content_bin[26:36]  # 消息体
        self.content = [message_header, message_body]
        msg_ID = message_header[:4]  # 消息ID
        rece_ID = message_body[4:8]  # 应答ID
        print(message_body)
        msg_result = message_body[8:10]  # 应答结果
        print(msg_result)
        print('消息ID: %s 应答ID: %s 应答结果：%s' %
              (msg_ID, rece_ID, self.answer_result(int(msg_result, 16))))
        return int(msg_result, 16)

    def answer_result(self, num):
        reason_dict = {0: '成功/确认', 1: '失败', 2: '消息有误', 3: '不支持'}
        return reason_dict[num]


if __name__ == '__main__':
    msg0 = b'~\x80\x01\x00\x05\x124Vx\x90\x12\x00\x00\x00\x00\x12\x10\x00\x0c~'
    msg1 = b'~\x80\x01\x00\x05\x013"!!"\x00\x01\x00\x00\x01\x02\x00\xb4~'
    msg2 = b'~\x80\x01\x00\x05"4Vx\x90\x15\x00}\x01\x00\x00\x00\x02\x00F~'
    msg3 = b'~\x80\x01\x00\x05"4Vx\x90\x15\x00E\x00\x00\x00\x02\x00}\x02~'
    rcm = ReceiveCommonMsg(msg3)
    print(rcm.explanation())
    # print(rcm.content)
