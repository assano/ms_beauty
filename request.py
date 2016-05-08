# -*- coding: utf-8 -*-

import httplib, urllib, base64
import urllib2
import json

url = "http://yangbing.chinacloudapp.cn:9200?id1=2157025439&id2=2134746982"
req = urllib2.Request(url)
res_data = urllib2.urlopen(req)
res = res_data.read()
# print type(res)
print 'request:',req
print 'response:',res