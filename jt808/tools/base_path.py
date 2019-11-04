from pathlib import Path
import logging


class BasePath:

    def __init__(self):
        # 当前工作路径：
        self.work_dir = Path.cwd()
        # home路径
        self.home_dir = Path.home()
        # 当前文件绝对路径
        self.abs_dir = Path(__file__)
        # 项目Base路径
        self.base_dir = self.abs_dir.parent.parent.parent

    # 路径拼接:项目路径+path
    def joinPath(self, path):
        p = Path(path)
        if p.is_file():
            return path
        else:
            try:
                DIR = self.base_dir / path
                return DIR
            except BaseException as i:
                logging.error(i)


if __name__ == '__main__':
    bp = BasePath()
    print(bp.work_dir)
    print(bp.home_dir)
    print(bp.abs_dir)
    print(bp.base_dir)
    print(bp.joinPath('./car/test.xls'))
    print(bp.joinPath(r'H:\灵犀金融\\test\jtt808DataBuilder\car\\test.xls'))
