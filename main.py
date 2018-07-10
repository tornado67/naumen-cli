# encoding=utf8
import os
import pprint
import logging
import argparse
from resources.kkm import kkm
from resources import av
from resources import common
from resources.api_engine import ApiEngine
from configparser import ConfigParser
from configparser import NoOptionError
from configparser import NoSectionError
# сообщения логера

__version__ = "1.1"

WRONG_HOSTNAME = "Failed to create request for host {}. wrong hostname"
NO_EVENTS = "No events found in {} for host {}"
NO_OPTION = "No {} options specified. using defaults: {}"
NO_OPTION_FATAL = "Fatal: No required option specified via parameter not via config file: {}"
TICKET_CREATED = "Ticket created with uuid: {}"
FILE_ADDED = "File {} added to ticket {}"

HOSTS_FILE_OVERLOADED = "hosts file is overloaded via -f option. using overloaded: {}"
MESSAGE_FILE_OVERLOADED = "message file was overloaded via -m option. using overloaded: {}"
DATABASE_OVERLOADED = "database name overloaded via -b option. using overloaded: {}"
DB_SERVER_OVERLOADED = "database server address overloaded via -d option. using overloaded: {}"
CUSTOM_FUNC_CALLED = "called custom function: {}"
CONFIG_OVERLOADED = "config file overloaded via -c function. using overloaded: {}"
BAD_OPERAND = "error: abd operand for {}: {}"



# Значения по-умолчанию для сервера БД Касперского.
__DEFAULT_SERVER = "r61avpdb02"
__DEFAULT_DB = "KAV"
# дефолтные файлы hosts и message
__DEFAULT_MSG_FILE = "message"
__DEFAULT_HOSTS_FILE = "hosts"
# инициализируем логер
logging.basicConfig(filename='naumen.log', level=logging.DEBUG)
api_engine = ApiEngine()

# отокрываем конфигурационный файл и чиатем настройки БД

DB = ""
server = ""
message_file = ""
hosts_file = ""
config_file = "common/config"
kkm_csv_file = "csv.csv"
# парсинг аргментов скрипта
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--hosts",       action='store',         dest='hosts_file', help="Указывает на путь к файлу со списком усройств для которыхъ выполняется запрос на антивирус.")
parser.add_argument("-m", "--message",     action='store',       dest='message_file', help="Указывает на файл с текстом сообщения, которое будет прикреплено к заявке.")
parser.add_argument("-d", "--dbserver",    action='store',      dest='db_server', help="Указывает на  имя или адрес сервера БД Касперского для выгрузки логов.")
parser.add_argument("-b", "--base",        action='store',          dest='base', help="Имя БД Касперского")
parser.add_argument("-c", "--config",      action='store',        dest='config', help="Указывает на файл конфигураии")
parser.add_argument("-F", "--function",    action='store',      dest='function', help="call custom API fucntion")
parser.add_argument("-k","--kkm",          action='store_true',      dest='kkm', help="создание заявок по ККМ на основе csv файла")
parser.add_argument("-a","--antivirus",    action='store_true', dest='av', help="Операции с антивирусом. По умолчанию -  проверка устройства на вирусы")
parser.add_argument("-ai","--antivirus-installation", action='store_true', dest='ai',help="Запрос на установку антивируса")
parser.add_argument("--del", action='store', dest='delim', help="Разделитель CSV файла")
parser.add_argument("--csv", action='store', dest='csv', help="")
parser.add_argument("-e","--expire-days", action='store', dest='days', help="")



# аргументы переданные опциями имеют приоритет над конфигурационным файлом даже если он передан через опцию -c.
args = parser.parse_args()

if args.function is not None:
    if args.args is not None:
        _function = getattr(api_engine, args.function)()(args.args)
        pprint.pprint(_function())
        exit()
    _function = getattr(api_engine, args.function)
    logging.info(CUSTOM_FUNC_CALLED.format(args.function))
    pprint.pprint(_function())
    exit()


# создание запроса на антивирь.
if args.av is not None:
    if args.hosts_file is not None:
        logging.info(HOSTS_FILE_OVERLOADED.format(os.path.abspath(hosts_file)))
        hosts_file = args.hosts_file

    if args.message_file is not None:
        logging.info(MESSAGE_FILE_OVERLOADED.format(os.path.abspath(message_file)))
        message_file = args.message_file

    if args.db_server is not None:
        logging.info(DB_SERVER_OVERLOADED.format(args.db_server))
        server = args.db_server

    if args.base is not None:
        logging.info(DATABASE_OVERLOADED.format(args.base))
        DB = args.base

    if args.config is not None:
        logging.info(CONFIG_OVERLOADED.format(args.config))
        config_file = args.config

    config = ConfigParser()
    config.read(config_file)

    try:
        if args.base is None:
            DB = config.get("db", "db")
    except NoOptionError or NoSectionError:
        DB = __DEFAULT_DB
        logging.info(NO_OPTION.format("DB", __DEFAULT_DB))

    try:
        if args.db_server is None:
            server = config.get("db", "dbserver")
    except NoOptionError or NoSectionError:
        server = __DEFAULT_SERVER
        logging.info(NO_OPTION.format("server", __DEFAULT_SERVER))

    try:
        if args.message_file is None:
            message_file = config.get("parser", "message")
    except NoOptionError or NoSectionError:
        message_file = __DEFAULT_MSG_FILE
        logging.info(NO_OPTION.format("message", __DEFAULT_MSG_FILE))

    try:
        if args.hosts_file is None:
            hosts_file = config.get("parser", "hosts")
    except NoOptionError or NoSectionError:
        hosts_file = __DEFAULT_HOSTS_FILE
        logging.info(NO_OPTION.format("hosts", __DEFAULT_HOSTS_FILE))
    # создаем класс отвечающий за создание запроса.
    antivirus = av.AvRequestCreator(db_user=config.get("db", "domain") + "\\" + config.get("db", "user"),
                                    db_pwd=config.get("db", "pass"), server=server, DB=DB, mesage_file=message_file)

    # если флаг "запрос на установку антивируса"  установлен
    try:
        if args.ai is not None:
            antivirus.create_antivirus_install_request(hosts_file=hosts_file)
            exit()
    except NoOptionError:
        pass

    # в случае если флаг "запрос на установку антивируса НЕ установлен, выполняется стандартный запрос на проверку антивирусом.
    antivirus.crt_virus_scan_req(hosts_file=hosts_file)

    exit()

if args.kkm:

    if args.days is not None:
        try:
            days = int(args.days)
        except ValueError or TypeError:
            print("Bad operand for -e. Must be integer")
            logging.error(BAD_OPERAND.format("-e", args.days))
            exit(-1)

    if args.csv is not None:
        kkm_csv_file = args.csv
    else:
        try:
            kkm_csv_file = config.get("kkm", "csv")
        except NoOptionError or NoSectionError or KeyError:
            logging.error(NO_OPTION_FATAL.format("--csv"))
            print(NO_OPTION_FATAL.format("--csv"))
            exit(-1)
    ops = common.load_locations()

    if args.delim is not None:
        k = kkm(kkm_csv_file, args.delim,  ops, days)
    else:
        k = kkm(kkm_csv_file,  message_file, ops, days)
        e = k.end_is_near()
    for _kkm in e:
        k.request_kkm_change(_kkm[7], _kkm[9], _kkm[5], _kkm[2], _kkm[2].split(',')[0], _kkm[12])

