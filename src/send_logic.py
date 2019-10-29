import time
import os
import sys
from socket import *
from src import send, send_attach_logic
from jt808.tools import data_config
from src.excel_data import ExcelData
from src.recv import Recv


# PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(PATH)


class MainLogic:

    def __init__(self, ip, port):
        self.ed = ExcelData()
        self.ip = ip
        self.port = port
        self.path_gps = data_config.PATH_GPS
        self.socketInit()

    def socketInit(self):
        try:
            self.tcp = socket(AF_INET, SOCK_STREAM)
            self.tcp.connect_ex((self.ip, self.port))
            self.recv = Recv(self.tcp)
            print('{}连接成功...'.format(self.tcp.getsockname()))
        except BaseException:
            print('无法连接！！！')
            return -1

        self.GPSList = self.ed.getGPSList(self.path_gps)
        self.regList = []

    # 注册逻辑
    def reg_logic(self, each_car):
        self.vehicleList = each_car
        try:
            self.sends = send.Send(self.vehicleList[0],
                                   self.vehicleList[1],
                                   self.vehicleList[2],
                                   self.tcp)
            self.regList.append(self.sends)
            self.sends.sendReg()
            data_config.ONLINE += 1
            result = self.recv.registerMsg()  # 接收消息
            if result[0] == 0:
                print('# ----------- 注册成功 ----------- #')
                aut_code = result[1]  # 返回鉴权码
                data_config.AUT = aut_code
                print('返回鉴权码: ', aut_code)

                # 注册完成后要发送一次鉴权
                print('# ----------- 发送鉴权 ----------- #')
                self.sends.sendAut()

            else:
                print('# ----------- 注册失败 ----------- #')
                print('失败原因: ', result[1])
                self.tcp.close()

        except BaseException:
            print('# ----------- 连接失败 ----------- #')

    # 心跳逻辑
    # 判断心跳应答结果，如果失败则发送鉴权
    def heart_logic(self):
        try:
            self.sends.sendHeart()
            result = self.recv.commonMsg()  # 接收消息
            if result == 0:
                print('# ----------- keep heart ----------- #')
        except BaseException as e:
            print(e)
            print('# ----------- 发送鉴权 ----------- #')
            self.sends.sendAut()

    # GPS逻辑
    def GPS_logic(self):
        self.gpsIndex = 0
        while self.gpsIndex < len(self.GPSList):
            try:
                print('# ----------- 发送GPS ----------- #')
                print(self.GPSList[self.gpsIndex])
                self.sends.sendGPS(self.GPSList[self.gpsIndex])
                result = self.recv.commonMsg()  # 接收消息
                time.sleep(1)
                if result == 0:
                    if data_config.IS_ATTACH == 1:
                        upload_ip, upload_port = self.recv.uploadMsg()  # 接收消息
                        print('# ----------- 发送附加信息 ----------- #')
                        sa = send_attach_logic.AttachLogic(
                            upload_ip, upload_port, self.vehicleList)
                        sa.run()
                data_config.GPS += 1
                self.heart_logic()
                data_config.HEART += 1
                self.gpsIndex += 1
                time.sleep(1)
            except ConnectionAbortedError as e:
                print(e)
                print('正在尝试重新连接...')
                self.socketInit()
                self.heart_logic()
                data_config.HEART += 1
        # 发送行程截止GPS，再次发送最后一个GPS定位，ACC关闭
        data_config.STATE = '00000000000000100000100000000010' # ACC关闭
        self.sends.sendGPS(self.GPSList[-1])
        print('# ----------- ACC关闭 ----------- #')

        # self.sends.sendLogout()  # 注销逻辑无用

    # 断开连接
    def stop(self):
        # 发送行程截止GPS，再次发送最后一个GPS定位，ACC关闭
        data_config.STATE = '00000000000000100000100000000010' # ACC关闭
        self.sends.sendGPS(self.GPSList[-1])
        print('# ----------- ACC关闭 ----------- #')
        self.tcp.close()
        print('# ----------- 停止程序 ----------- #')



if __name__ == '__main__':
    path_car = data_config.PATH_CAR
    path_gps = data_config.PATH_GPS
    t = MainLogic('192.168.1.192', 1077)
    # t = MainLogic('sentryward.wxb.com.cn', 1077)  # 正式
    print(t.GPSList)
    ed = ExcelData()
    carList = ed.getCarList(path_car)
    print(carList)
    each_car = carList[0]
    print(len(t.GPSList))
    # print(t.GPSList[-1])
    t.reg_logic(each_car)
    t.heart_logic()
    t.GPS_logic()
    t.tcp.close()
    # ed = ExcelData()
    # GPSList = ed.getGPSList(path_gps)
    # print(GPSList)
