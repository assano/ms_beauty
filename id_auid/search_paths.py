# -*-coding: utf-8 -*-

import json
import httplib, urllib, base64

#发送请求，获得需要的信息
def get_info(params):
    headers = {'Ocp-Apim-Subscription-Key': '37d3a9eea575471a9eaaefa3fe47b1da'}
    data = None
    try:
        conn = httplib.HTTPSConnection('api.projectoxford.ai')
        conn.request("GET", "/academic/v1.0/evaluate?%s" % params, "{body}", headers)
        response = conn.getresponse()
        data = response.read()
        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
    return data

class Id2AuId(object):

    one_hop_path = []
    two_hop_path = []
    three_hop_path = []

    def __init__(self):
        pass

    def one_hop(self, Id, AuId):
    	# 1)请求Id的AuId
        params = urllib.urlencode({
            # Request parameters
            'expr': 'Id='+str(Id),
            'model': 'latest',
            'count': '10',
            'offset': '0',
            'attributes': 'AA.AuId',
        })
        json_info = get_info(params)
        json_object = json.loads(json_info)
        entities = json_object["entities"]

        AuId_arr = []
        for entity in entities:
        	if 'AA' in entity:
        		AuId_dicts = entity['AA']
        		for tmp_dict in AuId_dicts:
        			if 'AuId' in tmp_dict:
        				AuId_arr.append(tmp_dict['AuId'])

        if AuId in AuId_arr:
        	Id2AuId.one_hop_path.append([str(Id), str(AuId)])
        return Id2AuId.one_hop_path
    def two_hop(self, Id, AuId):
    	




#test
Id = 2161304134
AuId = 2123314761
path = Id2AuId().one_hop(Id, AuId)
print 'one_hop_path:',path
