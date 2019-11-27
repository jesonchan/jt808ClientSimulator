import time
from socket import *
from src import send
from jt808.tools import data_config, tools, logs
from src.excel_data import ExcelData
from src.recv import RecvLogic
from threading import Thread, Event, current_thread
from queue import Queue

log = logs.Log(data_config.PATH_LOG)
logger = log.get_logger()


class MainLogic:

    def __init__(self, ip, port):
        self.ed = ExcelData()
        self.ip = ip
        self.port = port
        self.path_gps = data_config.PATH_GPS
        self.socketInit()
        self.t = tools.Tools()
        self.rl = RecvLogic()

    def socketInit(self):
        try:
            self.tcp = socket(AF_INET, SOCK_STREAM)
            self.tcp.connect_ex((self.ip, self.port))
            logger.info('{}连接成功...'.format(self.tcp.getsockname()))
        except BaseException:
            logger.info('无法连接！！！')
            return -1

        self.GPSList = self.ed.getGPSList(self.path_gps)
        self.regList = []

    # 接收应答消息队列
    def recv_queue(self, q):
        while True:
            q.put(self.tcp.recv(1024))

    # send主流程
    def run(self, each_car, e):
        data_config.VEHICLE = each_car
        self.reg_logic(e)
        self.heart_logic(e)
        self.GPS_logic(e)
        data_config.TRAVEL_END = 1

    # 终端应答流程
    def client_response(self, response_q):
        while True:
            res = response_q.get()
            if res == '8300':
                self.sends.sendClinetCommonReply()
            elif res == '9101':
                self.sends.sendClinetCommonReply()

    # 线程管理
    def send_thread(self, each_car):
        q = Queue()  # client消息接收队列
        e = Event()
        response_q = Queue()  # 终端应答队列
        # thread_list = []
        # send线程
        thread_send = Thread(target=self.run, args=(each_car, e))
        thread_send.start()
        # recv队列线程
        thread_recv_queue = Thread(
            target=self.recv_queue, args=(q,))
        thread_recv_queue.setDaemon(True)
        thread_recv_queue.start()
        # 读取recv线程
        thread_recv = Thread(
            target=self.rl.recv_logic, args=(q, e, response_q,))
        thread_recv.setDaemon(True)
        thread_recv.start()
        # client应答线程
        thread_recv = Thread(
            target=self.client_response, args=(response_q,))
        thread_recv.setDaemon(True)
        thread_recv.start()
        thread_send.join()
        logger.info('主线程结束了！%s' % current_thread().name)

    # 注册逻辑

    def reg_logic(self, e):
        self.vehicleList = data_config.VEHICLE
        try:
            self.sends = send.Send(self.vehicleList[0],
                                   self.vehicleList[1],
                                   self.vehicleList[2],
                                   self.tcp)
            self.regList.append(self.sends)
            self.sends.sendReg()
            data_config.ONLINE += 1
            if e.is_set() == False:  # 阻塞
                logger.info('等待应答')
                e.wait()

            logger.info('# ----------- 发送鉴权 ----------- #')
            self.sends.sendAut()
            e.clear()
            if e.is_set() == False:  # 阻塞
                logger.info('等待应答')
                e.wait()

        except BaseException as i:
            logger.error(i)
            logger.info('# ----------- 连接失败 ----------- #')

    # 心跳逻辑
    # 判断心跳应答结果，如果失败则发送鉴权
    def heart_logic(self, e):
        try:
            self.sends.sendHeart()
            e.clear()
            if e.is_set() == False:  # 阻塞
                logger.info('等待应答')
                e.wait()
            data_config.HEART += 1

        except BaseException as i:
            logger.error(i)
            logger.info('# ----------- 发送鉴权 ----------- #')
            self.sends.sendAut()

    # GPS逻辑
    def GPS_logic(self, e):
        gpsIndex = 0
        while gpsIndex < len(self.GPSList):
            try:
                logger.info('# ----------- 发送GPS ----------- #')
                logger.info(self.GPSList[gpsIndex])
                self.sends.sendGPS(self.GPSList[gpsIndex])

                e.clear()
                if e.is_set() == False:  # 阻塞
                    logger.info('等待应答')
                    e.wait()
                data_config.GPS += 1
                time.sleep(1)
                self.heart_logic(e)
                gpsIndex += 1

            except ConnectionAbortedError as i:
                logger.error(i)
                logger.info('正在尝试重新连接...')
                self.socketInit()
                self.heart_logic(e)
                data_config.HEART += 1
        # 发送行程截止GPS，再次发送最后一个GPS定位，ACC关闭
        data_config.STATE = '00000000000000100000100000000010'  # ACC关闭
        self.sends.sendGPS(self.GPSList[-1])
        logger.info('# ----------- 行程结束ACC关闭 ----------- #')

        # self.sends.sendLogout()  # 注销逻辑无用

    # 断开连接
    def stop(self):
        # 发送行程截止GPS，再次发送最后一个GPS定位，ACC关闭
        data_config.STATE = '00000000000000100000100000000010'  # ACC关闭
        self.sends.sendGPS(self.GPSList[-1])
        self.tcp.close()
        logger.info('# ----------- 停止程序 ----------- #')


if __name__ == '__main__':
    path_car = data_config.PATH_CAR
    ed = ExcelData()
    carList = ed.getCarList(path_car)
    print(carList)
    each_car = carList[0]
    # t = MainLogic('192.168.1.192', 1077)
    t = MainLogic('carstest.wxb.com.cn', 1077)
    # t = MainLogic('sentryward.wxb.com.cn', 1077)  # 正式
    t.send_thread(each_car)
