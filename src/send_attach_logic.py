import time
from socket import *
from src import send_attach
from jt808.tools import data_config
from src.recv import Recv


class AttachLogic:

    def __init__(self, ip, port, vehicleList):
        self.ip = ip
        self.port = port
        self.vehicleList = vehicleList
        self.socketInit()

        self.attachNum = data_config.ATTACH_SIGN  # 附件数量

    def socketInit(self):
        try:
            self.tcp = socket(AF_INET, SOCK_STREAM)
            self.tcp.connect((self.ip, self.port))
            print('{}连接成功...'.format(self.tcp.getsockname()))

            self.sa = send_attach.SendAttach(self.vehicleList[0],
                                             self.vehicleList[2],
                                             self.tcp)
            self.recv = Recv(self.tcp)
        except BaseException:
            print('无法连接！！！')
            return -1

    # 上传最多3个文件
    def run(self):
        self.sa.sendAttMsg()  # 文件信息上传
        self.recv.commonMsg()
        if self.attachNum == 1:
            self.sa.sendAttUp(data_config.ATTACH_PATH,data_config.ATTACH_TYPE)
            self.recv.commonMsg()
            self.sa.sendAttEnd(data_config.ATTACH_PATH,data_config.ATTACH_TYPE)
            self.recv.finishMsg()
            data_config.ATTACHMENT += 1
            self.tcp.close()

        elif self.attachNum == 2:
            self.sa.sendAttUp(data_config.ATTACH_PATH,data_config.ATTACH_TYPE)
            self.recv.commonMsg()
            self.sa.sendAttEnd(data_config.ATTACH_PATH,data_config.ATTACH_TYPE)
            self.recv.finishMsg()
            data_config.ATTACHMENT += 1
            time.sleep(1)
            self.sa.sendAttUp(data_config.ATTACH_PATH_01,data_config.ATTACH_TYPE_01)
            self.recv.commonMsg()
            self.sa.sendAttEnd(data_config.ATTACH_PATH_01,data_config.ATTACH_TYPE_01)
            self.recv.finishMsg()
            data_config.ATTACHMENT += 1
            self.tcp.close()

        elif self.attachNum == 3:
            self.sa.sendAttUp(data_config.ATTACH_PATH,data_config.ATTACH_TYPE)
            self.recv.commonMsg()
            self.sa.sendAttEnd(data_config.ATTACH_PATH,data_config.ATTACH_TYPE)
            self.recv.finishMsg()
            data_config.ATTACHMENT += 1
            time.sleep(1)
            self.sa.sendAttUp(data_config.ATTACH_PATH_01,data_config.ATTACH_TYPE_01)
            self.recv.commonMsg()
            self.sa.sendAttEnd(data_config.ATTACH_PATH_01,data_config.ATTACH_TYPE_01)
            self.recv.finishMsg()
            data_config.ATTACHMENT += 1
            time.sleep(1)
            self.sa.sendAttUp(data_config.ATTACH_PATH_02,data_config.ATTACH_TYPE_02)
            self.recv.commonMsg()
            self.sa.sendAttEnd(data_config.ATTACH_PATH_02,data_config.ATTACH_TYPE_02)
            self.recv.finishMsg()
            data_config.ATTACHMENT += 1
            self.tcp.close()

        else:
            self.sa.sendAttUp(data_config.ATTACH_PATH,data_config.ATTACH_TYPE)
            self.recv.commonMsg()
            self.sa.sendAttEnd(data_config.ATTACH_PATH,data_config.ATTACH_TYPE)
            self.recv.finishMsg()
            data_config.ATTACHMENT += 1
            time.sleep(1)
            self.sa.sendAttUp(data_config.ATTACH_PATH_01,data_config.ATTACH_TYPE_01)
            self.recv.commonMsg()
            self.sa.sendAttEnd(data_config.ATTACH_PATH_01,data_config.ATTACH_TYPE_01)
            self.recv.finishMsg()
            data_config.ATTACHMENT += 1
            time.sleep(1)
            self.sa.sendAttUp(data_config.ATTACH_PATH_02,data_config.ATTACH_TYPE_02)
            self.recv.commonMsg()
            self.sa.sendAttEnd(data_config.ATTACH_PATH_02,data_config.ATTACH_TYPE_02)
            self.recv.finishMsg()
            data_config.ATTACHMENT += 1
            time.sleep(1)
            self.sa.sendAttUp(data_config.ATTACH_PATH_03,data_config.ATTACH_TYPE_03)
            self.recv.commonMsg()
            self.sa.sendAttEnd(data_config.ATTACH_PATH_03,data_config.ATTACH_TYPE_03)
            self.recv.finishMsg()
            data_config.ATTACHMENT += 1
            self.tcp.close()


    def uploadFinish_logic(self):
        result = self.recv.finishMsg()
        if result[0] == 0:
            print('# ----------- 附件上传成功 ----------- #')
        else:
            print('# ----------- 附件上传失败 ----------- #')

if __name__ == '__main__':
    a = AttachLogic(
        '192.168.1.192', 1079, [
            '13322212122', '浙A22332', '2233200'])
    a.run()
