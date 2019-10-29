# 鉴权

from jt808.tools import tools, data_config


class Authentication:
    def __init__(self):
        self.t = tools.Tools()
        self.autID = data_config.AUT

    def getData(self):
        self.strHex = self.t.StrToHex(self.autID)
        return self.strHex


if __name__ == '__main__':
    a = Authentication()
    print('鉴权测试：', a.getData())
