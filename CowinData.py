import requests
import  json
import datetime
from dateutil.relativedelta import relativedelta
import  time
#import  multiprocessing
import threading
token='1849435569:AAHDYqbL-rIimeMyPVaPfoghkySHa6aqoKA'
url_getUpdate = "https://api.telegram.org/bot"+token+"/getUpdates"
url_sendMessage="https://api.telegram.org/bot"+token+"/sendMessage?chat_id="
headers = {
    'accept': 'application/json',
    'Accept-Language':'hi_IN',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'upgrade-insecure-requests': '1',
    'sec-fetch-user': '?1'
    }
user_last_msg={}
userAt_step={}
states_map={}
user_setAletrs={}
user_type={}
user_selected_age={}
use_al_len=0
max_UpdatedID=0
messagesQued=[]
botIdeal=True
welcomeMsg='Welcome to Cowin Bot \n Please Choose \n 1. Set Alert \n 2. View Center List'
ageMsg='Select Age\n 1. 18+\n 2. 45+'
searchMsg='Select Searh criteria \n 1. By Pincode \n 2. State Name and District Name'
allStates='{"states":[{"state_id":1,"state_name":"Andaman and Nicobar Islands"},{"state_id":2,"state_name":"Andhra Pradesh"},{"state_id":3,"state_name":"Arunachal Pradesh"},{"state_id":4,"state_name":"Assam"},{"state_id":5,"state_name":"Bihar"},{"state_id":6,"state_name":"Chandigarh"},{"state_id":7,"state_name":"Chhattisgarh"},{"state_id":8,"state_name":"Dadra and Nagar Haveli"},{"state_id":37,"state_name":"Daman and Diu"},{"state_id":9,"state_name":"Delhi"},{"state_id":10,"state_name":"Goa"},{"state_id":11,"state_name":"Gujarat"},{"state_id":12,"state_name":"Haryana"},{"state_id":13,"state_name":"Himachal Pradesh"},{"state_id":14,"state_name":"Jammu and Kashmir"},{"state_id":15,"state_name":"Jharkhand"},{"state_id":16,"state_name":"Karnataka"},{"state_id":17,"state_name":"Kerala"},{"state_id":18,"state_name":"Ladakh"},{"state_id":19,"state_name":"Lakshadweep"},{"state_id":20,"state_name":"Madhya Pradesh"},{"state_id":21,"state_name":"Maharashtra"},{"state_id":22,"state_name":"Manipur"},{"state_id":23,"state_name":"Meghalaya"},{"state_id":24,"state_name":"Mizoram"},{"state_id":25,"state_name":"Nagaland"},{"state_id":26,"state_name":"Odisha"},{"state_id":27,"state_name":"Puducherry"},{"state_id":28,"state_name":"Punjab"},{"state_id":29,"state_name":"Rajasthan"},{"state_id":30,"state_name":"Sikkim"},{"state_id":31,"state_name":"Tamil Nadu"},{"state_id":32,"state_name":"Telangana"},{"state_id":33,"state_name":"Tripura"},{"state_id":34,"state_name":"Uttar Pradesh"},{"state_id":35,"state_name":"Uttarakhand"},{"state_id":36,"state_name":"West Bengal"}],"ttl":24}'
jStates=json.loads(allStates)
jLen=len(jStates["states"])-1
state_message='Please Choose a state\n'
for x in range(0,jLen,1):
    state_message+= str(x+1)+'. '+jStates["states"][x]["state_name"]+'\n'
    states_map[x+1]=jStates["states"][x]["state_id"]    
state_message+='Example 1 for Andaman and Nicobar Islands'

def getDisDetails(state_code):
    url_districts="https://cdn-api.co-vin.in/api/v2/admin/location/districts/"+state_code
    response = requests.get(url_districts, headers=headers)
    data=response.text
    getDisList=json.loads(data)
    return getDisList  

