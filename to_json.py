# 파이썬의 set은 list를 저장할 수 없다.
# 굳이 set이 아니어도, dictionary 형태 역시 중복을 허용하지 않는다.
# list의 update를 이용하여, url이 중복되지 않는 그날의 뉴스 세트를 저장하도록 한다.


import json
import datetime


def artdic_to_json(dic, sid=100, date=str(datetime.date.today())) :
    jsonload = '{' + '"sid" : "' + str(sid) + '", "date" : "' + date + '", "links": ['
    count = 0
    for a, b in dic.items():
        count = count + 1
        c = str(b).replace("\\", "\\\\").replace('\"', '\\\"')
        d = str(a).replace("\\", "\\\\'").replace('\"', '\\\"')
        jsonload += '{"id" : "' + str(count) + '", "title": "' + c + '" , "url" : "' + d + '"'
        if (count < (len(dic))):
            jsonload += '}, '
        else:
            jsonload += '}'

    jsonload += ']}'
    return jsonload


def json_to_revdic(src) :
    test = json.loads(src)
    _res = {}
    for _art in test['links']:
        _res.update({_art['url']: _art['title']})
    return _res

