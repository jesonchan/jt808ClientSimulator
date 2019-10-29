import os
import sys

import xlrd


class ExcelData:

    def getCarList(self, filepath):
        vehicleList = []
        try:
            table_vehicle = xlrd.open_workbook(filepath).sheets()[0]
            for each in range(1, table_vehicle.nrows):
                if table_vehicle.row_values(
                        each)[0] == '' or table_vehicle.row_values(each)[1] == '':
                    continue
                vehicleList.append([table_vehicle.row_values(each)[3],
                                    table_vehicle.row_values(each)[1],
                                    table_vehicle.row_values(each)[2]])
        except IOError:
            print('读取表错误!')
        return vehicleList

    def getGPSList(self, filepath):
        GPSList = []
        try:
            table_gps = xlrd.open_workbook(filepath).sheets()[0]
            for each in range(1, table_gps.nrows):
                if table_gps.row_values(
                        each)[0] == '' or table_gps.row_values(each)[1] == '':
                    continue
                GPSList.append([table_gps.row_values(each)[0],
                                table_gps.row_values(each)[1],
                                int(table_gps.row_values(each)[2]),
                                int(table_gps.row_values(each)[3]),
                                int(table_gps.row_values(each)[4])])
        except IOError:
            print('读取表错误!')
        return GPSList


if __name__ == '__main__':
    PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(PATH)
    path_car = PATH + r'\car\test.xls'
    path_gps = PATH + r'\gps\gps_test0.xls'
    oe = ExcelData()
    print(oe.getGPSList(path_gps))
    print(oe.getCarList(path_car))
