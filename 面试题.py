#-*-doding:utf-8 -*-

data = [1,3,5,7,8,25,4,20]

def main():

	dataIndex = []
	length = len(data)
	totla = sum(data)

	if (length>2) :
		temSpum = data[0]
		for iin range(1,length-1):
			if (tempSum*2 + data[i] == total):
				dataIndex.append(i)
			temSum = tempSum + data[i]
	returm dataIndex

if __name__ == '__main__':
	print (main())



# -*- coding: utf-8 -*-
 # 用dictionary实现，key存放所给的数，value为list，存放所给数在数组中的位置
 # 一个数可能在数组中出现多次
 data = [3,,31,2,3]

 def main() :
 	dataIndex = []
 	hashData = {}

 	for i in range(0,len(data)) :
 		key = data[i]
 		if (key in hashData) :
 			value = hashData[key]
 			value.append(i)
 		else:
 			value = []
 			value.append(i)
 			hashData[key] = value
 	halfLength = int(len(data) / 2)
 	if (len(data) % 2 == 1):
 		halfLength = halfLength + 1
 	for key in hashData:
 		if (len(hashData[key]) >= halfLength) :
 			dataIndex.append(hashData[key])

 	return dataIndex

if __name__ == '__main__' :
	print(main())

#要求算任意长度字符串中不同的字符以及它的个数

s = "abcdefgabc"
dic = dict.fromkeys(s,0)
for x in s:
	dic[x] += 1
print '\n'.join('%s,%s' % (k,v) for k,v in dic.items())