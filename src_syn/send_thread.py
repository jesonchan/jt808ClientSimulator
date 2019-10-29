from src_syn import send_logic_syn, excel_data
from jt808.tools import data_config
from threading import Thread


# 主流程线程
class SendThread:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.path_car = data_config.PATH_CAR
        self.ed = excel_data.ExcelData()
        self.send = send_logic_syn.MainLogic(self.ip, self.port)

    # 断开连接
    def stop(self):
        self.send.stop()

    # 开启线程
    def startThread(self):
        carList = self.ed.getCarList(self.path_car)
        each_car = carList[0]
        print(each_car)
        t = Thread(target=self.send.send_thread, args=(each_car,))
        t.setDaemon(True)
        t.start()


if __name__ == '__main__':
    st = SendThread('192.168.1.192', 1077)
    st.startThread()
    # time.sleep(2)
    # st.stop()
