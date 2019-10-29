from jt808.message import attachUploadDataRate
from src import body_data
from jt808.tools import data_config
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# 苏标 上传报警附件信息


class SendAttach:
    # 建立Socket连接， 并且注册
    def __init__(self, sim, dID, tcp):
        self.dID = dID
        self.tcp = tcp
        self.sim = sim
        self.data = body_data.BodyData(sim)
        print(('send body data:', self.data))
        # self.filepath = config.ATTACH_PATH  # 附件路径
        self.tcp.settimeout(30)

    # 发送报警附件信息消息

    def sendAttMsg(self):
        attachMsg = self.data.attachMsg_0x1210(self.dID)
        print('发送报警附件信息消息 ', attachMsg)
        self.tcp.send(bytes.fromhex(attachMsg))
        data_config.BYTES += len(bytes.fromhex(attachMsg))

    # 发送文件信息上传

    def sendAttUp(self, filepath, fileType):
        attUpload = self.data.attachUpload_0x1211(filepath, fileType)
        print('发送文件信息上传 ', attUpload)
        self.tcp.send(bytes.fromhex(attUpload))
        dataRate = attachUploadDataRate.AttachDataRate(filepath, self.tcp)
        dataRate.sendData()
        data_config.BYTES += len(bytes.fromhex(attUpload))

    # 文件上传完成消息
    def sendAttEnd(self, filepath, fileType):
        attFinish = self.data.attachUploadEnd_0x1212(filepath, fileType)
        print('文件上传完成消息 ', attFinish)
        self.tcp.send(bytes.fromhex(attFinish))
        data_config.BYTES += len(bytes.fromhex(attFinish))


if __name__ == '__main__':
    from socket import *

    tcp = socket(AF_INET, SOCK_STREAM)
    tcp.connect(('172.16.0.38', 1079))
    s = SendAttach('123456789012', '8888888', tcp)
    s.sendAttMsg()
    msg = tcp.recv(1024)
    print(msg)
    # print(msg.decode('gbk'))
    s.sendAttUp('../attachment/02_64_6401_3_0.mp4',data_config.ATTACH_TYPE_03)
    s.sendAttEnd('../attachment/02_64_6401_3_0.mp4',data_config.ATTACH_TYPE_03)
    print(tcp.recv(1024))
    # # 接收数据:
    # buffer = []
    # while True:
    #     # 每次最多接收1k字节:
    #     d = tcp.recv(1024)
    #     if d:
    #         buffer.append(d)
    #         print(buffer)
    #         data = b''.join(buffer)
    #         print(data)
    #     else:
    #         break
    # 关闭连接:
    tcp.close()
