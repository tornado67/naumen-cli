import pymssql
import logging
import datetime
from os import remove
from resources.ticket import Ticket
from resources import common
from itertools import groupby
from resources.api_engine import ApiEngine
from multipledispatch import dispatch


class AvRequestCreator:
    __regions = ['R61', 'R68', 'R31', 'R34', 'R36', 'R48', 'R46', 'R23', 'R01']
    __region_indexes = {'R61': '344700', 'R68': '392700', 'R31': '308700', 'R34': '400700', 'R36': '394700',
                      'R48': '398700', 'R46': '305700', 'R23': '350700', 'R01': '385700'}

    api_engine = ApiEngine()
    logging.basicConfig(filename='naumen.log', level=logging.DEBUG)
    __FILE_ADDED = "File {} added to ticket {}"
    __NO_EVENTS = "No events found in {} for host {}"
    __TICKET_CREATED = "Ticket created with uuid: {}"
    __WRONG_HOSTNAME = "Failed to create request for host {}. wrong hostname"
    __NO_CREDENTIALS = "No credentials specified fo DB connection. Using defaults."
    # запрос который выбирает и базы Касперского события по хосту.
    __query = """use KAV;
    select convert(nvarchar,registration_time), 
           host_display_name, 
           task_display_name, 
           event_type_display_name, 
           descr 
    from ev_event where 
        host_display_name like %s
        and rise_time > convert( datetime, '{}' ,103)  order by rise_time;
    """
    # конструктор получает пользователя БД, его пароль, имя БД, файл с  тектсом сообщения


    #@dispatch(str, str, str, str, str)
    def __init__(self, db_user, db_pwd, server, DB, message_file):
        self.user   = db_user
        self.passwd = db_pwd
        self.DB     = DB
        self.server = server
        self.message_file = message_file
        self.api_engine = ApiEngine()




    # Функция выгружает события из БД касперского
    def create_log(self, host):
        # подключаемся к БД
        con = pymssql.connect(server=self.server, user=self.user, password=self.passwd, database=self.DB)
        # время нужно для выгрузи событий за период от "сейчас" - 3дня.
        now = datetime.datetime.now()
        #con = pymssql.connect(server=self.server, user=domain + "\\" + user, password=passwd, database=self.DB)
        try:

            cursor = con.cursor()
            # выполняем запрос подставляя нужные значения.
            cursor.execute(self.__query.format((now - datetime.timedelta(days=3)).strftime("%d/%m/%Y")), host)
            # если не получили событий то пишем в лог.
            if cursor.rowcount == 0:
                logging.debug(self.NO_EVENTS.format(self.server + "/" + self.DB, host))
                return -1
            # Если нет создаем файл с имением хоста и вносим в него логи.
            else:
                with open(host + ".txt", 'w') as file:
                    for row in cursor:
                        file.write(str(row).replace("(", "").replace(")", "").replace("'", "") + "\n")
                    return 0
        finally:
            con.close()

    def crt_virus_scan_req(self, hosts_file):
        ops = common.load_locations()
        with open(hosts_file) as file:
            hosts = [row.strip() for row in file]

        hosts = [el for el, _ in groupby(hosts)]
        for host in hosts:
            if host.find("-") == 3:
                index = host[host.find('-') + 1:][:6]
                if index.isnumeric():
                    with open(self.message_file) as message:
                        descriptionInRTF = message.read().format(host=host)
                    t = Ticket("service$20260901", 'service$23576410', 'catalogs$37027901',
                               descriptionInRTF, 'employee$405802127', 'employee$405802127',
                               ops[index]['uuid'], ops[index]['uuid'])

                    if self.create_log(host) == 0:
                        req_uuid = self.api_engine.create_request(t)['UUID']
                        logging.info(self.__TICKET_CREATED.format(req_uuid))
                        logging.info(self.__FILE_ADDED.format(
                            self.api_engine.add_file_to_object(host + ".txt", req_uuid), req_uuid))
                        remove(host + ".txt")
                else:
                    logging.debug(self.__WRONG_HOSTNAME.format(host))

            elif host[:3].upper() in self.__regions:
                with open(self.message_file, 'r') as message:
                    descriptionInRTF = message.read().format(host)

                t = Ticket("service$20260901", 'service$23576410', 'catalogs$37027901',
                           descriptionInRTF, 'employee$405802127', 'employee$405802127',
                           ops[self.__region_indexes[host[:3].upper()]]['uuid'],
                           ops[self.__region_indexes[host[:3].upper()]]['uuid'])
                if self.create_log(host) == 0:
                    req_uuid = self.api_engine.create_request(t)['UUID']
                    logging.info(self.__TICKET_CREATED.format(req_uuid))
                    logging.info(self.__FILE_ADDED.format(
                        self.api_engine.add_file_to_object(host + ".txt", req_uuid), req_uuid))
                    remove(host + ".txt")

            else:
                logging.error(self.__WRONG_HOSTNAME.format(host))
                continue

    def crt_antivirus_install_req(self,hosts_file):
        ops = common.load_locations()
        with open(hosts_file) as file:
            hosts = [row.strip() for row in file]

        hosts = [el for el, _ in groupby(hosts)]
        for host in hosts:
            if host.find("-") == 3:
                index = host[host.find('-') + 1:][:6]
                if index.isnumeric():
                    with open(self.message_file) as message:
                        descriptionInRTF = message.read().format(host=host)
                    t = Ticket("service$20260901", 'service$23576410', 'catalogs$37027901',
                               descriptionInRTF, 'employee$405802127', 'employee$405802127',
                               ops[index]['uuid'], ops[index]['uuid'])

                    print(self.api_engine.create_request(t)['UUID'])

            elif host[:3].upper() in self.__regions:
                with open(self.message_file, 'r') as message:
                    descriptionInRTF = message.read().format(host=host)

                t = Ticket("service$20260901", 'service$23576410', 'catalogs$37027901',
                           descriptionInRTF, 'employee$405802127', 'employee$405802127',
                           ops[self.__region_indexes[host[:3].upper()]]['uuid'],
                           ops[self.__region_indexes[host[:3].upper()]]['uuid'])
                if self.create_log(host) == 0:
                    req_uuid = self.api_engine.create_request(t)['UUID']
                    logging.info(self.__TICKET_CREATED.format(req_uuid))
                    logging.info(self.__FILE_ADDED.format(
                        self.api_engine.add_file_to_object(host + ".txt", req_uuid), req_uuid))
                    remove(host + ".txt")

            else:
                logging.error(self.__WRONG_HOSTNAME.format(host))
                continue




