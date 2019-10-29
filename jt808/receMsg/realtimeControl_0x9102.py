from jt808.tools import tools


class RealtimeControlMsg:
    def __init__(self, message):
        self.msg = message
        self.t = tools.Tools()
        self.content = []

    def explanation(self):
        content_bin = self.t.BinToHex(self.msg)  # 二进制转16进制
        print(content_bin)
        message_header = content_bin[2:26]  # 消息头
        message_body = content_bin[26:-4]  # 消息体
        self.content = [message_header, message_body]
        msg_ID = message_header[:4]  # 消息ID
        logic_pipe_no = message_body[:2]  # 逻辑通道号
        control_code = int(message_body[2:4], 16)  # 控制指令
        close_control = int(message_body[4:6], 16)  # 关闭音视频类型
        switch_stream = int(message_body[6:8], 16)  # 切换码流类型
        print(
            '消息ID: %s 控制指令: %s 关闭音视频类型: %s 切换码流类型: %s' %
            (msg_ID,
             self.controlType(control_code),
             self.closeType(close_control),
             self.streamType(switch_stream)))
        return logic_pipe_no, control_code, close_control, switch_stream

    def controlType(self, num):
        dict = {
            0: '关闭音视频传输指令',
            1: '切换码流',
            2: '暂停通道所有流发送',
            3: '恢复暂停',
            4: '关闭双向对讲'}
        return dict[num]

    def closeType(self, num):
        dict = {0: '关闭所有音视频', 1: '只关闭音频', 2: '只关闭视频'}
        return dict[num]

    def streamType(self, num):
        dict = {0: '主码流', 1: '子码流'}
        return dict[num]


if __name__ == '__main__':
    msg1 = b'~\x92\x08\x00S\x013"!!"\x00\x0b\x0e218.108.32.170\x047\x00\x002233200\x19\t\x12\x17\x11\x06\x00\x03\x00\x013"!!"2233200\x19\t\x12\x17\x11\x06\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xe4~'
    rlm = RealtimeControlMsg(msg1)
    print(rlm.explanation())
    # print(rcm.content)
