from jt808.tools import data_config
from jt808.tools import tools
import time


class AttachUpload:
    # 从Config.py中获取数据
    def __init__(self, filePath, fileType):
        self.t = tools.Tools()
        self.filePath = filePath
        self.setAttachType(fileType)  # 文件类型
        self.setAttachName(self.filePath)  # 文件名称
        self.setAttachSize(self.filePath)  # 文件大小
        self.setAttachNameLen(self.attachName)  # 文件长度

    def getData(self):
        self.data = (self.getAttachNameLen() + self.getAttachName() +
                     self.getAttachType() + self.getAttachSize())
        return self.data

    # 信息类型
    def getAttachType(self):
        return self.msgType

    def setAttachType(self, tempByte):
        self.msgType = tempByte

    # 文件名称
    def getAttachName(self):
        print('文件名称', self.attachName)
        return self.attachName

    def setAttachName(self, filepath):
        print('0x1211 ->文件名称', filepath)
        self.attachName = self.t.getDocNameToHex(filepath)

    # 文件名称长度
    def getAttachNameLen(self):
        print('文件名称长度', self.attachNameLen)
        return self.attachNameLen

    def setAttachNameLen(self, tempByte):
        lenNum = int(len(tempByte) / 2)
        self.attachNameLen = self.t.IntToHex(lenNum, 2)

    # 文件大小
    def getAttachSize(self):
        print('文件大小', self.attachSize)
        return self.attachSize

    def setAttachSize(self, filepath):
        size = self.t.getDocSizeToHex(filepath)
        if len(size) != 8:
            size = (8 - len(size)) * '0' + size
        self.attachSize = size


if __name__ == '__main__':
    a = AttachUpload('../../attachment/52204.jpg')
    print('文件信息上传：', a.getData())
