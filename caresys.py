import threading, time, sys
import cv2 
import os
from os import path
import requests
import base64
import json
from multiprocessing.pool import ThreadPool

#country = 'us'
# us: USA
# in: India

Res = []

#--------------------------------recogimg------------------------------------------
def recogimg(name, country):
    IRes = []
    IMAGE_PATH = name
    #print('Reading: ' + name)
    SECRET_KEY = 'sk_DEMODEMODEMODEMODEMODEMO'

    with open(IMAGE_PATH, 'rb') as image_file:
        img_base64 = base64.b64encode(image_file.read())

    
    print("Sending: " + name)
    url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country='+country+'&secret_key=%s' % (SECRET_KEY)
    r = requests.post(url, data = img_base64)
    
    mydict = json.dumps(r.json(), indent=2)
    
    d = json.loads(mydict)
    vehicles = []
    try:
        for i in range(0,len(d["results"])):
            '''
            print("Details for: " + name)
            print("Car#" + str(i+1))
            print("Plate No: " + d["results"][i]["plate"])
            print("Color: " + d["results"][i]["vehicle"]["color"][0]["name"])
            print("Make: " + d["results"][i]["vehicle"]["make"][0]["name"])
            print("Body Type: " + d["results"][i]["vehicle"]["body_type"][0]["name"])
            print("Year: " + d["results"][i]["vehicle"]["year"][0]["name"])
            print("Model: " + d["results"][i]["vehicle"]["make_model"][0]["name"])
            print("\n")
            '''
            
            vehicles.append((d["results"][i]["plate"],
                             d["results"][i]["vehicle"]["color"][0]["name"],
                             d["results"][i]["vehicle"]["make"][0]["name"],
                             d["results"][i]["vehicle"]["body_type"][0]["name"],
                             d["results"][i]["vehicle"]["year"][0]["name"],
                             d["results"][i]["vehicle"]["make_model"][0]["name"]))
            
    except KeyError:
        pass                         
    #print(vehicles)
    
    IRes.append(vehicles)
    return(IRes)



#--------------------------------OpenALPR.py------------------------------------------

def recog(name, country):
    
    IMAGE_PATH = name
    #print('Reading: ' + name)
    SECRET_KEY = 'sk_DEMODEMODEMODEMODEMODEMO'

    with open(IMAGE_PATH, 'rb') as image_file:
        img_base64 = base64.b64encode(image_file.read())

    
    print("Sending: " + name)
    url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country='+country+'&secret_key=%s' % (SECRET_KEY)
    r = requests.post(url, data = img_base64)
    try:
        mydict = json.dumps(r.json(), indent=2)
    except JSONDecodeError:
        print('Error')
    
    d = json.loads(mydict)
    vehicles = []
    try:
        for i in range(0,len(d["results"])):
            '''
            print("Details for: " + name)
            print("Car#" + str(i+1))
            print("Plate No: " + d["results"][i]["plate"])
            print("Color: " + d["results"][i]["vehicle"]["color"][0]["name"])
            print("Make: " + d["results"][i]["vehicle"]["make"][0]["name"])
            print("Body Type: " + d["results"][i]["vehicle"]["body_type"][0]["name"])
            print("Year: " + d["results"][i]["vehicle"]["year"][0]["name"])
            print("Model: " + d["results"][i]["vehicle"]["make_model"][0]["name"])
            print("\n")
            '''
            
            vehicles.append((d["results"][i]["plate"],
                             d["results"][i]["vehicle"]["color"][0]["name"],
                             d["results"][i]["vehicle"]["make"][0]["name"],
                             d["results"][i]["vehicle"]["body_type"][0]["name"],
                             d["results"][i]["vehicle"]["year"][0]["name"],
                             d["results"][i]["vehicle"]["make_model"][0]["name"]))
            
    except KeyError:
        pass                         
    #print(vehicles)
    global Res
    Res.append(vehicles)
    return(Res)
    
    

#--------------------------------VidCam.py------------------------------------------

    
def startVidCam(fileName, frame_rate, country):
    x = []
    threads = []
    try: 
      
        
        if not os.path.exists('data'): 
            os.makedirs('data') 
      
    
    except OSError: 
        print ('Error: Creating directory of data')

    cam = cv2.VideoCapture(fileName) 
    currentframe = 0
    j = 0
    frame_no = 0
    while(True):
        x.append(0)
        ret,frame = cam.read()
        if ret: 
            name = './data/frame' + str(currentframe) + '.jpg'
            #print ('Creating...' + name)
            cv2.imwrite(name, frame)

            x[j] = threading.Thread(target = recog, args=(name,country,))
            x[j].start()
            threads.append(x[j])
    
            currentframe += 1
            j += 1
        else: 
            break
        frame_no += frame_rate
        cam.set(1,frame_no)
        
    cam.release() 
    cv2.destroyAllWindows()
    for t in threads:
        t.join()
    #print('\nVidCamDone\n')
    global Res
    FVidCamRes = Res
    Res = []
    return(FVidCamRes)

#--------------------------------main.py-----------------------------------------


def caresysfunc(option,arg1,arg2, country):
    
    if option == 0:
        fileName = arg1
        r = recogimg(fileName, country)
        return(r)

    elif option == 1:
        fileName = arg1
        frame_rate = arg2                            
        r = startVidCam(fileName,frame_rate, country)
        return(r)

    else:
        print("Enter correct arguments!")

##s = caresysfunc(0, "frame0.jpg", 240)
##print(s)



