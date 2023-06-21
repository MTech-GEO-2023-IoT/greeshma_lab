
import tinytuya,json

# tinytuya.set_debug(True)

c = tinytuya.Cloud(
        apiRegion="in", 
        apiKey="fg84rkadavg8u3buzodi", 
        apiSecret="cff6cca0f15346f682b59ea86123f56c", 
        apiDeviceID="8062300084cca891796a")

devices = c.getdevices()
# print("Device List: %r" % devices)

result = c.getstatus("8062300084cca891796a")
print("Status of device:\n", result)
sw1 = result["result"][0]['value']
#print(sw1)
sw2 = result["result"][1]['value']
#print(sw2)
sw3 = result["result"][2]['value']
#print(sw3)
sw4 = result["result"][3]['value']
#print(sw4)


#Here the conversion co efficent used for the electrical energy to carbon foot print = .95 per kWh
#bulb socket
if sw1==True:
   P1 = 10
else: 
   P1 = 0

if sw2==True:
   P2 = 15
else: 
   P2 = 0
#charger point
if sw3==True:
   P3 = 50
else: 
   P3 = 0
if sw4==True:
   P4 = 75
else: 
   P4 = 0 

print(P1, P2, P3, P4)


 

import paho.mqtt.client as mqtt

payload=sw4
topic="t"
client = mqtt.Client()
client.connect('0.0.0.0',1883,60)
(rc,mid)=client.publish(topic,payload);
client.disconnect();


