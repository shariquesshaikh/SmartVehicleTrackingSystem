import threading, time, sys
import cv2 
import os
from os import path
import requests
import base64
import json


#--------------------------------OpenALPR.py------------------------------------------

def recog(name):
    
    IMAGE_PATH = name
    #print('Reading: ' + name)
    SECRET_KEY = 'sk_DEMODEMODEMODEMODEMODEMO'

    with open(IMAGE_PATH, 'rb') as image_file:
        img_base64 = base64.b64encode(image_file.read())

    
    print("Sending to API: " + name)
    url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=us&secret_key=%s' % (SECRET_KEY)
    r = requests.post(url, data = img_base64)
    
    mydict = json.dumps(r.json(), indent=2)
    
    d = json.loads(mydict)
    vehicles = []
    for i in range(0,len(d["results"])):
        print("Details for: " + name)
        print("Car#" + str(i+1))
        print("Plate No: " + d["results"][i]["plate"])
        print("Color: " + d["results"][i]["vehicle"]["color"][0]["name"])
        print("Make: " + d["results"][i]["vehicle"]["make"][0]["name"])
        print("Body Type: " + d["results"][i]["vehicle"]["body_type"][0]["name"])
        print("Year: " + d["results"][i]["vehicle"]["year"][0]["name"])
        print("Model: " + d["results"][i]["vehicle"]["make_model"][0]["name"])
        print("\n")
        
        vehicles.append((d["results"][i]["plate"],
                         d["results"][i]["vehicle"]["make"][0]["name"],
                         d["results"][i]["vehicle"]["body_type"][0]["name"],
                         d["results"][i]["vehicle"]["year"][0]["name"],
                         d["results"][i]["vehicle"]["make_model"][0]["name"]))
        
                         
    print(vehicles)
    

#--------------------------------VidCam.py------------------------------------------

def make_and_send_frame1(fileName, frame_rate):
    cam = cv2.VideoCapture(fileName) 
    currentframe = 0

    while(True):
        
        for i in range(frame_rate):
            ret,frame = cam.read()
            
        if ret: 
            # if video is still left continue creating images 
            name = './data/frame' + str(currentframe) + '.jpg'
            #print ('Creating...' + name)

            
            # writing the extracted images 
            cv2.imwrite(name, frame)
            threading.Thread(target = recog, args=(name,)).start()
      
            currentframe += 1
            
        else: 
            break
  
    cam.release() 
    cv2.destroyAllWindows()
    

def startVidCam(fileName, frame_rate):
    try: 
      
        # creating a folder named data 
        if not os.path.exists('data'): 
            os.makedirs('data') 
      
    # if not created then raise error 
    except OSError: 
        print ('Error: Creating directory of data')
        
    threading.Thread(target = make_and_send_frame1, args=(fileName, frame_rate,)).start()


#--------------------------------PhoneCam.py------------------------------------------

def make_and_send_frame2(url, delay):
    currentframe = 0

    while(True):

        imgResp = urllib.request.urlopen(url)
        imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
        frame = cv2.imdecode(imgNp, -1)  
        # reading from frame
            
        name = './data/frame' + str(currentframe) + '.jpg'
        #print('Creating...' + name)

            
            # writing the extracted images 
        cv2.imwrite(name, frame)

        threading.Thread(target = recog, args=(name,)).start()
    
        currentframe += 1
            
        time.sleep(delay)
      
    # Release all space and windows once done 
    cam.release() 
    cv2.destroyAllWindows()
    

def startPhoneCam(url, delay):
    
    cam = cv2.VideoCapture(0)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
      
    try: 
          
        # creating a folder named data 
        if not os.path.exists('data'): 
            os.makedirs('data') 
      
    # if not created then raise error 
    except OSError: 
        print ('Error: Creating directory of data') 
    
    threading.Thread(target = make_and_send_frame2, args=(url,delay,)).start()



#--------------------------------WebCam.py------------------------------------------
''' 
# Read the video from specified path 
cam = cv2.VideoCapture(0) 
  
try: 
      
    # creating a folder named data 
    if not os.path.exists('data'): 
        os.makedirs('data') 
  
# if not created then raise error 
except OSError: 
    print ('Error: Creating directory of data') 
  
# frame 
currentframe = 0


while(True):
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
      
    # reading from frame 
    ret,frame = cam.read()
    
    if ret: 
        # if video is still left continue creating images 
        name = './data/frame' + str(currentframe) + '.jpg'
        print ('Creating...' + name)

        
        # writing the extracted images 
        cv2.imwrite(name, frame) 
  
        # increasing counter so that it will 
        # show how many frames are created 
        currentframe += 1

        o(name)
        
        
    else: 
        break
    time.sleep(1)
  
# Release all space and windows once done 
cam.release() 
cv2.destroyAllWindows() 
'''

#--------------------------------main.py-----------------------------------------


def action(option,arg1,arg2):
    
    if option == 0:
        fileName = arg1
        threading.Thread(target = recog, args=(fileName,)).start()

    elif option == 1:
        fileName = arg1
        frame_rate = arg2                             #in fps
        #startVidCam(fileName,frame_rate)
        threading.Thread(target = startVidCam, args=(fileName,frame_rate,)).start()
        
    elif option == 2:
        url = arg1
        delay = arg2                                #in seconds
        #startPhoneCam(url, delay)
        threading.Thread(target = startPhoneCam, args=(url,delay,)).start()
        
    elif option == 3:
        delay = arg1                                  #in seconds
        threading.Thread(target = startWebCam, args=(delay,)).start()

    else:
        print("Enter correct arguments!")

#action(1, "sample vid.mp4", 60)



