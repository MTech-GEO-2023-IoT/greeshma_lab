import tinytuya
import json
import pymysql
import paho.mqtt.client as mqtt
import time

# tinytuya.set_debug(True)

c = tinytuya.Cloud(
        apiRegion="in", 
        apiKey="fg84rkadavg8u3buzodi", 
        apiSecret="cff6cca0f15346f682b59ea86123f56c", 
        apiDeviceID="8062300084cca891796a")

devices = c.getdevices()
# print("Device List: %r" % devices)

# Create a connection to MySQL Database
conn = pymysql.connect(database="workingtime", user="user", password="PASS", host="localhost")
# Create a MySQL Cursor that executes the SQLs
cur = conn.cursor()

while True:
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
    # Here the conversion coefficient used for the electrical energy to carbon footprint = 0.95 per kWh
    # Bulb socket
    if sw1 == True:
        P1 = 10
    else:
        P1 = 0
    if sw2 == True:
        P2 = 15
    else:
        P2 = 0
    # Charger point
    if sw3 == True:
        P3 = 50
    else:
        P3 = 0
    if sw4 == True:
        P4 = 75
    else:
        P4 = 0 

    print(P1, P2, P3, P4)

    payload = sw4
    topic = "sensordata"
    client = mqtt.Client()
    client.connect('0.0.0.0', 1883, 60)
    rc, mid = client.publish(topic, payload)
    client.disconnect()

    # Create a dictionary containing the fields, switch, and its power data
    data = {
        'sw1': sw1,
        'P1': P1,
        'sw2': sw2,
        'P2': P2,
        'sw3': sw3,
        'P3': P3,
        'sw4': sw4,
        'P4': P4
    }
    # Execute the SQL query to insert data into the database
    cur.execute("""
        INSERT INTO sensordata (timestamp, sw1, P1, sw2, P2, sw3, P3, sw4, P4)
        VALUES (UNIX_TIMESTAMP(), %(sw1)s, %(P1)s, %(sw2)s, %(P2)s, %(sw3)s, %(P3)s, %(sw4)s, %(P4)s);
    """, data)
    # Commit the data to the database
    conn.commit()

    # Wait for 1 minute before capturing the next data
    time.sleep(60)

# Close the cursor
cur.close()
# Close the connection to the database
conn.close()
