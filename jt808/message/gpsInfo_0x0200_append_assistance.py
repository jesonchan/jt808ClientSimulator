from jt808.tools import data_config
from jt808.tools import tools
from jt808.message.gpsInfo_0x0200_append_common import GPSInfoAppendCommon


class GPSInfoAppendAssistance:
    # 从GPSinfo.txt 和Config.py中获取数据
    def __init__(self, GPSList, dID):
        self.t = tools.Tools()
        self.GPSList = GPSList
        self.dID = dID
        # -----------高级驾驶辅助报警信息----------- #
        self.setAssID(data_config.ASS_ID)                # 报警 ID
        self.setAssStateData(data_config.ASS_STATE)      # 标志状态
        self.setAssAlarmData(data_config.ASS_ALARM)      # 报警/事件类型
        self.setAssAlarmLevel(data_config.ASS_LEVEL)     # 报警级别
        self.setFrontSpeedData(data_config.ASS_F_SPEED)  # 前车车速
        self.setFrontDistance(data_config.ASS_F_DISTANCE)    # 前车/行人距离
        self.setDeviate(data_config.ASS_DEVIATE)         # 偏离类型
        self.setRoadSign(data_config.ASS_ROAD_SIGN)      # 道路标志识别类型
        self.setRoadSignData('00')                  # 道路标志识别数据

    # 高级驾驶辅助系统报警

    def getDrivingAssistanceData(self):
        common = GPSInfoAppendCommon(self.GPSList, self.dID)
        body_data = (self.getAssID() +
                     self.getAssStateData() +
                     self.getAssAlarmData() +
                     self.getAssAlarmLevel() +
                     self.getFrontSpeedData() +
                     self.getFrontDistance() +
                     self.getDeviate() +
                     self.getRoadSign() +
                     self.getRoadSignData() +
                     common.getCommonData()
                     )
        divAssData = ('64' + common.bodyLen(body_data) + body_data)
        return divAssData

    # -----------高级驾驶辅助报警信息----------- #
    # 报警ID
    def getAssID(self):
        return self.assID

    def setAssID(self, tempByte):
        self.assID = tempByte
    # 报警

    def getAssAlarmData(self):
        print('高级驾驶辅助报警事件', self.assAlarmData)
        return self.assAlarmData

    def setAssAlarmData(self, tempByte):
        self.assAlarmData = tempByte

    # 状态
    def getAssStateData(self):
        return self.assStateData

    def setAssStateData(self, tempByte):
        self.assStateData = tempByte

    # 报警级别
    def getAssAlarmLevel(self):
        return self.assAlarmLevel

    def setAssAlarmLevel(self, tempByte):
        self.assAlarmLevel = tempByte

    # 前车车速
    def getFrontSpeedData(self):
        return self.frontSpeed

    def setFrontSpeedData(self, tempFloat):
        self.frontSpeed = self.t.IntToHex(tempFloat, 2)

    # 前车/行人距离
    def getFrontDistance(self):
        return self.frontDistance

    def setFrontDistance(self, tempInt):
        self.frontDistance = self.t.IntToHex(tempInt, 2)

    # 道路标志识别类型
    def getRoadSign(self):
        return self.roadSign

    def setRoadSign(self, tempByte):
        self.roadSign = tempByte

    # 偏离类型
    def getDeviate(self):
        return self.deviate

    def setDeviate(self, tempByte):
        self.deviate = tempByte

    # 道路标志识别数据
    def getRoadSignData(self):
        return self.roadSignData

    def setRoadSignData(self, tempByte):
        self.roadSignData = tempByte


if __name__ == '__main__':
    g = GPSInfoAppendAssistance([120.091645, 30.277906, 38, 9, 0], '8888888')
    print('GPS测试附加信息：', g.getDrivingAssistanceData())
