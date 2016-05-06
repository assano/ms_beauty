# -*- coding: utf-8 -*-

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


class AuId2AuId(object):
    """docstring for AuId2AuId"""

    two_hop_path = []
    three_hop_path = []

    def __init__(self):
        pass

    def two_hop(self, AuId1, AuId2):
		# 1)请求AuId1 的Id 和 AA.AfId
        params1 = urllib.urlencode({
            # Request parameters
            'expr': 'Composite(AA.AuId='+str(AuId1)+')',
            'model': 'latest',
            'count': '10',
            'offset': '0',
            'attributes': 'Id,AA.AfId',
        })
        json_info1 = get_info(params1)
        json_object1 = json.loads(json_info1)
        entities1 = json_object1["entities"]
        #保存本作者的所有文章Id和所有AA.AfId
        id_arr1 = []
        AfId_arr1 = []

        for tmp_dict in entities1:
        	#Id
            if 'Id' in tmp_dict:
                id_arr1.append(tmp_dict['Id'])
            #AfId
            if 'AA' in tmp_dict:
            	tmp_AfIds = tmp_dict['AA']
            	for t_d in tmp_AfIds:
            		if 'AfId' in t_d:
            			AfId_arr1.append(t_d['AfId'])

		# 2)请求AuId2 的Id 和 AA.AfId
        params2 = urllib.urlencode({
            # Request parameters
            'expr': 'Composite(AA.AuId='+str(AuId2)+')',
            'model': 'latest',
            'count': '10',
            'offset': '0',
            'attributes': 'Id,AA.AfId',
        })
        json_info2 = get_info(params2)
        json_object2 = json.loads(json_info2)
        entities2 = json_object2["entities"]
        #保存本作者的所有文章Id和所有AA.AfId
        id_arr2 = []
        AfId_arr2 = []

        for tmp_dict in entities2:
        	#Id
            if 'Id' in tmp_dict:
                id_arr2.append(tmp_dict['Id'])
            #AfId
            if 'AA' in tmp_dict:
            	tmp_AfIds = tmp_dict['AA']
            	for t_d in tmp_AfIds:
            		if 'AfId' in t_d:
            			AfId_arr2.append(t_d['AfId'])

        id_set1 = set(id_arr1)
        id_set2 = set(id_arr2)
        AfId_set1 = set(AfId_arr1)
        AfId_set2 = set(AfId_arr2)

        #分别求两个集合的交集
        inters1 = id_set1 & id_set2
        inters2 = AfId_set1 & AfId_set2

        #加入路径
        for ele in inters1:
        	AuId2AuId.two_hop_path.append([str(AuId1), str(ele), str(AuId2)])

        for ele in inters2:
        	AuId2AuId.two_hop_path.append([str(AuId1), str(ele), str(AuId2)])

        return AuId2AuId.two_hop_path


#test
AuId1 = 2123314761
AuId2 = 2105571773

path = AuId2AuId().two_hop(AuId1, AuId2)

print 'two_hop_path:',path