import multiprocessing
from jt808.tools.get_data import GetData
import time

PATH_DATA = './config/data.ini'
data = GetData(PATH_DATA)

# 车辆信息文件路径
PATH_CAR = data.car_path

# GPS文件路径
PATH_GPS = data.gps_path

# Log文件路径
PATH_LOG = './config/log.ini'

# -----------基础信息----------- #
VEHICLE = ''
TRAVEL_END = 0

# 车辆颜色ID
COLOR = data.device_color
# 省域ID
PROVINCE = data.device_province  # 360426  江西省/九江市/德安县   因此应是0036 数据类型WORD  应转'0024'
# 市域ID
CITY = data.device_city  # 0426  数据类型WORD  应转'01AA'
# 制造商ID
MAKER = data.device_maker  # 五个字节，由大写字母和数字组成，此终端 ID 由制造商自行定义
# 终端型号
DEVICEMODEL = data.device_model  # 八个字节，此终端型号由制造商自行定义，位数不足八位的，补空格

# 测试用鉴权码 test_token
AUT = 'test_token'  # 鉴权码 STRING 终端重连后上报鉴权码

# -----------GPS信息----------- #
# 指定报警
ALARM = data.gps_alarm  # 无报警 目前报警标志位无用，报警只看附加位置信息
# ALARM = '11110000000000000000111111111111'  # 报警

# 制定状态
# ACC 开，定位，运营状态，油路正常，电路正常，车门加锁,GPS定位
STATE = data.gps_state

# 方向  0 ～359，正北为 0，顺时针
DIRECTION = data.gps_direction

# -----------终端通用应答----------- #
# 应答流水号
REPLY_NO = '0000'
# 应答 ID
REPLY_ID = '9208'
# 应答结果
REPLY_RESULT = 0  # 0：成功/ 确认；1：失败；2：消息有误；3：不支持

# -----------GPS附加信息----------- #
# 是否有附加信息
IS_ATTACH = 0
# 车辆状态
CAR_STATE = data.gps_append_CAR_STATE
# 报警标识号
SIGN = '32323333323030190924175400000100'
# 报警标识附件数量
ATTACH_SIGN = data.gps_append_ATTACH_SIGN  # 表示该报警对应的附件数量

# ----------- 报警附件信息消息数据----------- #
MSG_TYPE = data.gps_attachment_MSG_TYPE  # 信息类型0x00：正常报警文件信息 0x01：补传报警文件信息
# 文件类型  0x00：图片 0x01：音频 0x02：视频 0x03：文本 0x04：其它
ATTACH_TYPE = data.gps_attachment_type0
ATTACH_PATH = data.gps_attachment_path0

# 文件类型  0x00：图片 0x01：音频 0x02：视频 0x03：文本 0x04：其它
ATTACH_TYPE_01 = data.gps_attachment_type1
ATTACH_PATH_01 = data.gps_attachment_path1
# 文件类型  0x00：图片 0x01：音频 0x02：视频 0x03：文本 0x04：其它
ATTACH_TYPE_02 = data.gps_attachment_type2
ATTACH_PATH_02 = data.gps_attachment_path2
# 文件类型  0x00：图片 0x01：音频 0x02：视频 0x03：文本 0x04：其它
ATTACH_TYPE_03 = data.gps_attachment_type3
ATTACH_PATH_03 = data.gps_attachment_path3

# -----------高级驾驶辅助报警信息----------- #
# 报警 ID
ASS_ID = data.alarm_ass_id  # 按照报警先后，从 0 开始循环累加，不区分报警类型。
# 标志状态
ASS_STATE = data.alarm_ass_state  # 0x00：不可用 0x01：开始标志 0x02：结束标志
# 报警/事件类型
# 0x01：前向碰撞报警 0x02：车道偏离报警 0x03：车距过近报警 0x04：行人碰撞报警 0x06：道路标识超限报警
ASS_ALARM = data.alarm_ass_event
# 报警级别
ASS_LEVEL = data.alarm_ass_level  # 0x01：一级报警 0x02：二级报警
# 前车车速
# 单位 Km/h。范围 0~250，仅报警类型为 0x01 和 0x02 时有效。
ASS_F_SPEED = data.alarm_ass_front_speed
# 前车/行人距离
# 单位 100ms，范围 0~100，仅报警类型为 0x01、0x02 和0x04 时有效。
ASS_F_DISTANCE = data.alarm_ass_front_distance
# 偏离类型
ASS_DEVIATE = data.alarm_ass_deviate  # 0x01：左侧偏离 0x02：右侧偏离 仅报警类型为 0x02 时有效
# 道路标志识别类型
# 0x01：限速标志 0x02：限高标志 0x03：限重标志 仅报警类型为 0x06 和 0x10 时有效
ASS_ROAD_SIGN = data.alarm_ass_road_sign

# -----------驾驶员状态监测系统报警信----------- #
# 报警 ID
CON_ID = data.alarm_con_id  # 按照报警先后，从 0 开始循环累加，不区分报警类型。
# 标志状态
CON_STATE = data.alarm_con_state  # 0x00：不可用 0x01：开始标志 0x02：结束标志
# 报警/事件类型
# 0x01:疲劳驾驶报警 0x02:接打电话报警 0x03:抽烟报警 0x04:分神驾驶报警 0x05:驾驶员异常报警
CON_ALARM = data.alarm_con_event
# 报警级别
CON_LEVEL = data.alarm_ass_level  # 0x01：一级报警 0x02：二级报警
# 疲劳程度
CON_WEARY = data.alarm_con_weary  # 范围 1~10。数值越大表示疲劳程度越严重，仅在报警类型为 0x01 时有效

# -----------胎压监测系统报警信息----------- #
TIRE_PRESSURE = ['0' for tp in range(92)]

# ----------- 盲区监测系统报警信息----------- #
BLIND_AREA = ['0' for ba in range(74)]


# -----------GUI信息----------- #
START_TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

# -----------多进程信息----------- #
gps_count = multiprocessing.Value('L', 0)
hear_count = multiprocessing.Value('L', 0)
online_car = multiprocessing.Value('L', 0)
bytes_count = multiprocessing.Value('L', 0)
send_fail = multiprocessing.Value('L', 0)

# -----------多线程信息----------- #
GPS = 0
HEART = 0
ATTACHMENT = 0
ONLINE = 0
BYTES = 0
FAIL = 0

if __name__ == '__main__':
    print(ALARM)
    print(STATE)
    print(PATH_CAR)
    # gd = GetData('../../config/data.ini')
    # print(gd.car_path)
