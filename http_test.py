#coding: utf-8

import httplib, urllib, base64
import json

headers = {
    # Request headers
    'Ocp-Apim-Subscription-Key': '37d3a9eea575471a9eaaefa3fe47b1da',
}

params = urllib.urlencode({
    # Request parameters
    'expr': "Composite(AA.AuN=='jaime teevan')",
    'model': 'latest',
    'count': '10',
    'offset': '0',
    #'orderby': '{string}',
    'attributes': 'Id,AA.AuId,F.FId,J.JId,C.CId,AA.AfId,RId',
})

try:
    conn = httplib.HTTPSConnection('api.projectoxford.ai')
    conn.request("GET", "/academic/v1.0/evaluate?%s" % params, "{body}", headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("[Errno {0}] {1}".format(e.errno, e.strerror))


o = json.loads(data)
#print o.keys()
entities = o["entities"]
for entity in entities:
	print entity
