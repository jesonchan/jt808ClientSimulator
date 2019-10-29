from jt808.message import attachUploadFinish_0x1212
from jt808.message import attachUpload_0x1211
from jt808.message import attachMsg_0x1210
from jt808.message import authentication_0x0102
from jt808.message import register_0x0100
from jt808.message import join_data
from jt808.message import gpsInfo_0x0200
from jt808.message import commonReply_0x0001


# import os
# import sys
# CAR_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(CAR_PATH)


class BodyData:
    def __init__(self, sim):
        self.joinData = join_data.JoinData(sim)
        self.fullData = ''

    # 注册
    def register_0x0100(self, vID, dID):
        self.reg = register_0x0100.Register(vID, dID)
        self.fullData = self.joinData.getFullData('0100', self.reg.getData())
        return self.fullData

    # 鉴权
    def authentication_0x0102(self):
        self.aut = authentication_0x0102.Authentication()
        self.fullData = self.joinData.getFullData('0102', self.aut.getData())
        return self.fullData

    # 心跳
    def heartbeat_0x0002(self):
        self.fullData = self.joinData.getFullData('0002', '')
        return self.fullData

    # 注销
    def logout_0x0003(self):
        self.fullData = self.joinData.getFullData('0003', '')
        return self.fullData

    # gps
    def gpsInfo_0x0200(self, GPSList, dID):
        self.gps = gpsInfo_0x0200.GPSInfo(GPSList, dID)
        self.fullData = self.joinData.getFullData('0200', self.gps.getData())
        return self.fullData

    # 报警附件信息消息
    def attachMsg_0x1210(self, dID):
        self.atm = attachMsg_0x1210.AttachMsg(dID)
        self.fullData = self.joinData.getFullData('1210', self.atm.getData())
        return self.fullData

    # 文件信息上传
    def attachUpload_0x1211(self, filePath, fileType):
        self.upload = attachUpload_0x1211.AttachUpload(filePath, fileType)
        self.fullData = self.joinData.getFullData(
            '1211', self.upload.getData())
        return self.fullData

    # 文件上传完成消息
    def attachUploadEnd_0x1212(self, filePath, fileType):
        self.finish = attachUploadFinish_0x1212.AttachUploadFinish(filePath, fileType)
        self.fullData = self.joinData.getFullData(
            '1212', self.finish.getData())
        return self.fullData

    # 终端通用应答
    def clinetCommonReply_0x0001(self):
        self.aut = commonReply_0x0001.CommonReply()
        self.fullData = self.joinData.getFullData('0001', self.aut.getData())
        return self.fullData


if __name__ == '__main__':
    b = BodyData('123456789012')
    print(b.gpsInfo_0x0200([120.090102, 30.277826, -14, 1, 0], '1234567'))
    # print(b.attachMsg_0x1210( '../attachment/52204.jpg','8888888'))
    # print(b.attachUpload_0x1211('../attachment/52204.jpg'))
    # print(b.attachUploadEnd_0x1212('../attachment/52204.jpg'))
