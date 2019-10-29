from configparser import ConfigParser
import threading


class GetData(object):
    def __init__(self, data_config):
        pass

    def __new__(cls, data_config):
        mutex = threading.Lock()
        mutex.acquire()  # 上锁，防止多线程下出问题
        if not hasattr(cls, 'instance'):
            cls.instance = super(GetData, cls).__new__(cls)
            config = ConfigParser()
            config.read(data_config, encoding='UTF-8')
            # print(config.sections())
            cls.instance.car_path = config.get('FILE', 'PATH_CAR')
            cls.instance.gps_path = config.get('FILE', 'PATH_GPS')

            cls.instance.device_color = config.get('BASE', 'COLOR')
            cls.instance.device_province = config.get('BASE', 'PROVINCE')
            cls.instance.device_city = config.get('BASE', 'CITY')
            cls.instance.device_maker = config.get('BASE', 'MAKER')
            cls.instance.device_model = config.get('BASE', 'DEVICEMODEL')

            cls.instance.gps_alarm = config.get('GPS', 'ALARM')
            cls.instance.gps_state = config.get('GPS', 'STATE')
            cls.instance.gps_direction = config.getint('GPS', 'DIRECTION')

            cls.instance.gps_append_CAR_STATE = config.get(
                'GPS_ATTACH', 'CAR_STATE')
            cls.instance.gps_append_ATTACH_SIGN = config.getint(
                'GPS_ATTACH', 'ATTACH_SIGN')

            cls.instance.gps_attachment_MSG_TYPE = config.get(
                'ATTACHMENT', 'MSG_TYPE')
            cls.instance.gps_attachment_type0 = config.get(
                'ATTACHMENT', 'ATTACH_TYPE')
            cls.instance.gps_attachment_path0 = config.get(
                'ATTACHMENT', 'ATTACH_PATH')
            cls.instance.gps_attachment_type1 = config.get(
                'ATTACHMENT', 'ATTACH_TYPE_01')
            cls.instance.gps_attachment_path1 = config.get(
                'ATTACHMENT', 'ATTACH_PATH_01')
            cls.instance.gps_attachment_type2 = config.get(
                'ATTACHMENT', 'ATTACH_TYPE_02')
            cls.instance.gps_attachment_path2 = config.get(
                'ATTACHMENT', 'ATTACH_PATH_02')
            cls.instance.gps_attachment_type3 = config.get(
                'ATTACHMENT', 'ATTACH_TYPE_03')
            cls.instance.gps_attachment_path3 = config.get(
                'ATTACHMENT', 'ATTACH_PATH_03')

            cls.instance.alarm_ass_id = config.get('ALARM_ASS', 'ASS_ID')
            cls.instance.alarm_ass_state = config.get('ALARM_ASS', 'ASS_STATE')
            cls.instance.alarm_ass_event = config.get('ALARM_ASS', 'ASS_ALARM')
            cls.instance.alarm_ass_level = config.get('ALARM_ASS', 'ASS_LEVEL')
            cls.instance.alarm_ass_front_speed = config.getint(
                'ALARM_ASS', 'ASS_F_SPEED')
            cls.instance.alarm_ass_front_distance = config.getint(
                'ALARM_ASS', 'ASS_F_DISTANCE')
            cls.instance.alarm_ass_deviate = config.get(
                'ALARM_ASS', 'ASS_DEVIATE')
            cls.instance.alarm_ass_road_sign = config.get(
                'ALARM_ASS', 'ASS_ROAD_SIGN')

            cls.instance.alarm_con_id = config.get('ALARM_CON', 'CON_ID')
            cls.instance.alarm_con_state = config.get('ALARM_CON', 'CON_STATE')
            cls.instance.alarm_con_event = config.get('ALARM_CON', 'CON_ALARM')
            cls.instance.alarm_con_level = config.get('ALARM_CON', 'CON_LEVEL')
            cls.instance.alarm_con_weary = config.get('ALARM_CON', 'CON_WEARY')

        mutex.release()
        return cls.instance

if __name__ == '__main__':
    PATH_DATA = '../../config/data.ini'
    data = GetData(PATH_DATA)
    path = data.car_path
    print(path)