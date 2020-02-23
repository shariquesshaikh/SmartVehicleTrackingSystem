import requests
import json

URL = 'https://www.sms4india.com/api/v1/sendCampaign'


def sendPostRequest(reqUrl, apiKey, secretKey, useType, phoneNo, senderId, textMessage):
  req_params = {
  'apikey':apiKey,
  'secret':secretKey,
  'usetype':useType,
  'phone': phoneNo,
  'message':textMessage,
  'senderid':senderId
  }
  return requests.post(reqUrl, req_params)

def get_response(number,color,model): #number,color,make
    x="Vehicle with number "+number+" and color "+color+" with "+model+" has been spotted near Cam1."
    response = sendPostRequest(URL, '5JOLWYTFTHGZMTXW3YSR4EEBN6IGDQO0', 'ORU4EL60WBSCOUQS', 'stage', '8104150837', 'sharique29311@gmail.com', x)







