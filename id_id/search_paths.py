#coding: utf-8

import httplib, urllib, base64
import json


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


class Id2Id(object):

    r_id_arr = []

    def __init__(self):
        pass

    def one_hop(self, id1, id2):
        #请求id1的RId
        res = []
        params = urllib.urlencode({
            # Request parameters
            'expr': "Id="+str(id1),
            'model': 'latest',
            'count': '10',
            'offset': '0',
            #'orderby': '{string}',
            'attributes': 'RId',
        })
        #请求RId
        json_info = get_info(params)
        json_object = json.loads(json_info)
        entitie = json_object["entities"][0]
        r_id_arr = entitie["RId"]

        if id2 in r_id_arr:
            path = [id1, id2]
            res.append(path) 
        return res

    def two_hop(self, id1, id2):
        #
        pass



id1 = 2157025439
id2 = 2102958620
path = Id2Id().one_hop(id1, id2)
print 'path:',path
