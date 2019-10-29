from jt808.tools import data_config
from jt808.tools import tools
from jt808.message.gpsInfo_0x0200_append_common import GPSInfoAppendCommon


class GPSInfoAppendCondition:
    # 从GPSinfo.txt 和Config.py中获取数据
    def __init__(self, GPSList, dID):
        self.t = tools.Tools()
        self.GPSList = GPSList
        self.dID = dID

        # ----------- 驾驶状态监测系统报警信息----------- #
        self.setConID(data_config.CON_ID)                    # 报警 ID
        self.setConStateData(data_config.CON_STATE)          # 标志状态
        self.setConAlarmData(data_config.CON_ALARM)          # 报警/事件类型
        self.setConAlarmLevel(data_config.CON_LEVEL)         # 报警级别
        self.setConWeary(data_config.CON_WEARY)                 # 疲劳程度

    # 驾驶状态监测系统报警信息

    def getDrivingConditionMonitor(self):
        common = GPSInfoAppendCommon(self.GPSList, self.dID)
        body_data = (
            self.getConID() +
            self.getConStateData() +
            self.getConAlarmData() +
            self.getConAlarmLevel() +
            self.getConWeary() +
            '00000000' +
            common.getCommonData()
        )
        divConMon = ('65' + common.bodyLen(body_data) + body_data)
        return divConMon

    # 报警ID
    def getConID(self):
        return self.conID

    def setConID(self, tempByte):
        self.conID = tempByte

    # 状态
    def getConStateData(self):
        return self.conStateData

    def setConStateData(self, tempByte):
        self.conStateData = tempByte

    # 报警/事件类型
    def getConAlarmData(self):
        print('驾驶状态监测报警事件', self.conAlarmData)
        return self.conAlarmData

    def setConAlarmData(self, tempByte):
        self.conAlarmData = tempByte

    # 报警级别
    def getConAlarmLevel(self):
        return self.conAlarmLevel

    def setConAlarmLevel(self, tempByte):
        self.conAlarmLevel = tempByte

    # 疲劳程度
    def getConWeary(self):
        return self.weary

    def setConWeary(self, tempByte):
        self.weary = tempByte


if __name__ == '__main__':
    g = GPSInfoAppendCondition([120.091645, 30.277906, 38, 9, 0], '8888888')
    print('驾驶状态监测系统报警信息：', g.getDrivingConditionMonitor())
