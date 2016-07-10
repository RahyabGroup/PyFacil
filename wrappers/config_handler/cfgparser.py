from configparser import ConfigParser

__author__ = 'Amir H. Nejati'


class CfgParser:
    _parser = None
    _section = None
    _option = None
    _file_path = None

    def __init__(self, file_path):
        self._parser = ConfigParser(allow_no_value=True)
        self._parser.read(file_path, encoding='utf-8')
        self._file_path = file_path

    def sec(self, sec_name):
        self._section = sec_name
        return self

    def opt(self, opt_name):
        self._option = opt_name
        return self

    def get(self, opt_type=str):
        opt_selector = {str: self._parser.get, int: self._parser.getint, bool: self._parser.getint,
                        float: self._parser.getfloat}
        return opt_selector[opt_type](self._section, self._option)

    def set(self, value=None):
        self._parser.set(self._section, self._option, value)
        with open(self._file_path, 'w') as conf_file:
            self._parser.write(conf_file)

    def options(self):
        return self._parser.options(self._section)
