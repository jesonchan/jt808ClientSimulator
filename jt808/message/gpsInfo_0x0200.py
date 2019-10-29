from jt808.tools import data_config
from jt808.tools import tools
from jt808.message.gpsInfo_0x0200_append import GPSInfoAppend

import time


class GPSInfo:
    # 从GPSinfo.txt 和Config.py中获取数据
    def __init__(self, GPSList, dID='8888888'):
        self.t = tools.Tools()
        self.dID = dID
        self.GPSList = GPSList
        self.setAlarmData(data_config.ALARM)  # 报警标志
        self.setStateData(data_config.STATE)  # 状态
        self.setLatitudeData(GPSList[0])  # 经度
        self.setLongitudeData(GPSList[1])  # 纬度
        self.setElevationData(GPSList[2])  # 高程
        self.setSpeedData(GPSList[3])  # 速度
        data_config.IS_ATTACH = GPSList[4]  # 是否有附加报警指令
        self.setDirectData(data_config.DIRECTION)  # 方向
        self.setDateData()  # 时间

    def getData(self):
        self.data = (self.getAlarmData() +
                     self.getStateData() +
                     self.getLongitudeData() +
                     self.getLatitudeData() +
                     self.getElevationData() +
                     self.getSpeedData() +
                     self.getDirectData() +
                     self.getDateData() +
                     self.get_Append())
        return self.data

    # 是否有附加报警信息
    def get_Append(self):
        if data_config.IS_ATTACH == 1:
            self.GPSAppend = GPSInfoAppend(self.GPSList, self.dID)  # 附加信息
            return self.GPSAppend.getAppendData()
        else:
            return ''

    # 报警
    def getAlarmData(self):
        return self.alarmData

    def setAlarmData(self, tempInt):
        # 报警标志
        strBin = ''.join(tempInt)
        print('报警标志', strBin)
        hexBinData = int(strBin, 2)  # 转int类型，strBin 为二进制
        self.alarmData = self.t.IntToHex(hexBinData, 8)  # int转16进制，数据类型为DWORD

    # 状态
    def getStateData(self):
        return self.stateData

    def setStateData(self, tempInt):
        strBin = ''.join(tempInt)
        print('状态位', strBin)
        hexBinData = int(strBin, 2)
        self.stateData = self.t.IntToHex(hexBinData, 8)

    # 经度

    def getLongitudeData(self):
        print('经度', self.lonData)
        return self.lonData

    def setLongitudeData(self, tempDouble):
        lonNum = int(float(tempDouble) * 1000000)
        self.lonData = self.t.IntToHex(lonNum, 8)

    # 纬度
    def getLatitudeData(self):
        print('纬度', self.latData)
        return self.latData

    def setLatitudeData(self, tempDouble):
        latNum = int(float(tempDouble) * 1000000)
        print(latNum)
        self.latData = self.t.IntToHex(latNum, 8)

    # 海拔高程
    def getElevationData(self):
        print('海拔高程', self.eleData)
        return self.eleData

    def setElevationData(self, tempInt):
        self.eleData = self.t.IntToHex(tempInt, 4)

    # 速度
    def getSpeedData(self):
        print('速度', self.speedData)
        return self.speedData

    def setSpeedData(self, tempFloat):
        self.speedData = self.t.IntToHex(int(tempFloat*10), 4)

    # 方向
    def getDirectData(self):
        print('方向', self.dirData)
        return self.dirData

    def setDirectData(self, tempInt):
        self.dirData = self.t.IntToHex(tempInt, 4)  # "0020"

    # 时间
    def getDateData(self):
        return self.dateData

    def setDateData(self):
        self.dateData = time.strftime("%y%m%d%H%M%S", time.localtime())

    # 里程
    # def getMileageData(self):
    #     return self.milData
    #
    # def setMileageData(self, tempInt):
    #     milNum = self.t.IntToHex(tempInt*10, 8)
    #     self.milData = '0104' + milNum

    # # 油量
    # def getOliData(self):
    #     return self.oilData
    #
    # def setOliData(self, tempInt):
    #     oilNum = self.t.IntToHex(tempInt, 2)
    #     self.oilData = '0202' + oilNum


if __name__ == '__main__':
    g = GPSInfo([120.090102, 30.277826, -14, 10, 1], '1234567')
    print('GPS测试：', g.getData())
