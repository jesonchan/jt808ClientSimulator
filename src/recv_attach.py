from jt808.receMsg.attachUploadFinish_0x9212 import ReceiveUploadFinishMsg
from jt808.receMsg.common_0x8001 import ReceiveCommonMsg
from jt808.tools import logs, data_config

log = logs.Log(data_config.PATH_LOG)
logger = log.get_logger()

# 附件上传应答同步处理


class AttachRecv:
    def __init__(self, tcp):
        self.tcp = tcp

    # 通用应答
    def commonMsg(self):
        recv_message = self.tcp.recv(1024)
        logger.info('通用应答%s' % recv_message)
        rc = ReceiveCommonMsg(recv_message)
        result = rc.explanation()
        return result

    # 文件上传完成应答
    def finishMsg(self):
        recv_message = self.tcp.recv(1024)
        logger.info('文件上传完成应答%s' % recv_message)
        auf = ReceiveUploadFinishMsg(recv_message)
        result = auf.explanation()
        return result


if __name__ == '__main__':
    logger.info('test')
