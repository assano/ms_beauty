# encoding=utf-8

import requests
import json
import sys
import copy

headers = {'Ocp-Apim-Subscription-Key':'eb3f9d9e561d4463b30fbddba069463a'}
head = {}
nxt = []
to = []
tot = 0
edge = set()
vis = set()
allpath = []
# all number will be int/long/int64

def AddTwo(a, b):
	AddOne(a, b)
	AddOne(b, a)

def AddOne(a, b):
	global to
	global head
	global nxt
	global tot
	global edge

	if (a,b) in edge:
		return
	edge.add((a,b))

	to.append(b)
	if head.has_key(a):
		nxt.append(head[a])
	else:
		nxt.append(-1)
	head[a]=tot
	tot = tot + 1

def IsId(a):
	url = 'https://api.projectoxford.ai/academic/v1.0/evaluate?expr=Id=%d&model=latest&count=1&offset=0&attributes=Id,AA.AuId,AA.AfId,J.JId,C.CId,F.FId,RId' % a
	res = requests.get(url,headers=headers)
	data = json.loads(res.text)
	if len(data['entities'])>0:
		return data['entities'][0]['Id'] == a and data['entities'][0].has_key('AA')
	return False

def GetId(a):
	while True:
		url = 'https://api.projectoxford.ai/academic/v1.0/evaluate?expr=Id=%d&model=latest&count=1&offset=0&attributes=Id,AA.AuId,AA.AfId,J.JId,C.CId,F.FId,RId' % a
		res = requests.get(url,headers=headers)
		data = json.loads(res.text)
		if data.has_key('entities'):
			return data['entities'][0]

def GetAuthor(a, InRId = False):
	if InRId:
		url = 'https://api.projectoxford.ai/academic/v1.0/evaluate?expr=Composite(AA.AuId=%d)&model=latest&count=10000&offset=0&attributes=Id,AA.AuId,AA.AfId,RId' % a
	else:
		url = 'https://api.projectoxford.ai/academic/v1.0/evaluate?expr=Composite(AA.AuId=%d)&model=latest&count=10000&offset=0&attributes=Id,AA.AuId,AA.AfId' % a
	res = requests.get(url,headers=headers)
	data = json.loads(res.text)
	return data['entities']


def AddEdgeId(a, data, AddRId = True):
	if data.has_key('AA'):
		for i in data['AA']:
			AddTwo(a, i['AuId'])
			if i.has_key('AfId'):
				AddTwo(i['AuId'],i['AfId'])
	if data.has_key('F'):
		for i in data['F']:
			AddTwo(a, i['FId'])
	if data.has_key('C'):
		AddTwo(a, data['C']['CId'])
	if data.has_key('J'):
		AddTwo(a, data['J']['JId'])
	if AddRId:
		RId = data['RId']
		for i in RId:
			AddOne(a, i)

def AddEdgeAuthor(a, data, AddRId = False):
	addafid = False
	for i in data:
		AddTwo(a,i['Id'])
		if AddRId:
			for j in i['RId']:
				AddOne(i['Id'],j)
		if addafid:
			continue
		for j in i['AA']:
			if j['AuId'] == a:
				AddTwo(a,j['AfId'])
				addafid = True

def GetRId(a):
	url = 'https://api.projectoxford.ai/academic/v1.0/evaluate?expr=RId=%d&model=latest&count=10000&offset=0&attributes=Id'%a
	res = requests.get(url,headers=headers)
	data = json.loads(res.text)
	return data['entities']

nowpath = []
def DFS(a, b, cnt):
	global allpath
	global head
	global to
	global nxt
	global nowpath
	global vis


	if a == b:
		allpath.append(copy.deepcopy(nowpath))
	if cnt == 3:
		return
	else:
		if head.has_key(a):
			v = head[a]
			while v >= 0:
				if to[v] not in vis:
					vis.add(to[v])
					nowpath.append(to[v])
					DFS(to[v],b,cnt+1)
					nowpath.pop()
					vis.remove(to[v])
				v = nxt[v]

def FindPath(a, b):
	global nowpath
	global vis

	vis.add(a)
	nowpath.append(a)
	DFS(a, b, 0)
	nowpath.pop()
	vis.remove(a)

def CalcId2Id(a,b):
	data = GetId(a)
	AddEdgeId(a, data)
	RId = data['RId']
	for i in RId:
		d = GetId(i)
		AddEdgeId(i, d)

	data = GetId(b)
	AddEdgeId(b, data, False)
	data = GetRId(b)
	for i in data:
		AddOne(i['Id'],b)
	FindPath(a, b)

def CalcId2AuId(a, b):
	data = GetId(a)
	AddEdgeId(a, data)
	RId = data['RId']
	for i in RId:
		d = GetId(i)
		AddEdgeId(i, d)
	data = GetAuthor(b)
	AddEdgeAuthor(b, data)
	FindPath(a,b)

def ReverseAllPath():
	global allpath
	for i in allpath:
		i.reverse()

def CalcAuId2AuId(a, b):
	data = GetAuthor(a, True)  # °üº¬RId
	AddEdgeAuthor(a,data, True)
	data = GetAuthor(b)
	AddEdgeAuthor(b,data)
	FindPath(a, b)
	

def CalcAllPath(a, b):
	global allpath
	IsIda = IsId(a)
	IsIdb = IsId(b)
	print IsIda
	print IsIdb
	if IsIda and IsIdb:
		CalcId2Id(a,b)
	elif IsIda and not IsIdb:
		CalcId2AuId(a,b)
	elif not IsIda and IsIdb:
		CalcId2AuId(b,a)
		ReverseAllPath()
	else:
		CalcAuId2AuId(a,b)
	f = open('out.out','w')
	for i in allpath:
		for j in i:
			f.write(str(j)+' ')
		f.write('\n')
	f.close()

if __name__ == '__main__':
	CalcAllPath(int(sys.argv[1]),int(sys.argv[2]))