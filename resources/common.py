import re
from resources.api_engine import ApiEngine


api_engine = ApiEngine()

# функция подгружает (и долго!) все возможные расположения
# сохраняет их в словарь с индекосм ОПС в качестве ключа
def load_locations():
    _ops = {}
    locations = api_engine.list_locations()
    for location in locations:

        for obj2 in api_engine.list_sub_locations(re.sub('location\$', '', location['uuid'])):
            _ops[obj2['postcode']] = obj2
    return _ops
