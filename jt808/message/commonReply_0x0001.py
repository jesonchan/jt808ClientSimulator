from jt808.tools import tools, data_config


class CommonReply:
    def __init__(self):
        self.ID = data_config.REPLY_ID  # 应答ID
        self.NO = data_config.REPLY_NO  # 应答流水号
        self.result = data_config.REPLY_RESULT  # 应答结果
        self.t = tools.Tools()

    def getData(self):
        self.data = self.NO + self.ID + self.t.IntToHex(self.result, 2)
        return self.data


if __name__ == '__main__':
    cr = CommonReply()
    print(cr.getData())
