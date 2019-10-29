from jt808.tools import tools, logs, data_config

log = logs.Log(data_config.PATH_LOG)
logger = log.get_logger()


class TextDownloadMsg:
    def __init__(self, message):
        self.msg = message
        self.t = tools.Tools()
        self.content = []

    def explanation(self):
        content_bin = self.t.BinToHex(self.msg)  # 二进制转16进制
        # logger.info(content_bin)
        message_header = content_bin[2:26]  # 消息头
        message_body = content_bin[26:-4]  # 消息体
        self.content = [message_header, message_body]
        msg_ID = message_header[:4]  # 消息ID
        reply_No = message_header[20:24]  # 消息流水号
        data_config.REPLY_ID = msg_ID
        data_config.REPLY_NO = reply_No
        sign = message_body[:2]  # 标志
        text = message_body[2:]  # 文本信息
        text = self.t.HexToChr(text)  # 转中文
        logger.info(
            '消息ID: %s  消息流水号：%s 标志: %s 下发文本信息：%s' %
            (msg_ID, reply_No, sign, text))
        return text


if __name__ == '__main__':
    msg1 = b'~\x83\x00\x00\r"4Vx\x90\x15\x00I\x08test\xce\xc4\xb1\xbe\xcf\xc2\xb7\xa2y~'
    tdm = TextDownloadMsg(msg1)
    print(tdm.explanation())
    # print(rcm.content)