def getByDisURL(district_code):
     url_vac_list="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
     one_year_from_now = datetime.datetime.now()+relativedelta(days=0)
     date_formated = one_year_from_now.strftime("%d-%m-%Y")
     url_vac_listl=url_vac_list+'?district_id='+str(district_code)+'&date='+str(date_formated)
     print(url_vac_listl)
     return url_vac_listl

def getByPinUrl(district_code):
    url_vac_list="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"
    one_year_from_now = datetime.datetime.now()+relativedelta(days=0)
    date_formated = one_year_from_now.strftime("%d-%m-%Y")
    url_vac_listl=url_vac_list+'?pincode='+str(district_code)+'&date='+str(date_formated)
    print(url_vac_listl) 
    return url_vac_listl
 
def getCenterList(code,age,search_by):
    url_vac_listl=''
    if(search_by==1):
        url_vac_listl=getByDisURL(code)
    elif(search_by==2): 
        url_vac_listl=getByPinUrl(code)
    else:
        url_vac_listl=search_by
    response = requests.get(url_vac_listl, headers=headers)
    raw_vac_data=response.text
    j_vac_data=json.loads(raw_vac_data)
    j_len=len(j_vac_data["centers"])
    message='---------------------\n'
    NoslotCheck=True
    for x in range (0,j_len,1):
        ses_len=len(j_vac_data["centers"][x]["sessions"])
        for k in range(0,ses_len,1):
            avail=j_vac_data["centers"][x]["sessions"][k]["available_capacity"]
            avail_age=j_vac_data["centers"][x]["sessions"][k]["min_age_limit"] 
            if(avail>0 and avail_age==int(age)):
                message+='Center Name: '+str(j_vac_data["centers"][x]["name"])+'\n'
                message+='Age Limit: '+str(j_vac_data["centers"][x]["sessions"][k]["min_age_limit"])+'+\n'
                message+='Vaccine: '+str(j_vac_data["centers"][x]["sessions"][k]["vaccine"])+'\n'
                message+='Fees Type: '+str(j_vac_data["centers"][x]["fee_type"])+'\n'
                message+='Date: '+str(j_vac_data["centers"][x]["sessions"][k]["date"])+'\n'
                message+='---------------------\n'
                NoslotCheck=False
    if(NoslotCheck):
        message+='No Slots Availabe\n'
        message+='---------------------\n'        
    return message

def getMaxIdPos(max_id,getLatestMessage,k):
    for x in range(0,k,1):
        m=getLatestMessage["result"][x]["update_id"]
        if(int(m)==int(max_id)):
            return x

def getUpdates(max_UpdatedID):
    response = requests.get(url_getUpdate, headers=headers)
    data=response.text
    getLatestMessage=json.loads(data)
    messages_len=len(getLatestMessage["result"])
    if(messages_len)>0:
        latest_messageUpID=getLatestMessage["result"][messages_len-1]["update_id"]
        print(max_UpdatedID,latest_messageUpID)
        pos_last_upID=getMaxIdPos(max_UpdatedID,getLatestMessage,messages_len)+1
        if(max_UpdatedID<latest_messageUpID):
             botIdeal=False
             for x in range(pos_last_upID,messages_len,1):
                  message_data=getLatestMessage["result"][x]["message"]["text"]
                  message_id=getLatestMessage["result"][x]["message"]["message_id"]
                  chat_id=getLatestMessage["result"][x]["message"]["chat"]["id"]
                  chat_type=message_data.isnumeric()
                  final_m=str(chat_id)+','+str(message_data)+','+str(chat_type)+','+str(message_id)
                  messagesQued.append(str(final_m))
                  print(x)
        else:
           botIdeal=True
        return latest_messageUpID
    else:
        return 0

def sendMessage(chatID,message):
    sen_to=url_sendMessage+chatID+'&text='+message
    requests.get(sen_to, headers=headers)
             
