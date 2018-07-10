import csv
import datetime
from resources.ticket import Ticket
from dateutil.easter import *
from dateutil.rrule import *
from dateutil.parser import *
from dateutil.relativedelta import *
from resources.api_engine import ApiEngine
from multipledispatch import dispatch

class kkm:

#    @dispatch(str, str, dict, int)
    def __init__(self, csv_file, message_file, ops,days_expire,delimeter=';'):
        self.kkm_csv_file = csv_file
        self.delimiter = delimeter
        self.days_expire =  days_expire
        self.the_end = datetime.date.today() + relativedelta(days=+days_expire)
        self.api_engine = ApiEngine()
        self.message_file = message_file
        self.ops = ops


    @dispatch()
    def end_is_near(self):
        outdated_serials = []

        with open(self.kkm_csv_file, 'r', encoding='utf8') as csv_file:
            reader = csv.reader(csv_file, delimiter=self.delimiter)
            for row in reader:
                try:
                    if parse(row[5][:10]).date() == self.the_end:
                        outdated_serials.append(row)
                except ValueError:
                    try:
                        if parse(row[5][:9]).date() == self.the_end:
                            outdated_serials.append(row)
                            print(row)
                    except ValueError:
                        pass
        return outdated_serials

    def request_kkm_change(self, serial, fn, end_date, address, index, type):
        mpkt_service = "service$63044706"
        mpkt_service_component = "service$271691940"
        mpkt_route = "catalogs$429322501"

        pkt_service = "service$1622149"
        pkt_service_component = "service$271691939"
        pkt_route = "catalogs$425703227"
        with open(self.message_file,encoding='utf8') as message:
            address = address.replace(',', ' ')

            descriptionInRTF = message.read().format(serial + '\n', fn + '\n', end_date + '\n', address + '\n')

            if "mpkt" in type:

                t = Ticket(mpkt_service, mpkt_service_component, mpkt_route,
                           descriptionInRTF, 'employee$15706889', 'employee$15706889',
                           self.ops[index]['uuid'], self.ops[index]['uuid'])
            if "pkt" in type:

                t = Ticket(pkt_service, pkt_service_component, pkt_route,
                       descriptionInRTF, 'employee$15706889', 'employee$15706889',
                       self.ops[index]['uuid'], self.ops[index]['uuid'])

            else:
                print("Type error")
            self.api_engine.create_request(t)
            print(str(t))
