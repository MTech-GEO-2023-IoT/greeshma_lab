
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
    apiDeviceID="8062300084cca891796a"
)

devices = c.getdevices()
# print("Device List: %r" % devices)

# Create a connection to MySQL Database
conn = pymysql.connect(database="workingtime", user="user", password="PASS", host="localhost")
# Create a MySQL Cursor that executes the SQLs
cur = conn.cursor()

# Create the sensordata
cur.execute("""
CREATE TABLE sensordata1 (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    timestamp INT NOT NULL,
    sw1 BOOLEAN NOT NULL,
    P1 INT NOT NULL,
    sw2 BOOLEAN NOT NULL,
    P2 INT NOT NULL,
    sw3 BOOLEAN NOT NULL,
    P3 INT NOT NULL,
    sw4 BOOLEAN NOT NULL,
    P4 INT NOT NULL
);
""")
# MQTT Callback function for handling received messages
def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    print("Received payload:", payload)

# Create an MQTT client and set the callback function
client = mqtt.Client()
client.on_message = on_message

# Connect to the MQTT broker and subscribe to the topic
client.connect("0.0.0.0", 1883, 60)
client.subscribe("sensordata1")
client.loop_start()

while True:
    result = c.getstatus("8062300084cca891796a")
    print("Status of device:\n", result)
    sw1 = result["result"][0]['value']
    # print(sw1)
    sw2 = result["result"][1]['value']
    # print(sw2)
    sw3 = result["result"][2]['value']
    # print(sw3)
    sw4 = result["result"][3]['value']
    # print(sw4)
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

    # Publish the data to the MQTT broker
    payload = sw4
    client.publish("sensordata1", payload)

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
        INSERT INTO sensordata1 (timestamp, sw1, P1, sw2, P2, sw3, P3, sw4, P4)
        VALUES (UNIX_TIMESTAMP(), %(sw1)s, %(P1)s, %(sw2)s, %(P2)s, %(sw3)s, %(P3)s, %(sw4)s, %(P4)s);
    """, {'sw1': sw1, 'P1': P1, 'sw2': sw2, 'P2': P2, 'sw3': sw3, 'P3': P3, 'sw4': sw4, 'P4': P4})

    # Commit the data to the database
    conn.commit()

    # Wait for 1 minute before capturing the next data
    time.sleep(60)
import pymysql

# Create a connection to MySQL Database
conn = pymysql.connect(database="workingtime", user="user", password="PASS", host="localhost")
# Create a MySQL Cursor that executes the SQLs
cur = conn.cursor()

# Calculate average time worked per hour
cur.execute("SELECT HOUR(FROM_UNIXTIME(timestamp)) AS hour, AVG(P1 + P2 + P3 + P4) AS avg_power FROM sensordat>
average_data = cur.fetchall()

for row in average_data:
    minute = row[0]
    avg_power = row[1]
    print("minute:", minute)
    print("Average Power Consumption:", avg_power)

# Calculate total electricity consumption
cur.execute("SELECT SUM(P1 + P2 + P3 + P4) AS total_power FROM sensordata1;")
total_power = float(cur.fetchone()[0])

print("Total Power Consumption:", total_power)
 
Electricity = total_power *  minute/60

# Calculate carbon emission
carbon_emission = (Electricity / 1000) * 0.85
print("Carbon Emission in kg of co2 :", carbon_emission)


