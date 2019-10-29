from jt808.tools import tools, logs, data_config

log = logs.Log(data_config.PATH_LOG)
logger = log.get_logger()


class RealtimeMsg:
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
        reply_No = message_header[20:24]  # 消息流水号
        data_config.REPLY_ID = msg_ID
        data_config.REPLY_NO = reply_No
        ip_length = message_body[:2]  # 附件服务器 IP 地址长度
        length = int(ip_length, 16)
        hostHex = message_body[2:(2 + length * 2)]  # 附件服务器 IP 地址
        host = self.t.HexToStr(hostHex)
        portHex = message_body[(2 + length * 2):(2 + length * 2 + 4)]  # 附件服务器端口（TCP）
        port = int(portHex, 16)
        logic_pipe_no = message_body[(
            2 + length * 2 + 8):(2 + length * 2 + 10)]  # 逻辑通道号
        data_typeHex = message_body[(
            2 + length * 2 + 10):(2 + length * 2 + 12)]  # 数据类型
        data_type = int(data_typeHex, 16)
        stream_typeHex = message_body[(
            2 + length * 2 + 12):(2 + length * 2 + 14)]  # 码流类型
        stream_type = int(stream_typeHex, 16)
        logger.info('消息ID: %s IP地址: %s 服务器端口: %s' % (msg_ID, host, port))
        logger.info('数据类型: %s 码流类型: %s' %
                    (self.dataType(data_type),
                     self.streamType(stream_type)))
        logger.info('逻辑通道号: %s' % logic_pipe_no)
        return host, port, logic_pipe_no, data_type, stream_type

    def dataType(self, num):
        dict = {
            0: '音视频',
            1: '视频',
            2: '双向对话',
            3: '监听',
            4: '中心广播',
            5: '透传'}
        return dict[num]

    def streamType(self, num):
        dict = {0: '主码流', 1: '子码流'}
        return dict[num]


if __name__ == '__main__':
    msg1 = b'~\x92\x08\x00S\x013"!!"\x00\x0b\x0e218.108.32.170\x047\x00\x002233200\x19\t\x12\x17\x11\x06\x00\x03\x00\x013"!!"2233200\x19\t\x12\x17\x11\x06\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\xe4~'
    rlm = RealtimeMsg(msg1)
    print(rlm.explanation())
    # print(rcm.content)
