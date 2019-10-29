from jt808.tools import data_config
from jt808.tools import tools
import time


class AttachMsg:
    # 从Config.py中获取数据
    def __init__(self, dID):
        self.t = tools.Tools()
        self.setdIDData(dID)                # 终端 ID
        self.setDateData()                  # 时间
        self.alarmSign = data_config.SIGN    # 报警标识号 同GPS 0x0200里报警标识号一致
        self.attchNum = self.t.IntToHex(data_config.ATTACH_SIGN, 2)  # 附件数量
        self.setMsgType(data_config.MSG_TYPE)    # 信息类型
        self.fileInit()

    def fileInit(self):
        num = data_config.ATTACH_SIGN
        if num == 1:
            name = self.setAttachName(data_config.ATTACH_PATH)  # 文件名称
            filepath = self.setAttachSize(data_config.ATTACH_PATH)  # 文件大小
            self.attachMsgList = self.setAttachMsgList(name, filepath)  # 附件消息
        elif num == 2:
            name = self.setAttachName(data_config.ATTACH_PATH)  # 文件名称
            filepath = self.setAttachSize(data_config.ATTACH_PATH)  # 文件大小
            name1 = self.setAttachName(data_config.ATTACH_PATH_01)  # 文件名称
            filepath1 = self.setAttachSize(data_config.ATTACH_PATH_01)  # 文件大小
            # 附件消息列表
            self.attachMsgList = self.setAttachMsgList(name, filepath) + \
                self.setAttachMsgList(name1, filepath1)
        elif num == 3:
            name = self.setAttachName(data_config.ATTACH_PATH)  # 文件名称
            filepath = self.setAttachSize(data_config.ATTACH_PATH)  # 文件大小
            name1 = self.setAttachName(data_config.ATTACH_PATH_01)  # 文件名称
            filepath1 = self.setAttachSize(data_config.ATTACH_PATH_01)  # 文件大小
            name2 = self.setAttachName(data_config.ATTACH_PATH_02)  # 文件名称
            filepath2 = self.setAttachSize(data_config.ATTACH_PATH_02)  # 文件大小
            # 附件消息列表
            self.attachMsgList = self.setAttachMsgList(name, filepath) + \
                                 self.setAttachMsgList(name1, filepath1) + \
                                 self.setAttachMsgList(name2, filepath2)

        else:
            name = self.setAttachName(data_config.ATTACH_PATH)  # 文件名称
            filepath = self.setAttachSize(data_config.ATTACH_PATH)  # 文件大小
            name1 = self.setAttachName(data_config.ATTACH_PATH_01)  # 文件名称
            filepath1 = self.setAttachSize(data_config.ATTACH_PATH_01)  # 文件大小
            name2 = self.setAttachName(data_config.ATTACH_PATH_02)  # 文件名称
            filepath2 = self.setAttachSize(data_config.ATTACH_PATH_02)  # 文件大小
            name3 = self.setAttachName(data_config.ATTACH_PATH_03)  # 文件名称
            filepath3 = self.setAttachSize(data_config.ATTACH_PATH_03)  # 文件大小
            # 附件消息列表
            self.attachMsgList = self.setAttachMsgList(name, filepath) + \
                self.setAttachMsgList(name1, filepath1) + \
                self.setAttachMsgList(name2, filepath2) + \
                self.setAttachMsgList(name3, filepath3)


    def getData(self):
        self.data = (self.getdIDData() +
                     self.alarmSign +
                     self.getAlarmSignNo() +
                     self.getMsgType() +
                     self.attchNum +
                     self.attachMsgList
                     )
        return self.data

    # 时间
    def getDateData(self):
        return self.dateData

    def setDateData(self):
        self.dateData = time.strftime("%y%m%d%H%M%S", time.localtime())

    # 终端ID
    def getdIDData(self):
        # print('终端ID ', self.dIDData)
        return self.dIDData

    # 七个字节，由大写字母和数字组成，此终端 ID 由制造商自行定义
    def setdIDData(self, tempStr):
        dIDNum = self.t.StrToHex(tempStr)
        if 14 != len(dIDNum):
            dIDNum = dIDNum + ((14 - len(dIDNum)) * '0')
        self.dIDData = dIDNum

    # 报警编号
    def getAlarmSignNo(self):
        sign = self.alarmSign
        print('报警标识号', sign)
        if len(sign) != 64:
            sign = ((64 - len(sign)) * '0') + sign
        self.AlarmSignNo = sign
        print('报警编号 ', self.AlarmSignNo)
        return self.AlarmSignNo

    # 信息类型
    def getMsgType(self):
        return self.msgType

    def setMsgType(self, tempByte):
        self.msgType = tempByte

    # 文件名称
    def setAttachName(self, filepath):
        print('0x1210 ->文件名称', filepath)
        self.attachName = self.t.getDocNameToHex(filepath)
        return self.attachName

    # 文件大小
    def setAttachSize(self, filepath):
        size = self.t.getDocSizeToHex(filepath)
        if len(size) != 8:
            size = (8 - len(size)) * '0' + size
        self.attachSize = size
        print('文件大小', self.attachSize)
        return self.attachSize

    # 附件信息列表
    def setAttachMsgList(self, ATTACH_NAME, ATTACH_SIZE):
        lenNum = int(len(ATTACH_NAME) / 2)
        attachNameLen = self.t.IntToHex(lenNum, 2)
        attachMsgList = attachNameLen + ATTACH_NAME + ATTACH_SIZE
        print('附件信息列表 ', attachMsgList)
        return attachMsgList


if __name__ == '__main__':
    # a = AttachMsg('../../attachment/52204.jpg','1234567')
    # a = AttachMsg('8888888')
    # print('报警附件信息消息测试：', a.getData())
    print(time.strftime("%y%m%d%H%M%S", time.localtime()))
