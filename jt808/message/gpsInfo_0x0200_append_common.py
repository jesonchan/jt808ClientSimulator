from jt808.tools import data_config
from jt808.tools import tools
import time


class GPSInfoAppendCommon:
    # 从GPSinfo.txt 和Config.py中获取数据
    def __init__(self, GPSList, dID):
        self.t = tools.Tools()
        self.setdIDData(dID)
        self.setLatitudeData(GPSList[0])  # 经度
        self.setLongitudeData(GPSList[1])  # 纬度
        self.setElevationData(GPSList[2])  # 海拔高程
        self.setSpeedData(GPSList[3])  # 速度
        # self.setElevationData(config.ELEVATION)  # 海拔高程
        # self.setSpeedData(config.SPEED)  # 速度
        self.setDateData()  # 时间
        self.setCarState(data_config.CAR_STATE)  # 车辆状态
        self.setAlarmSign(data_config.ATTACH_SIGN)  # 报警标识号

    # 通用信息：车速 高程 纬度 经度 日期时间 车辆状态 报警标识号
    def getCommonData(self):
        self.commonData = (
            self.getSpeedData() +
            self.getElevationData() +
            self.getLatitudeData() +
            self.getLongitudeData() +
            self.getDateData() +
            self.getCarState() +
            self.getAlarmSign()
        )
        return self.commonData

    # 附加信息长度
    def bodyLen(self, bodyData):
        attribute_body_len = int(len(bodyData) / 2)
        attribute_body_len_sHex = self.t.IntToHex(attribute_body_len, 2)
        print('附加信息长度 ', attribute_body_len_sHex)
        return attribute_body_len_sHex

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
        self.latData = self.t.IntToHex(latNum, 8)

    # 海拔高程
    def getElevationData(self):
        return self.eleData

    def setElevationData(self, tempInt):
        self.eleData = self.t.IntToHex(tempInt, 4)

    # 速度
    def getSpeedData(self):
        print('速度', self.speedData)
        return self.speedData

    def setSpeedData(self, tempFloat):
        self.speedData = self.t.IntToHex(tempFloat, 2)

    # 时间
    def getDateData(self):
        return self.dateData

    def setDateData(self):
        self.dateData = time.strftime("%y%m%d%H%M%S", time.localtime())

    # 终端ID
    def getdIDData(self):
        print('终端ID ', self.dIDData)
        return self.dIDData

    # 七个字节，由大写字母和数字组成，此终端 ID 由制造商自行定义
    def setdIDData(self, tempStr):
        dIDNum = self.t.StrToHex(tempStr)
        if 14 != len(dIDNum):
            dIDNum = dIDNum + ((14 - len(dIDNum)) * '0')
        self.dIDData = dIDNum

    # 车辆状态
    def getCarState(self):
        return self.carState

    def setCarState(self, tempByte):
        self.carState = tempByte

    # 报警标识号
    def getAlarmSign(self):
        return self.AlarmSign

    def setAlarmSign(self, tempInt):
        dID = self.getdIDData()  # 终端 ID
        date = self.getDateData()  # 时间
        Num = '00'  # 同一时间点报s警的序号，从 0 循环累加
        attchNum = self.t.IntToHex(tempInt, 2)  # 表示该报警对应的附件数量
        self.AlarmSign = (dID + date + Num + attchNum + '00')
        data_config.SIGN = self.AlarmSign
        print('报警标识号', self.AlarmSign ,'附件数量', attchNum)

if __name__ == '__main__':
    g = GPSInfoAppendCommon([120.091645, 30.277906, 38, 9, 0], '8888888')
    print('GPS测试附加信息：', g.getCommonData())
    print(data_config.SIGN)
