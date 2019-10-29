from jt808.receMsg.attachUploadFinish_0x9212 import ReceiveUploadFinishMsg
from jt808.receMsg.attachUpload_0x9208 import ReceiveUploadMsg
from jt808.receMsg.common_0x8001 import ReceiveCommonMsg
from jt808.receMsg.register_0x8100 import ReceiveRegisterMsg

class Recv:
    def __init__(self, tcp):
        self.tcp = tcp

    # 通用应答
    def commonMsg(self):
        recv_message = self.tcp.recv(1024)
        print(recv_message)
        rc = ReceiveCommonMsg(recv_message)
        result = rc.explanation()
        return result

    # 注册应答
    def registerMsg(self):
        recv_message = self.tcp.recv(1024)
        print(recv_message)
        rrm = ReceiveRegisterMsg(recv_message)
        result = rrm.explanation()
        return result

    # 报警附件上传指令，获取附件上传ip port
    def uploadMsg(self):
        recv_message = self.tcp.recv(1024)
        print(recv_message)
        rum = ReceiveUploadMsg(recv_message)
        upload_ip, upload_port = rum.explanation()
        return upload_ip, upload_port

    # 文件上传完成应答
    def finishMsg(self):
        recv_message = self.tcp.recv(1024)
        print(recv_message)
        auf = ReceiveUploadFinishMsg(recv_message)
        result = auf.explanation()
        return result


