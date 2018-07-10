# encoding=utf8
import sys
import argparse
from resources import av
from resources import common
from resources import kkm
from configparser import ConfigParser
from configparser import NoOptionError
from configparser import NoSectionError
class AntivirusArgParser(argparse.ArgumentParser):

    def __init__(self, *args, **kwargs):
        super(AntivirusArgParser, self).__init__(*args, **kwargs)

        self.__DEFAULT_SERVER = "<your_server>"
        self.__DEFAULT_DB = "your_db"
        self.__DEFAULT_MSG_FILE = "message"
        self.__DEFAULT_HOSTS_FILE = "hosts"
        self.config_file = "./common/config"

        self.add_argument("-f", "--hosts",
                          action='store',
                          dest='hosts_file',
                          help="Указывает на путь к файлу со списком усройств для которыхъ выполняется запрос на антивирус.")

        self.add_argument("-m", "--message",
                          action='store',
                          dest='message_file',
                          help="Указывает на файл с текстом сообщения, которое будет прикреплено к заявке.")

        self.add_argument("-d", "--dbserver",
                          action='store',
                          dest='server',
                          help="Указывает на  имя или адрес сервера БД Касперского для выгрузки логов.")


        self.add_argument("-b", "--base",
                          action='store',
                          dest='db',
                          help="Имя БД Касперского")

    def getArgs(self):
        return self.parse_args()

    def getConfig(self):
        config_parser = ConfigParser()
        config_parser.read(self.config_file)
        __config = {}

        try:
            __config["db"] = config_parser.get("db", "db")
        except NoOptionError or NoSectionError:
            pass

        try:
            __config['server'] = config_parser.get("db", "server")
        except NoOptionError or NoSectionError:
            pass

        try:
            __config['db_user'] = config_parser.get("db", "domain") + "\\" + config_parser.get("db", "user")
        except NoOptionError or NoSectionError:
            pass

        try:
            __config['db_pass'] = config_parser.get("db", "pass")
        except NoOptionError or NoSectionError:
            pass

        try:
            __config['message_file'] = config_parser.get("parser", "message")
        except NoOptionError or NoSectionError:
            pass

        try:
            __config['hosts_file'] = config_parser.get("parser", "hosts")
        except NoOptionError or NoSectionError:
            pass

        return __config

    def process(self):

        __config = self.getConfig()

        self.args = vars(self.parse_args())

        if self.args["db"]:              __config["db"] = self.args["db"]
        if self.args["server"]:          __config["server"] = self.args["server"]
        if self.args["message_file"]:    __config["message_file"] = self.args["message_file"]
        if self.args["hosts_file"]:      __config["hosts_file"] = self.args["hosts_file"]

        if not "db" in __config: __config["db"] = self.__DEFAULT_DB
        if not "server" in __config: __config["server"] = self.__DEFAULT_SERVER
        if not "message_file" in __config: __config["message_file"] = self.__DEFAULT_MSG_FILE
        if not "hosts_file" in __config: __config["hosts_file"] = self.__DEFAULT_HOSTS_FILE

        # без этих опций нельзя
        if "db_user" not in __config: print("Error. No user option specified. "); exit(-1)
        if "db_pass" not in __config: print("Error. No password  specified. "); exit(-1)

        antivirus = av.AvRequestCreator(db_user          = __config["db_user"],
                                        db_pwd           = __config["db_pass"],
                                        server           = __config["server"],
                                        DB               = __config["db"],
                                        message_file     = __config["message_file"])

        antivirus.crt_virus_scan_req(hosts_file=__config["hosts_file"])
        exit(0)

