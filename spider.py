import urllib2
import re
import threading
import time
'''
http://www.cnproxy.com/proxy1.html
<tr><td>46.231.14.177<SCRIPT type=text/javascript>document.write(":"+x+f+x+f)</SCRIPT></td><td>HTTP</td><td>313,813,829</td><td>Britain</td></tr>
'''
portdicts={'z':"3",'m':"4",'a':"2",'l':"9",'f':"0",'b':"5",'i':"7",'w':"6",'x':"8",'c':"1",'r':'','d':'','k':''} #定义一个字典，用于生成对应端口号
proxylist1=[] #保存匹配到的代理服务器信息


'''
获取代理服务器信息
'''
def get_proxy_from_cnproxy():
           global proxylist1
           p=re.compile(r'''<tr><td>(.+?)<SCRIPT type=text/javascript>document.write\(":"\+(.+?)\)</SCRIPT></td><td>(.+?)</td><td>(.+?)</td><td>(.+?)</td></tr>''')
           for i in range(1,2):
                      target=r"http://www.cnproxy.com/proxy%d.html" % i
                      #print target
                      req=urllib2.urlopen(target)
                      result=req.read()
                      matchs=p.findall(result)
                      #print  matchs
                      for row in matchs:
                                 ip=row[0]
                                 port=row[1]
                                 port=map(lambda x:portdicts[x],port.split('+'))#处理端口号(会生成['8','0','8','0'])
                                 port=''.join(port) #PS:str.join(list),使用str作为分隔符，把list里的元素连接成一个字符串。如：’*’.join(['a','b','c'])得到’a*b*c’
                                 agent=row[2]
                                 addr=row[3].decode('cp936').encode('utf-8')
                                 l=[ip,port,agent,addr]
                                 #print l
                                 proxylist1.append(l)

'''
           1.检测代理服务器的有效性
           2.检测代理服务器的处理时间并排序
           3.将检测结果写到一个文件中
'''
class ProxyCheck(threading.Thread):
           def __init__(self,proxylist,fname):
                      threading.Thread.__init__(self) #线程初始化【必须】
                      self.proxylist=proxylist
                      self.timeout=0.5
                      self.test_url="http://www.baidu.com" #使用百度网站作为抓取的代理服务器的测试网站
                      self.test_str="030173" #匹配关键字
                      self.checkProxyList=[]  #已经通过检测的代理服务器列表
                      self.fname=fname
           def checkProxy(self):
                      cookies=urllib2.HTTPCookieProcessor()  #构造cookies对象【百度网站需要cookie方式进行登录】
                      for proxy in self.proxylist:
                                 proxy_handler=urllib2.ProxyHandler({"http":r'http://%s:%s' %(proxy[0],proxy[1])}) #构造请求代理操作句柄【ip地址+端口号】
                                 opener=urllib2.build_opener(cookies,proxy_handler) #构造opener对象
                                 '''
                                 百度网站需要验证用户浏览器信息，这里需要模拟User-agent信息【模拟chrome】
                                 '''
                                 opener.addheaders=[('User-agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1')]
                                 urllib2.install_opener(opener)  #加载opener到请求库urllib2中
                                 t1=time.time()                       #获得当前时间戳信息
                                 try:
                                            req = urllib2.urlopen(self.test_url,timeout=self.timeout)
                                            result=req.read()
                                            timeused=time.time()-t1     #计算通过代理网站访问百度的消耗时间值
                                            pos=result.find(self.test_str)#验证能否匹配到定义的关键字，来判断请求是否成功
                                            if pos > 1:
                                                       self.checkProxyList.append([proxy[0],proxy[1],proxy[2],proxy[3],timeused]) #proxy是self.proxylist的元素
                                            else:
                                                       continue

                                 except Exception as e:
                                            #print error_log.write('An error occeurred : %s \n' % e)
                                            continue
                                 #print self.checkProxyList
           def sort(self):
                      #sorted(self.checkProxyList,cmp=lambda x,y:(x[4],y[4]))
                      sorted(self.checkProxyList,key=lambda x:(x[4])) #根据消耗时间进行排序
           def save(self):
                      f=open(self.fname,'a+')
                      for proxy in self.checkProxyList:
                                 f.write("%s:%s\t%s\t%s\t%s\n" %(proxy[0],proxy[1],proxy[2],proxy[3],str(proxy[4])))
                      f.close()
           def run(self):
                      self.checkProxy()
                      print "*"*50
                      self.sort()
                      print "*"*50
                      self.save()
if __name__=="__main__":
           get_proxy_from_cnproxy()
           t1=ProxyCheck(proxylist1,"t1.txt")
           t1.start()
