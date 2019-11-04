import time
from socket import *
from src_syn import send_attach
from jt808.tools import data_config, logs
from src_syn.recv_attach import AttachRecv

log = logs.Log(data_config.PATH_LOG)
logger = log.get_logger()


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
            logger.info('附件服务器{}连接成功...'.format(self.tcp.getsockname()))

            self.sa = send_attach.SendAttach(self.vehicleList[0],
                                             self.vehicleList[2],
                                             self.tcp)
            self.recv = AttachRecv(self.tcp)
        except BaseException as i:
            logger.error(i)
            logger.info('附件服务器无法连接！！！')
            return -1

    # 上传最多3个文件
    def run(self):
        try:
            self.sa.sendAttMsg()  # 文件信息上传
            self.recv.commonMsg()
            logger.info('# ----------- 上传附件 ----------- #')

            if self.attachNum == 1:
                self.uploadFile(
                    data_config.ATTACH_PATH,
                    data_config.ATTACH_TYPE)
                self.tcp.close()

            elif self.attachNum == 2:
                self.uploadFile(
                    data_config.ATTACH_PATH,
                    data_config.ATTACH_TYPE)
                self.uploadFile(
                    data_config.ATTACH_PATH_01,
                    data_config.ATTACH_TYPE_01)
                self.tcp.close()

            elif self.attachNum == 3:
                self.uploadFile(
                    data_config.ATTACH_PATH,
                    data_config.ATTACH_TYPE)
                self.uploadFile(
                    data_config.ATTACH_PATH_01,
                    data_config.ATTACH_TYPE_01)
                self.uploadFile(
                    data_config.ATTACH_PATH_02,
                    data_config.ATTACH_TYPE_02)
                self.tcp.close()

            else:
                self.uploadFile(
                    data_config.ATTACH_PATH,
                    data_config.ATTACH_TYPE)
                self.uploadFile(
                    data_config.ATTACH_PATH_01,
                    data_config.ATTACH_TYPE_01)
                self.uploadFile(
                    data_config.ATTACH_PATH_02,
                    data_config.ATTACH_TYPE_02)
                self.uploadFile(
                    data_config.ATTACH_PATH_03,
                    data_config.ATTACH_TYPE_03)
                self.tcp.close()
        except BaseException as i:
            logger.error(i)

    def uploadFile(self, ATTACH_PATH, ATTACH_TYPE):
        try:
            self.sa.sendAttUp(ATTACH_PATH, ATTACH_TYPE)
            self.recv.commonMsg()
            self.sa.sendAttEnd(ATTACH_PATH, ATTACH_TYPE)
            self.uploadFinishLogic()
            data_config.ATTACHMENT += 1
            time.sleep(1)
        except BaseException as i:
            logger.error(i)

    def uploadFinishLogic(self):
        result = self.recv.finishMsg()
        if result[0] == 0:
            logger.info('# ----------- 附件上传成功 ----------- #')
        else:
            logger.info('# ----------- 附件上传失败：%s ----------- #' % result)


if __name__ == '__main__':
    a = AttachLogic(
        '192.168.1.192', 1079, [
            '13322212122', '浙A22332', '2233200'])
    a.run()
