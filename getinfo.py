# -*- coding: utf-8 -*-

import httplib, urllib, base64

#发送请求，获得需要的信息
def get_info(params):
    headers = {'Ocp-Apim-Subscription-Key': '37d3a9eea575471a9eaaefa3fe47b1da'}
    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("GET", "/academic/v1.0/evaluate?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    return data