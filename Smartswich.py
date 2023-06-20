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
print(sw1)








''''
{'result': [{'code': 'switch_1', 'value': True}, {'code': 'switch_2', 'value': True}, 
{'code': 'switch_3', 'value': True}, {'code': 'switch_4', 'value': True}, {'code': 'countdown_1', 'value': 0}, 
{'code': 'countdown_2', 'value': 0}, {'code': 'countdown_3', 'value': 0}, {'code': 'countdown_4', 'value': 0}], 
'success': True, 't': 1687233241579, 'tid': '17a8867b0f1e11ee8d5f9e9bc4b5c240'}
''''
