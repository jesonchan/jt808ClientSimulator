from src import send_logic, excel_data
from jt808.tools import data_config
from threading import Thread, Event


# 主流程线程
class SendThread:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.path_car = data_config.PATH_CAR
        self.ed = excel_data.ExcelData()
        self.send = send_logic.MainLogic(self.ip, self.port)

    # 断开连接
    def stop(self):
        self.send.stop()

    def run(self, each_car):
        self.send.reg_logic(each_car)
        self.send.heart_logic()
        self.send.GPS_logic()
        data_config.TRAVEL_END = 1

    # 开启线程
    def startThread(self):
        carList = self.ed.getCarList(self.path_car)
        each_car = carList[0]
        print(each_car)
        t = Thread(target=self.run, args=(each_car,))
        t.setDaemon(True)
        t.start()


if __name__ == '__main__':
    eEnd = Event()
    st = SendThread('192.168.1.192', 1077)
    st.startThread()
    # time.sleep(2)
    # st.stop()
