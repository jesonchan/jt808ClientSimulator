from jt808.tools import tools


class ReceiveRegisterMsg:
    def __init__(self, message):
        self.msg = message
        self.t = tools.Tools()
        self.content = []  # 消息内容
        self.result = []  # 消息结果 鉴权码

    def explanation(self):
        content_bin = self.t.BinToHex(self.msg)  # 二进制转16进制
        # print(content_bin)
        message_header = content_bin[2:26]  # 消息头
        message_body = content_bin[26:-4]  # 消息体
        self.content = [message_header, message_body]
        msg_ID = message_header[:4]  # 消息ID
        msg_result = message_body[4:6]  # 应答结果
        self.result.append(int(msg_result))
        print('消息ID: %s 应答结果：%s' %
              (msg_ID, self.answer_result(int(msg_result))))
        if int(msg_result) == 0:
            AutHex = message_body[6:]  # 鉴权码
            AutCode = self.t.HexToStr(AutHex)  # 转string
            self.result.append(AutCode)
        else:
            fail_reason = self.answer_result(int(msg_result))
            self.result.append(fail_reason)
        return self.result

    def answer_result(self, num):
        reason_dict = {
            0: '成功',
            1: '车辆已被注册',
            2: '数据库中无该车辆',
            3: '终端已被注册',
            4: '数据库中无该终端'}
        return reason_dict[num]


if __name__ == '__main__':
    message = b'~\x81\x00\x00\r\x013"!!"\x00\x00\x00\x00\x00test_token\x8c~'
    rcm = ReceiveRegisterMsg(message)
    print(rcm.explanation())
    print(rcm.content)
    print(rcm.answer_result(1))
