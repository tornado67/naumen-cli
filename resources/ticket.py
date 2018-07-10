from multipledispatch  import dispatch
import urllib
"{{'slmService':'{}','seviceComp':'{}', 'route':'{}','descriptionInRTF':'{}','userName':'{}','client':'{}','location':'{}','place':'{}'}}"
class Ticket:
    @dispatch(str,str,str,str,str,str,str,str)
    def __init__(self,service,service_comp,route,descr,user,client,location,place):
            self.url = "{{'slmService':'{}','seviceComp':'{}', 'route':'{}','descriptionInRTF':'{}','userName':'{}','client':'{}','location':'{}','place':'{}'}}".format(service,service_comp,route, urllib.parse.quote(descr.encode('utf-8')) ,user,client,location,place)

    @dispatch(str,str,str,str,str,str,str,str,str)
    def __init__(self,service,service_comp,route,descr,user,client,location,place,priority):
            self.url = "{{'slmService':'{}','seviceComp':'{}', 'route':'{}','descriptionInRTF':'{}','userName':'{}','client':'{}','location':'{}','place':'{}','priority':'{}'}}".format(
                service,service_comp,route, urllib.parse.quote(descr.encode('utf-8')) ,user,client,location,place,priority)

    @dispatch(str,str,str,str,str,str,str,str,str)
    def __init__(self, service, service_comp, route, descr, user, client, location, place,log_file_content):
        self.url = "{{'slmService':'{}','seviceComp':'{}', 'route':'{}','descriptionInRTF':'{}','userName':'{}','client':'{}','location':'{}','place':'{}','ContentFiles':'{}'}}".format(
            service, service_comp, route, urllib.parse.quote(descr.encode('utf-8')), user, client, location, place)

    def __repr__(self):
        return  self.url

    def __str__(self):
        return self.url


