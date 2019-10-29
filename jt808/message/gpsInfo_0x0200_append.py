from jt808.tools import data_config
from jt808.tools import tools
from jt808.message.gpsInfo_0x0200_append_assistance import GPSInfoAppendAssistance
from jt808.message.gpsInfo_0x0200_append_condition import GPSInfoAppendCondition
import random


class GPSInfoAppend:
    # 从GPSinfo.txt 和Config.py中获取数据
    def __init__(self, GPSList, dID):
        self.t = tools.Tools()
        self.GPSList = GPSList
        self.dID = dID
        self.alarm = self.GPSList[5]

        # -----------胎压监测系统报警信息----------- #
        self.setTirePressure(data_config.TIRE_PRESSURE)

        # ----------- 盲区监测系统报警信息----------- #
        self.setBlindArea(data_config.BLIND_AREA)

    # -----------附加信息组装----------- #
    # 选取附加信息
    def getAppendData(self):
        ass_alarm_dict = {
            '前向碰撞报警': '01',
            '车道偏离报警': '02',
            '车距过近报警': '03',
            '行人碰撞报警': '04',
            '频繁变道报警': '05',
            '道路标识超限报警': '06',
            '障碍物报警': '07',
            '用户自定义': '08~0F',
            '道路标志识别事件': '10',
            '主动抓拍事件': '11'}
        con_alarm_dict = {
            '疲劳驾驶报警': '01',
            '接打电话报警': '02',
            '抽烟报警': '03',
            '分神驾驶报警': '04',
            '驾驶员异常报警': '05',
            '用户自定义': '12~1F',
            '自动抓拍事件': '10',
            '驾驶员变更事件': '11'}
        ass_alarm_list = [
            '前向碰撞报警',
            '车道偏离报警',
            '车距过近报警',
            '行人碰撞报警',
            '频繁变道报警',
            '道路标识超限报警']
        con_alarm_list = ['疲劳驾驶报警', '接打电话报警', '抽烟报警', '分神驾驶报警', '驾驶员异常报警', ]
        # print(sign)
        if self.alarm in ass_alarm_list:
            data_config.ASS_ALARM = ass_alarm_dict[self.alarm]
            # print(data_config.ASS_ALARM)
            appendData = self.getAssData()
        elif self.alarm in con_alarm_list:
            data_config.CON_ALARM = con_alarm_dict[self.alarm]
            # print(data_config.CON_ALARM)
            appendData = self.getConData()
        else:
            appendData = self.getRandomAppendData()
        return appendData

    def getRandomAppendData(self):
        data_list = ['Assistance', 'Condition']
        choice = random.choice(data_list)
        if choice == 'Condition':
            self.data = self.getConData()
        else:
            self.data = self.getAssData()
        return self.data

    # -----------高级驾驶辅助报警信息----------- #

    def getAssData(self):
        gaa = GPSInfoAppendAssistance(self.GPSList, self.dID)
        return gaa.getDrivingAssistanceData()

    # -----------驾驶员状态监测系统报警信----------- #
    def getConData(self):
        gac = GPSInfoAppendCondition(self.GPSList, self.dID)
        return gac.getDrivingConditionMonitor()

    # -----------胎压监测系统报警信息----------- #

    def setTirePressure(self, TIRE_PRESSURE):
        pass

    # ----------- 盲区监测系统报警信息----------- #
    def setBlindArea(self, BLIND_AREA):
        pass


if __name__ == '__main__':
    g = GPSInfoAppend([120.091645, 30.277906, 38, 9, 0, '疲劳驾驶报警'], '8888888')
    print('GPS测试附加信息:', g.getAppendData())
    # print(data_config.IS_ATTACH)
