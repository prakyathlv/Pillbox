import my_conf,conf1
from boltiot import Bolt,Sms
import json, time
from datetime import datetime
import pytz

threshold=500
j=0

n = int(input("how many times do you take pills in a day :"))
x = {}

for i in range(n):
    keys = i  
    values = (input('enter the pill taking time in HH:MM:SS format only '))
    x[keys] = values
pill_time=sorted(x.values())

mybolt = Bolt(my_conf.API_KEY, my_conf.DEVICE_ID)
sms = Sms(conf1.SID, conf1.AUTH_TOKEN, conf1.TO_NUMBER, conf1.FROM_NUMBER)

def default():
      mybolt.digitalWrite('3','LOW')
      mybolt.digitalWrite('4','LOW')       
      mybolt.digitalWrite('1','HIGH')
     
default()

def take_pill():
   mybolt.digitalWrite('3','HIGH')
   mybolt.digitalWrite('4','HIGH')
   mybolt.digitalWrite('1','LOW')
  
def light_intensity():
    response = mybolt.analogRead('A0') 
    data = json.loads(response) 
    print("Sensor value is: " + str(data['value']))
    return int(data['value'])

def get_time():
    tz_IN = pytz.timezone('Asia/Kolkata') 
    datetime_IN = datetime.now(tz_IN)
    current_time=datetime_IN.strftime("%H:%M:%S")
    print("current time is:",current_time)
    return current_time

def send_sms():
   response = sms.send_sms("Remainder to take your pills😊")
   print("Status of SMS at Twilio is :" + str(response.status))

def test():
  for i in range(n):
      current_time=get_time()
      if(current_time<=pill_time[i]):
        break     
  return i
    
j=test()

while True: 
    try:
        current_time=get_time()
        print("next pill taking time is:",pill_time[j])
        sensor_value = light_intensity()

        if current_time>=pill_time[j] and sensor_value<=threshold:
          send_sms()
          while True:
            print("\n")
            take_pill()
            sensor_value = light_intensity()
            
            if(sensor_value>threshold):
              default()
              j=j+1
              if(j==n):
                j=0
                while(current_time>pill_time[j]):
                  default()
                  time.sleep(7)
                  print("\n")
                  light_intensity()
                  get_time()
                  print("next pill time is:",pill_time[j])
                  print("one")
              else:
                if(current_time<=pill_time[j]):
                  break
                while(current_time<=pill_time[j]):
                  default()
                  time.sleep(7)
                  print("\n")
                  light_intensity()
                  get_time()
                  print("next pill time is:",pill_time[j])
                  print("two")
    
    except Exception as e: 
        print ("Error occured: Below are the details")
        print (e)
   
    default()
 
    print('\n')   
    time.sleep(7)


