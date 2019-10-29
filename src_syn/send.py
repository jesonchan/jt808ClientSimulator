from jt808.message import attachUploadDataRate
from src_syn import body_data
from jt808.tools import data_config, logs

log = logs.Log(data_config.PATH_LOG)
logger = log.get_logger()


class Send:
    # 建立Socket连接， 并且注册
    def __init__(self, sim, vID, dID, tcp):
        self.vID = vID
        self.dID = dID
        self.sim = sim
        self.tcp = tcp
        self.data = body_data.BodyData(sim)
        # logger.info(('send body data:', self.data))
        self.tcp.settimeout(30)

    # 转格式发送
    def sendBytes(self, data):
        self.tcp.send(bytes.fromhex(data))
        data_config.BYTES += len(bytes.fromhex(data))

    # 发送注册
    def sendReg(self):
        reg = self.data.register_0x0100(self.vID, self.dID)
        logger.info('发送注册消息 %s' % reg)
        self.sendBytes(reg)
        logger.info((self.tcp.getsockname(), self.vID + '上线了'))

    # 发送鉴权
    def sendAut(self):
        aut = self.data.authentication_0x0102()
        logger.info('发送鉴权消息 %s' % aut)
        self.sendBytes(aut)

    # 发送GPS
    def sendGPS(self, GPSList):
        gps = self.data.gpsInfo_0x0200(GPSList, self.dID)
        logger.info('发送GPS %s' % gps)
        self.sendBytes(gps)

    # 发送心跳
    def sendHeart(self):
        heart = self.data.heartbeat_0x0002()
        logger.info('发送心跳 %s' % heart)
        self.sendBytes(heart)

    # 发送注销
    def sendLogout(self):
        out = self.data.logout_0x0003()
        logger.info('发送注销 %s' % out)
        self.sendBytes(out)

    # 发送终端通用应答
    def sendClinetCommonReply(self):
        reply = self.data.clinetCommonReply_0x0001()
        logger.info('发送终端通用应答 %s' % reply)
        self.sendBytes(reply)


if __name__ == '__main__':
    from socket import *

    tcp = socket(AF_INET, SOCK_STREAM)
    tcp.connect(('192.168.1.192', 1079))
    s = Send('123456789012', '浙C88888', '8888888', tcp)
    s.sendHeart()
    # 关闭连接:
    tcp.close()