class AntivirusInstallArgParser(argparse.ArgumentParser):

    def __init__(self, *args, **kwargs):
        super(AntivirusInstallArgParser, self).__init__(*args, **kwargs)

        self.__DEFAULT_SERVER = "your_server"
        self.__DEFAULT_DB = "your_db"
        self.__DEFAULT_MSG_FILE = "message"
        self.__DEFAULT_HOSTS_FILE = "hosts"
        self.config_file = "./common/config"
        self.config_file_section_avinstall = 'avinstall'
        self.config_file_section_parser = 'parser'
        self.opt_severity = 'severity'
        self.opt_message_file = 'message'
        self.opt_hosts_file = 'hosts'

        self.add_argument("-f", "--hosts",
                          action='store',
                          dest=self.opt_hosts_file,
                          help="Указывает на путь к файлу со списком усройств для которыхъ выполняется запрос на антивирус.")

        self.add_argument("-m", "--message",
                          action='store',
                          dest=self.opt_message_file,
                          help="Указывает на файл с текстом сообщения, которое будет прикреплено к заявке.")


    def getConfig(self):
        config_parser = ConfigParser()
        config_parser.read(self.config_file)
        __config = {}

        try:
            __config[self.opt_severity] = config_parser.get(self.config_file_section_parser, self.opt_severity)
        except NoOptionError or NoSectionError:
            pass

        try:
            __config[self.opt_message_file] = config_parser.get(self.config_file_section_parser, self.opt_message_file)
        except NoOptionError or NoSectionError:
            pass

        try:
            __config[self.opt_hosts_file] = config_parser.get(self.config_file_section_parser, self.opt_hosts_file)
        except NoOptionError or NoSectionError:
            pass

        return __config

    def process(self):

        __config = self.getConfig()

        self.args = vars(self.parse_args())

        if not "db" in __config: __config["db"] = self.__DEFAULT_DB
        if not "server" in __config: __config["server"] = self.__DEFAULT_SERVER
        if not  self.opt_message_file in __config: __config[  self.opt_message_file] = self.__DEFAULT_MSG_FILE
        if not  self.opt_hosts_file in __config: __config[self.opt_hosts_file] = self.__DEFAULT_HOSTS_FILE

        # без этих опций нельзя
        if "db_user" not in __config: __config["db_user"] = ""
        if "db_pass" not in __config: __config["db_pass"] = ""
        if self.args[  self.opt_message_file]:    __config[self.opt_message_file] = self.args[self.opt_message_file]
        if self.args[ self.opt_hosts_file]:       __config[self.opt_hosts_file] = self.args[ self.opt_hosts_file]

        if not  self.opt_message_file in __config: __config[self.opt_message_file] = self.__DEFAULT_MSG_FILE
        if not  self.opt_hosts_file in __config: __config[self.opt_hosts_file] = self.__DEFAULT_HOSTS_FILE

        antivirus = av.AvRequestCreator(db_user          =__config["db_user"],
                                        db_pwd           =__config["db_pass"],
                                        server           =__config["server"],
                                        DB               =__config["db"],
                                        message_file      =   __config[self.opt_message_file])

        antivirus.crt_antivirus_install_req(hosts_file=__config[self.opt_hosts_file])
        exit(0)


class KkmChangeRequestCreator(argparse.ArgumentParser):

    def __init__(self, *args, **kwargs):
        super(KkmChangeRequestCreator, self).__init__(*args, **kwargs)
        self.config_file = "./common/config"
        self.__DEFAULT_EXP_DAYS = 30
        self.opt_csv_file = 'csv_file'
        self.opt_message_file = 'message_file'
        self.opt_expire_days = 'expire_days'
        self.opt_delim = 'delimeter'

        self.add_argument("-m", "--message",
                          action='store',
                          dest=self.opt_message_file,
                          help="Указывает на файл с текстом сообщения, которое будет прикреплено к заявке.")

        self.add_argument("--csv",
                          dest=self.opt_csv_file,
                          help="Путь у CSV файлу")

        self.add_argument("-e", "--expire-days",
                          action='store',
                          dest= self.opt_expire_days ,
                          help="")

        self.add_argument("--del",
                          action='store',
                          dest=self.opt_delim,
                          help="Разделитель CSV файла")


    def getConfig(self):
            config_parser = ConfigParser()
            config_parser.read(self.config_file)
            __config = {}

            try:
                __config[self.opt_message_file] = config_parser.get("parser",  self.opt_message_file)
            except NoOptionError or NoSectionError:
                pass

            try:
                __config[self.opt_csv_file] = config_parser.get("kkm", self.opt_csv_file)
            except NoOptionError or NoSectionError:
                pass

            try:
                __config[self.opt_csv_file] = config_parser.get("kkm", self.opt_expire_days)
            except NoOptionError or NoSectionError:
                pass

            return __config

    def process(self):

        __config = self.getConfig()

        self.args = vars(self.parse_args())

        # если есть значение переданное через аргументы, то оно имеет приоритет над тем, что прочтено из конфига
        if self.args[self.opt_message_file]:    __config[ self.opt_message_file] = self.args[self.opt_message_file]
        if self.args[self.opt_csv_file]:      __config[self.opt_csv_file] = self.args[self.opt_csv_file]
        #  проверим, является ли --expire-days целым числом.
        try: int( self.args[self.opt_expire_days])
        except ValueError or TypeError:
            print("Bad operand for -e. Must be integer")
            exit(-1)

        if self.args[self.opt_expire_days]:      __config[self.opt_expire_days] = self.args[self.opt_expire_days]

        # если параметр не передан ни через конфиг ни через параметры, используется дефолт
        if not self.opt_message_file in __config: __config[self.opt_message_file] = self.__DEFAULT_MSG_FILE
        if not self.opt_expire_days  in __config: __config[self.opt_expire_days] = self.__DEFAULT_EXP_DAYS

        ops = common.load_locations()
        k = kkm.kkm(__config[self.opt_csv_file], __config[self.opt_message_file], ops, int(__config[self.opt_expire_days]))
        expirings_kkm = k.end_is_near()
        for _kkm in expirings_kkm:
            k.request_kkm_change(_kkm[7], _kkm[9], _kkm[5], _kkm[2], _kkm[2].split(',')[0], _kkm[12])

        exit(0)
