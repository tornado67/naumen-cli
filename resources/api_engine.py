# encoding=utf8
import json
import base64
import urllib.parse
import urllib.error
import urllib.request
from resources.ticket import Ticket
from multipledispatch  import dispatch

#Route - вид запроса
#service -  услуга
#outes - подпункты service
#location -  ОПС

class ApiEngine:

    __api_access_key_string = "accessKey=your_key_here"
    __api_host = "https://<your_address_here>"
    __api_application_address = "/sd/services/rest/exec"

    def list_service(self):
        api_function_str_list_service = "func=modules.sdRest.listService&params=user"
        url="{}{}?{}&{}".format(self.__api_host, self.__api_application_address, self.__api_access_key_string, api_function_str_list_service)
        try:
            with urllib.request.urlopen(url) as _url:

                if _url.getcode() < 200 and url.getcode() > 299:
                    print("HTTP Error code" + _url.getcode())
                    return None
                _json = _url.read().decode("utf-8")

                return json.loads(_json)

        except urllib.error.URLError as url_error:
            print ("URL Error occured")
            print(url_error.args)
            print(url_error.reason)
            print(url_error.errno)
            return None

    def list_service_calls(self):
        api_function_str_list_service_calls = "func=modules.sdRest.listServiceCalls&params=user"
        url = "{}{}?{}&{}".format(self.__api_host,
                                  self.__api_application_address,
                                  self.__api_access_key_string,
                                  api_function_str_list_service_calls)
        try:
            with urllib.request.urlopen(url) as _url:
                if _url.getcode() < 200 and url.getcode() > 299:
                    print("HTTP Error code" + _url.getcode())
                    return None

                _json = _url.read().decode("utf-8")

                return json.loads(_json)

        except urllib.error.URLError as url_error:
            print("URL Error occured")
            print(url_error.args)
            print(url_error.reason)
            print(url_error.errno)
            return None

    def list_ci(self):
        body = {
            "locationUuid": "location$16178616",
            "supServiceUuid":"service$54081202",

                        "firstResult": "0",
                          "maxResult" : "1000"
        }
        body = json.dumps(body).encode('utf8')
        api_application_address = "/sd/services/rest/exec-post"
        api_function = "func=modules.sdRest.getCiList&params=user,requestContent"
        url = "{}{}?{}&{}".format(self.__api_host,
                                  api_application_address,
                                  self.__api_access_key_string,
                                  api_function
                                  )

        req = urllib.request.Request(url)
        req.add_header('Content-Type', 'application/json')
        try:
            with urllib.request.urlopen(req, data=body) as _url:
                if _url.getcode() < 200 and url.getcode() > 299:
                    print("HTTP Error code" + _url.getcode())
                    return None

                _json = _url.read().decode("utf-8")

            return _json

        except urllib.error.URLError as url_error:
            print("URL Error occured")
            print(url_error.args)
            print(url_error.reason)
            print(url_error.errno)
            return None



    def mark_service_call(self, uuid):

        api_func_str_mark_service_call = "func=modules.sdRest.markServiceCall&params={},user"

        url = "{}{}?{}&{}".format(self.__api_host,
                                 self.__api_application_address,
                                 self.__api_access_key_string,
                                 api_func_str_mark_service_call.format(uuid))

        try:
            with urllib.request.urlopen(url) as _url:
                if _url.getcode() < 200 and url.getcode() > 299:
                    print("HTTP Error code" + _url.getcode())
                    return None

        except urllib.error.URLError as url_error:
            print("URL Error occured")
            print(url_error.args)
            print(url_error.reason)
            print(url_error.errno)
            return None

    def add_file_to_object(self,file_path,object_id):
        with open(file_path, "rb") as file:
            content = base64.b64encode(file.read())
            content = content.decode()

            body = {
                'attrCode': "ContentFiles",
                'sourceUUID': object_id,
                'mimeType': "text/plain",
                'title': file_path,
                'content': content
            }
            body = json.dumps(body).encode('utf8')
            api_application_address = "/sd/services/rest/exec-post"
            api_function = "func=modules.sdRest.addFileToObject&params=requestContent,user"
            url = "{}{}?{}&{}".format(self.__api_host,
                                      api_application_address,
                                      self.__api_access_key_string,
                                      api_function
                                      )

            req = urllib.request.Request(url)
            req.add_header('Content-Type', 'application/json')
            try:
                with urllib.request.urlopen(req, data=body) as _url:
                    if _url.getcode() < 200 and url.getcode() > 299:
                        print("HTTP Error code" + _url.getcode())
                        return None

                    _json = _url.read().decode("utf-8")

                return _json

            except urllib.error.URLError as url_error:
                print("URL Error occured")
                print(url_error.args)
                print(url_error.reason)
                print(url_error.errno)
                return None

    def create_object(self, _json_body):
        api_application_address = "/sd/services/rest/create-m2m/serviceCall$request/"
        url = "{}{}?{}".format(self.__api_host,
                               api_application_address,
                               self.__api_access_key_string
                               )
        data = urllib.request.quote(_json_body).encode()
        try:
            req = urllib.request.Request(url,data=data)
        #req.add_header('Content-Type','application/json')
            print (req.full_url)
            response = urllib.request.urlopen(req)
            print (response)
            return  response.getcode()
        except urllib.error.HTTPError as url_error:
            print("URL Error occured")
            print(url_error.args)
            print(url_error.reason)
            print(url_error.headers)
            print(url_error.info())
            print(url_error.code)
            print(url_error.msg)
            print(url_error.name)
            return None

    @dispatch(str,str,str,str,str,str,str,str)
    def create_request(self,service,service_comp,route,descr,user,client,location,place):
        #'{"slmService":"service$38741002","route":"catalogs$38741604","descriptionInRTF":"nested tested test","userName":"employee$405802127","client":"employee$405802127","location":"location$16178616","place":"location$16178616"}'
        application_address = "/sd/services/rest/create-m2m/serviceCall$request/"
        params ="{{'slmService':'{}','seviceComp':'{}', 'route':'{}','descriptionInRTF':'{}','userName':'{}','client':'{}','location':'{}','place':'{}'}}"

        url = "{}{}{}?{}".format(self.__api_host,
                                 application_address,
                                 params.format(service,service_comp,route, urllib.parse.quote(descr.encode('utf-8')) ,user,client,location,place),
                                 self.__api_access_key_string)
        try:

            with urllib.request.urlopen(url) as _url:
                if _url.getcode() < 200 and url.getcode() > 299:
                    print("HTTP Error code" + _url.getcode())
                    return None

                _json = _url.read().decode("utf-8")

            return json.loads(_json)

        except urllib.error.URLError as url_error:
            print("URL Error occured")
            print(url_error.args)
            print(url_error.reason)
            print(url_error.errno)
            return None

    @dispatch(Ticket)
    def create_request(self,  ticket):
            application_address = "/sd/services/rest/create-m2m/serviceCall$request/"
            url = "{}{}{}?{}".format(self.__api_host,
                                     application_address,
                                     str(ticket),
                                     self.__api_access_key_string)
            try:
                print(url)
                with urllib.request.urlopen(url) as _url:
                    if _url.getcode() < 200 and url.getcode() > 299:
                        print("HTTP Error code" + _url.getcode())
                        return None

                    _json = _url.read().decode("utf-8")

                return json.loads(_json)

            except urllib.error.URLError as url_error:
                print("URL Error occured")
                print(url_error.args)
                print(url_error.reason)
                print(url_error.errno)
                return None

    @dispatch(Ticket,str)
    def create_request(self, ticket):
        application_address = "/sd/services/rest/create-m2m/serviceCall$request/"
        url = "{}{}{}?{}".format(self.__api_host,
                                 application_address,
                                 str(ticket),
                                 self.__api_access_key_string)
        try:
            print(url)
            with urllib.request.urlopen(url) as _url:
                if _url.getcode() < 200 and url.getcode() > 299:
                    print("HTTP Error code" + _url.getcode())
                    return None

                _json = _url.read().decode("utf-8")

            return json.loads(_json)

        except urllib.error.URLError as url_error:
            print("URL Error occured")
            print(url_error.args)
            print(url_error.reason)
            print(url_error.errno)
            return None

    def list_locations(self):
        api_function_str_list_locations = "func=modules.sdRest.listLocations&params"
        url = "{}{}?{}&{}".format(self.__api_host,
                                  self.__api_application_address,
                                  self.__api_access_key_string,
                                  api_function_str_list_locations)
        try:
            with urllib.request.urlopen(url) as _url:
                if _url.getcode() < 200 and url.getcode() > 299:
                    print("HTTP Error code" + _url.getcode())
                    return None

                _json = _url.read().decode("utf-8")

                return json.loads(_json)
        except urllib.error.URLError as url_error:
            print("URL Error occured")
            print(url_error.args)
            print(url_error.reason)
            print(url_error.errno)
            return None

    def list_code_closing(self):
        api_function_str_list_code_closing = "&func=modules.sdRest.listCodeClosing&params=user"
        url = "{}{}?{}&{}".format(self.__api_host,
                                  self.__api_application_address,
                                  self.__api_access_key_string,
                                  api_function_str_list_code_closing)
        try:
            with urllib.request.urlopen(url) as _url:
                if _url.getcode() < 200 and url.getcode() > 299:
                    print("HTTP Error code" + _url.getcode())
                    return None

                _json = _url.read().decode("utf-8")

                return json.loads(_json)
        except urllib.error.URLError as url_error:
            print("URL Error occured")
            print(url_error.args)
            print(url_error.reason)
            print(url_error.errno)
            print(url_error.strerror)
            return None

    def list_all_routes(self):
        api_function_str_list_all_routes = "func=modules.sdRest.listAllRoutes&params=user"
        url = "{}{}?{}&{}".format(self.__api_host,
                                  self.__api_application_address,
                                  self.__api_access_key_string,
                                  api_function_str_list_all_routes)
        try:
            with urllib.request.urlopen(url) as _url:
                if _url.getcode() < 200 and url.getcode() > 299:
                    print("HTTP Error code" + _url.getcode())
                    return None

                _json = _url.read().decode("utf-8")
                return _json
        except urllib.error.URLError as url_error:
            print("URL Error occured")
            print(url_error.args)
            print(url_error.reason)
            print(url_error.errno)
            return None

    def list_sub_locations(self,location):
        api_func_str_list_sub_locations = "func=modules.sdRest.listSubLocations&params={}"

        url = "{}{}?{}&{}".format(self.__api_host,
                                  self.__api_application_address,
                                  self.__api_access_key_string,
                                  api_func_str_list_sub_locations.format(location))
        try:
            with urllib.request.urlopen(url) as _url:
                if _url.getcode() < 200 and url.getcode() > 299:
                    print("HTTP Error code" + _url.getcode())
                    return None

                _json = _url.read().decode("utf-8")

                return json.loads(_json)
        except urllib.error.URLError as url_error:
            print("URL Error occured")
            print(url_error.args)
            print(url_error.reason)
            print(url_error.errno)
            return None















     #pprint.pprint(obj)
#print (api_engine.list_all_routes())

#uuid =  re.sub('serviceCall\$', '',  api_engine.list_service_calls()[0]['uuid'])
#api_engine.mark_service_call(uuid)
