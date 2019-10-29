from jt808.message import attachUploadDataRate
from src import body_data
from jt808.tools import data_config
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class Send:
    # 建立Socket连接， 并且注册
    def __init__(self, sim, vID, dID, tcp):
        self.vID = vID
        self.dID = dID
        self.sim = sim
        self.tcp = tcp
        self.data = body_data.BodyData(sim)
        print(('send body data:', self.data))
        self.tcp.settimeout(30)
        # self.filepath = config.ATTACH_PATH  # 附件路径

    # 发送注册
    def sendReg(self):
        reg = self.data.register_0x0100(self.vID, self.dID)
        print('发送注册消息 ', reg)
        self.tcp.send(bytes.fromhex(reg))
        data_config.BYTES += len(bytes.fromhex(reg))
        print(self.tcp.getsockname(), self.vID + '上线了')
        # logging.info(self.tcp.recv(1024))
        # self.failLog('注册', reg)

    # 发送鉴权
    def sendAut(self):
        aut = self.data.authentication_0x0102()
        print('发送鉴权消息 ', aut)
        self.tcp.send(bytes.fromhex(aut))
        data_config.BYTES += len(bytes.fromhex(aut))
        # logging.info(self.tcp.recv(1024))
        # self.failLog('鉴权', aut)

    # 发送GPS
    def sendGPS(self, GPSList):
        gps = self.data.gpsInfo_0x0200(GPSList, self.dID)
        print('发送GPS ', gps)
        self.tcp.send(bytes.fromhex(gps))
        data_config.BYTES += len(bytes.fromhex(gps))
        # self.failLog('gps', gps)

    # 发送心跳
    def sendHeart(self):
        heart = self.data.heartbeat_0x0002()
        print('发送心跳 ', heart)
        self.tcp.send(bytes.fromhex(heart))
        data_config.BYTES += len(bytes.fromhex(heart))
        # logging.info(self.tcp.recv(1024))
        # self.failLog('心跳', heart)

    # 发送注销
    def sendLogout(self):
        out = self.data.logout_0x0003()
        print('发送注销 ', out)
        self.tcp.send(bytes.fromhex(out))
        data_config.BYTES += len(bytes.fromhex(out))


if __name__ == '__main__':
    from socket import *

    tcp = socket(AF_INET, SOCK_STREAM)
    tcp.connect(('192.168.1.192', 1079))
    s = Send('123456789012', '浙C88888', '8888888', tcp)
    s.sendHeart()
    # 关闭连接:
    tcp.close()
