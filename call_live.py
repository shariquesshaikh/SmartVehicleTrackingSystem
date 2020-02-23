from livecaresys import *
from multiprocessing.pool import ThreadPool
import threading, time, sys
import image
import notify

def get(vehicles):
      res=vehicles
      print(res)
      if(len(vehicles)!=0):
            lis = image.fetch()
            for i in range(len(res)):
                  if(type(res)==tuple):
                              #print(res)
                              check(res,lis)
                              image.live_ins(res[i])
                  else:
                        for j in range(len(res[i])):
                              if(type(res)==tuple):
                                    #print(res)
                                    check(res,lis)
                                    image.live_ins(res[i])

def check(res,lis):
      for i in range(len(res)):
           if(res[i][0] == lis[i][0]):
                notify.get_response(res[i][0],res[i][1],res[i][4])
                image.notifi(res)
 
    
#threading.Thread(target = livecaresysfunc, args=("http://192.168.43.1:7500/stream.mjpeg",1,'call_live','get','us')).start()
threading.Thread(target = livecaresysfunc, args=("http://192.168.137.19:8080/stream.mjpeg",1,'call_live','get','in')).start()



