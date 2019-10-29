import binascii
from threading import Thread
from jt808.receMsg.realtime_0x9101 import RealtimeMsg
from jt808.receMsg.realtimeControl_0x9102 import RealtimeControlMsg
from jt808.receMsg.attachUpload_0x9208 import ReceiveUploadMsg
from jt808.receMsg.common_0x8001 import ReceiveCommonMsg
from jt808.receMsg.register_0x8100 import ReceiveRegisterMsg
from jt808.receMsg.textDownload_0x8300 import TextDownloadMsg
from jt808.tools import data_config, logs
from src_syn import send_attach_logic

log = logs.Log(data_config.PATH_LOG)
logger = log.get_logger()


# 消息应答逻辑


class RecvLogic:

    def msg_ID(self, msg):
        sBin = binascii.hexlify(msg)
        ID = str(sBin)[4:8]
        return ID

    def recv_logic(self, q, e, response_q):
        while True:
            # 从recv队列取消息
            recv_message = q.get()
            logger.info(recv_message)
            msgID = self.msg_ID(recv_message)
            # 注册应答
            if msgID == '8100':
                rc = ReceiveRegisterMsg(recv_message)
                result = rc.explanation()
                if result[0] == 0:
                    logger.info('# ----------- 注册成功 ----------- #')
                    aut_code = result[1]  # 返回鉴权码
                    data_config.AUT = aut_code
                    logger.info('返回鉴权码: %s' % aut_code)
                    e.set()

            # 通用应答
            elif msgID == '8001':
                rc = ReceiveCommonMsg(recv_message)
                result = rc.explanation()
                if result == 0:
                    logger.info('# ----------- 通用应答成功 ----------- #')
                    e.set()
                else:
                    data_config.FAIL += 1
                    logger.info('# ----------- 通用应答失败 ----------- #')
                    e.set()

            # 报警附件上传指令，获取附件上传ip port
            elif msgID == '9208':
                rum = ReceiveUploadMsg(recv_message)
                upload_ip, upload_port = rum.explanation()  # 接收附件服务器地址
                logger.info('# ----------- 发送附加信息 ----------- #')
                # 开启附件上传线程
                sa = send_attach_logic.AttachLogic(
                    upload_ip, upload_port, data_config.VEHICLE)
                upload_thread = Thread(target=sa.run)
                upload_thread.start()
                e.set()

            # 实时音视频传输请求，获取附件上传ip port 数据类型 码流类型
            elif msgID == '9101':
                try:
                    logger.info('# ----------- 开启实时通讯 ----------- #')
                    rt = RealtimeMsg(recv_message)
                    # 接收实时通讯服务器地址
                    upload_ip, upload_port, logic_pipe_no, data_type, stream_type = rt.explanation()
                    logger.info(
                        'ip %s, port %s, data type %s, stream_type %s' %
                        (upload_ip, upload_port, data_type, stream_type))
                    # msgID存入终端应答队列
                    response_q.put('9101')

                except BaseException as i:
                    logger.error(i)


            # 文本信息下发指令
            elif msgID == '8300':
                try:
                    logger.info('# ----------- 平台文本下发 ----------- #')
                    tdm = TextDownloadMsg(recv_message)
                    text = tdm.explanation()
                    if text:
                        data_config.REPLY_RESULT = 0
                    else:
                        data_config.REPLY_RESULT = 1
                    # msgID存入终端应答队列
                    response_q.put('8300')

                except BaseException as i:
                    logger.error(i)


if __name__ == '__main__':
    logger.info('test')
