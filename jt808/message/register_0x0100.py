from jt808.tools import data_config
from jt808.tools import tools

# 终端注册


class Register:
    def __init__(self, vID, dID):
        self.t = tools.Tools()
        self.setvIDData(vID)
        self.setdIDData(dID)
        self.setColorData(data_config.COLOR)
        self.setProvinceData(data_config.PROVINCE)
        self.setCityData(data_config.CITY)
        self.setMakerData(data_config.MAKER)
        self.setDeviceModel(data_config.DEVICEMODEL)

    def getData(self):
        self.data = (
            self.getProvinceData() +
            self.getCityData() +
            self.getMakerData() +
            self.getDeviceModel() +
            self.getdIDData() +
            self.getColorData() +
            self.getvIDData()
        )
        return self.data

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

    # 车牌号
    def getvIDData(self):
        print('车牌号 ', self.vIDData)
        return self.vIDData

    # 数据类型STRING
    def setvIDData(self, tempStr):
        vIDNum = self.t.ChrToHex(tempStr[0])
        vIDNum = vIDNum + self.t.StrToHex(tempStr[1:])
        self.vIDData = vIDNum

    # 车牌颜色
    def getColorData(self):
        print('车牌颜色 ', self.coloData)
        return self.coloData

    # 数据类型BYTE
    def setColorData(self, tempHex):
        self.coloData = tempHex

    # 省域ID
    def getProvinceData(self):
        print('省ID ', self.provinceData)
        return self.provinceData

    # 数据类型WORD
    def setProvinceData(self, tempChr):
        tempInt = int(tempChr)
        self.provinceData = self.t.IntToHex(tempInt, 4).upper()

    # 市域ID

    def getCityData(self):
        print('市ID ', self.CityData)
        return self.CityData

    # 数据类型WORD
    def setCityData(self, tempChr):
        tempInt = int(tempChr)
        self.CityData = self.t.IntToHex(tempInt, 4).upper()

    # 制造商

    def getMakerData(self):
        print('制造商 ', self.makerData)
        return self.makerData

    # 五个字节，终端制造商编码

    def setMakerData(self, tempChr):
        self.makerData = self.t.StrToHex(tempChr)

    # 终端型号

    def getDeviceModel(self):
        print('终端型号 ', self.dmData)
        return self.dmData

    # 八个字节，此终端型号由制造商自行定义，位数不足八位的，补空格 0x20
    def setDeviceModel(self, tempChr):
        sHex = self.t.StrToHex(tempChr)
        if 16 != len(sHex):
            self.dmData = sHex + ((16 - len(sHex)) * '0')


if __name__ == '__main__':
    a = Register('鄂A00001', 'AA00001')
    print('终端注册测试：', a.getData())
