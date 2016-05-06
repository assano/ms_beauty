# -*- coding: utf-8 -*-

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
    one_hop_path = []
    two_hop_path = []

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
        if 'RId' in entitie.keys():
            Id2Id.r_id_arr = entitie["RId"]
            if id2 in Id2Id.r_id_arr:
                path = [str(id1), str(id2)]
                self.one_hop_path.append(path) 
        
        return self.one_hop_path


    def two_hop(self, id1, id2):
        #1)请求id3的RId, id1----->id3---->id2
            #============请求id1的RId
        # params1 = urllib.urlencode({
        #     'expr': "Id="+str(id1),
        #     'model': 'latest',
        #     'count': '10',
        #     'offset': '0',
        #     'attributes': 'RId',
        # })
        # json_info1 = get_info(params1)
        # json_object1 = json.loads(json_info1)
        # entitie1 = json_object1["entities"][0]


        # keys1 = entitie1.keys()
        # if 'RId' in keys1:
            # r_id_arr1 = entitie1['RId']

        #===========请求r_id_arr1中每一个Id的RId，并且比对有没有id2
            # for tmp_id in r_id_arr1:
        for tmp_id in Id2Id.r_id_arr:
            tmp_params = urllib.urlencode({
                'expr': "Id="+str(tmp_id),
                'model': 'latest',
                'count': '10',
                'offset': '0',
                'attributes': 'RId',
            })
            tmp_json_info = get_info(tmp_params)
            tmp_json_object = json.loads(tmp_json_info)
            tmp_entitie = tmp_json_object["entities"][0]

            tmp_keys = tmp_entitie.keys()
            if 'RId' in tmp_keys:
                tmp_r_id_arr = tmp_entitie['RId']
                #比对
                if id2 in tmp_r_id_arr:
                    self.two_hop_path.append([str(id1), str(tmp_id), str(id2)])

        #2)请求Id1的除RId的其余 4 种信息
        id1_params = urllib.urlencode({
            'expr': "Id="+str(id1),
            'model': 'latest',
            'count': '10',
            'offset': '0',
            'attributes': 'AA.AuId,F.FId,J.JId,C.CId',
        })
        json_info_id1 = get_info(id1_params)
        json_object_id1 = json.loads(json_info_id1)
        entitie_id1 = json_object_id1['entities'][0]


        AA_AuId_dict_id1 = []
        F_FId_dict_id1 = []
        C_CId_dict_id1 = []
        J_JId_dict_id1 = []

        keys_id1 = entitie_id1.keys()
        if 'AA' in keys_id1:
            AA_AuId_dict_id1 = entitie_id1['AA']
        if 'F' in keys_id1:
            F_FId_dict_id1 = entitie_id1['F']
        if 'C' in keys_id1:
            C_CId_dict_id1.append(entitie_id1['C'])
        if 'J' in keys_id1:
            J_JId_dict_id1.append(entitie_id1['J'])

        #3)请求Id2的除RId的其余 4 种信息
        id2_params = urllib.urlencode({
            'expr': "Id="+str(id2),
            'model': 'latest',
            'count': '10',
            'offset': '0',
            'attributes': 'AA.AuId,F.FId,J.JId,C.CId',
        })
        json_info_id2 = get_info(id2_params)
        json_object_id2 = json.loads(json_info_id2)
        entitie_id2 = json_object_id2['entities'][0]

        AA_AuId_dict_id2 = []
        F_FId_dict_id2 = []
        C_CId_dict_id2 = []
        J_JId_dict_id2 = []

        keys_id2 = entitie_id2.keys()
        if 'AA' in keys_id2:
            AA_AuId_dict_id2 = entitie_id2['AA']
        if 'F' in keys_id2:
            F_FId_dict_id2 = entitie_id2['F']
        if 'C' in keys_id2:
            C_CId_dict_id2.append(entitie_id2['C'])
        if 'J' in keys_id2:
            J_JId_dict_id2.append(entitie_id2['J'])

        #4)比对Id1和Id2的 4 种信息
            #==========比对 AA.AuId
        AA_AuId_arr_id1 = []
        for tmp_dict in AA_AuId_dict_id1:
            AA_AuId_arr_id1.append(tmp_dict['AuId'])
        AA_AuId_arr_id2 = []
        for tmp_dict in AA_AuId_dict_id2:
            AA_AuId_arr_id2.append(tmp_dict['AuId'])
        AA_AuId_set_id1 = set(AA_AuId_arr_id1)
        AA_AuId_set_id2 = set(AA_AuId_arr_id2)
            #==========求两个集合的交集
        inters = AA_AuId_set_id1 & AA_AuId_set_id2
            #==========把交集里的结果节点添加到two_hop的路径中，Id1----->集合中的元素----->Id3
        for ele in inters:
            self.two_hop_path.append([str(id1), str(ele), str(id2)])

            #==========比对 F.FId
        F_FId_arr_id1 = []
        for tmp_dict in F_FId_dict_id1:
            F_FId_arr_id1.append(tmp_dict['FId'])
        F_FId_arr_id2 = []
        for tmp_dict in F_FId_dict_id2:
            F_FId_arr_id2.append(tmp_dict['FId'])
        F_FId_set_id1 = set(F_FId_arr_id1)
        F_FId_set_id2 = set(F_FId_arr_id2)
            #==========求两个集合的交集
        inters1 = F_FId_set_id1 & F_FId_set_id2
            #==========把交集里的结果节点添加到two_hop的路径中，Id1----->集合中的元素----->Id3
        for ele in inters1:
            self.two_hop_path.append([str(id1), str(ele), str(id2)])

            #==========比对 J.JId==========J.JId是只有一个元素的数组
        J_JId_arr_id1 = []
        for tmp_dict in J_JId_dict_id1:
            J_JId_arr_id1.append(tmp_dict['JId'])
        J_JId_arr_id2 = []
        for tmp_dict in J_JId_dict_id2:
            J_JId_arr_id2.append(tmp_dict['JId'])
        J_JId_set_id1 = set(J_JId_arr_id1)
        J_JId_set_id2 = set(J_JId_arr_id2)
            #==========求两个集合的交集
        inters2 = J_JId_set_id1 & J_JId_set_id2
            #==========把交集里的结果节点添加到two_hop的路径中，Id1----->集合中的元素----->Id3
        for ele in inters2:
            self.two_hop_path.append([str(id1), str(ele), str(id2)])

            #==========比对 C.CId==========C.CId是只有一个元素的数组
        C_CId_arr_id1 = []
        for tmp_dict in C_CId_dict_id1:
            C_CId_arr_id1.append(tmp_dict['CId'])
        C_CId_arr_id2 = []
        for tmp_dict in C_CId_dict_id1:
            C_CId_arr_id2.append(tmp_dict['CId'])
        C_CId_set_id1 = set(C_CId_arr_id1)
        C_CId_set_id2 = set(C_CId_arr_id2)
            #==========求两个集合的交集
        inters3 = C_CId_set_id1 & C_CId_set_id2
            #==========把交集里的结果节点添加到two_hop的路径中，Id1----->集合中的元素----->Id3
        for ele in inters3:
            self.two_hop_path.append([str(id1), str(ele), str(id2)])

        return self.two_hop_path


#--------------------test------------------
id1 = 2157025439
id2 = 2102958620

# id1 = 2061901927
# id2 = 2134746982

path = Id2Id().one_hop(id1, id2)
print 'one_hop_path:',path
path2 = Id2Id().two_hop(id1, id2)
print 'two_hop_path:',path2