def consumeMessages():
    queLen=len(messagesQued)
    if(queLen>0):
        message=messagesQued[0].split(",")
        processMessage(message[0],message[1],message[2],message[3])
        print(message)
        messagesQued.pop(0)  
        
def resetAllonError(chat_id):
    userAt_step.pop(str(chat_id))
    
def getAge(age):
    if(int(age)==1):
        return 18
    else:
        return 45
    
def getStepMessage(step,message,chat_id,age):
    if(step==0):
        return state_message
    elif(step==1):
        getDisList=getDisDetails(message)
        messages_len=len(getDisList["districts"])
        message="Select City\n"
        for x in range(0,messages_len,1):
            message+= str(x+1)+'. '+getDisList["districts"][x]["district_name"]+'\n'
        message+='Example 1 for '+getDisList["districts"][0]["district_name"]
        return message
    elif(step==2):
       state_code=int(user_last_msg[str(chat_id)]) 
       getDisList=getDisDetails(str(state_code))
       dis_code=getDisList["districts"][int(message)-1]["district_id"]
       age=getAge(age)
       message=getCenterList(int(dis_code),str(age),1)           
       return message
  
def getSearchType(chat_id,message,type_me,message_id):
    if(userAt_step.get(str(chat_id))==3 and str(message)=='1'):
        sendMessage(chat_id,'Please Enter Pincode')
        userAt_step[str(chat_id)]=4
    elif(userAt_step.get(str(chat_id))==3 and str(message)=='2'):
        sendMessage(chat_id,state_message)
        userAt_step[str(chat_id)]=4

def processMessagesForAlert(chat_id,message,type_me,message_id):
    if(userAt_step.get(str(chat_id))==2):
        user_selected_age[str(chat_id)]=str(message)
        sendMessage(chat_id,searchMsg)
        userAt_step[str(chat_id)]=3
    elif(userAt_step.get(str(chat_id))==3):
        getSearchType(chat_id,message,type_me,message_id)
    elif(userAt_step.get(str(chat_id))==4 and len(message)>2):
        sendMessage(chat_id,'\nThanks For using servie Alert is set, send (/start) start again')
        user_setAletrs[str(chat_id)]=getByPinUrl(str(message))
        userAt_step[str(chat_id)]=6
    elif(userAt_step.get(str(chat_id))==4):
        state_code=states_map.get(int(message))
        step_messagemessage=getStepMessage(1,str(state_code),chat_id,0)
        sendMessage(str(chat_id),step_messagemessage)
        userAt_step[str(chat_id)]=5
        user_last_msg[str(chat_id)]=state_code
    elif(userAt_step.get(str(chat_id))==5):
        step_messagemessage='\n Thanks For using servie Alert is set, send (/start) start again'
        sendMessage(str(chat_id),step_messagemessage)
        state_code=int(user_last_msg[str(chat_id)]) 
        getDisList=getDisDetails(str(state_code))
        dis_code=getDisList["districts"][int(message)-1]["district_id"]
        user_setAletrs[str(chat_id)]=getByDisURL(dis_code)
        user_last_msg.pop(str(chat_id))
        userAt_step.pop(str(chat_id))
        user_type.pop(str(chat_id))
    elif(userAt_step.get(str(chat_id))==6):
        resetAllonError(chat_id)
        user_type.pop(str(chat_id))
    else:
        sendMessage(chat_id,"Invalid Option Choosed")
        resetAllonError(chat_id)
        user_type.pop(str(chat_id))
   
def processMessagesForCenterView(chat_id,message,type_me,message_id):
    if(userAt_step.get(str(chat_id))==2):
        user_selected_age[str(chat_id)]=str(message)
        sendMessage(chat_id,searchMsg)
        userAt_step[str(chat_id)]=3
    elif(userAt_step.get(str(chat_id))==3):
        getSearchType(chat_id,message,type_me,message_id)
    elif(userAt_step.get(str(chat_id))==4 and len(message)>2):
        age=str(user_selected_age.get(str(chat_id)))
        age=getAge(age)
        sendMessage(chat_id,str(getCenterList(str(message),str(age),2)))
        userAt_step[str(chat_id)]=6
    elif(userAt_step.get(str(chat_id))==4):
        state_code=states_map.get(int(message))
        step_messagemessage=getStepMessage(1,str(state_code),chat_id,0)
        sendMessage(str(chat_id),step_messagemessage)
        userAt_step[str(chat_id)]=5
        user_last_msg[str(chat_id)]=state_code
    elif(userAt_step.get(str(chat_id))==5):
        step_messagemessage=getStepMessage(2,message,chat_id,str(user_selected_age[str(chat_id)]))
        step_messagemessage+='\n Thanks For using servie send (/start) start again'
        sendMessage(str(chat_id),step_messagemessage)
        user_last_msg.pop(str(chat_id))
        userAt_step.pop(str(chat_id))
        user_type.pop(str(chat_id))
    elif(userAt_step.get(str(chat_id))==6):
        resetAllonError(chat_id)
        user_type.pop(str(chat_id))
    else:
        sendMessage(chat_id,"Invalid Option Choosed")
        resetAllonError(chat_id)
        user_type.pop(str(chat_id))
      
def processMessage(chat_id,message,type_me,message_id):
    if(str(type_me).lower()=='false' and str(message).lower()=='/start'):
        sendMessage(chat_id,welcomeMsg)
        user_last_msg[str(chat_id)]=str(message)
        userAt_step[str(chat_id)]=1
    elif(str(userAt_step.get(str(chat_id)))=='None'):
        sendMessage(chat_id,'Please send /start to start again')
    elif(str(type_me).lower()=='false' and str(message).lower()!='/start'):
        sendMessage(chat_id,'Invalid Option Please select again.') 
    elif(userAt_step.get(str(chat_id))==1 and str(message)=='1'):
        user_type[str(chat_id)]=1
        userAt_step[str(chat_id)]=2
        sendMessage(chat_id,ageMsg)
    elif(userAt_step.get(str(chat_id))==1 and str(message)!='1'):
        userAt_step[str(chat_id)]=2
        user_type[str(chat_id)]=2
        sendMessage(chat_id,ageMsg)
    elif(userAt_step.get(str(chat_id))>1 and user_type.get(str(chat_id))==1):
        processMessagesForAlert(chat_id, message, type_me, message_id)
    elif(userAt_step.get(str(chat_id))>1 and user_type.get(str(chat_id))==2):
        processMessagesForCenterView(chat_id, message, type_me, message_id)

def updtesProcess(maxId):
    t=1
    while True:
        if (t==1):
            maxId='127749753'
        max_UpdatedID=getUpdates(int(maxId))
        maxId=max_UpdatedID
        consumeMessages()
        time.sleep(1)
        print(user_setAletrs)
        t=2
        print('in')
        
def consueProcess():
        while True:
             if(botIdeal and len(user_setAletrs)>0):
                 time.sleep(2)
                 for x in  user_setAletrs:
                    age=str(user_selected_age.get(str(x)))
                    age=getAge(age)
                    center_data=getCenterList(0,age,str(user_setAletrs.get(x)))
                    pos=center_data.find("No Slots Availabe")
                    if(pos==-1):
                        sendMessage(x,'Slots Are Available Now \nList Of Centers\n')
                        sendMessage(x,center_data)
                        sendMessage(x, '\n Visit https://selfregistration.cowin.gov.in/ and register \n Thanks for use cowin bot')
                        user_setAletrs.pop(x)
            
             time.sleep(30)

t1 = threading.Thread(target=updtesProcess, args=(str(max_UpdatedID)))
t2 = threading.Thread(target=consueProcess)
  
    # starting thread 1
t1.start()
# starting thread 2
#t2.start()
  
 # wait until thread 1 is completely executed
t1.join()
# wait unti
#t2.join()


