import paho.mqtt.client as mqtt
import time
import random    

connected=True

def on_connect(client,usedata,flags,rc):
    if rc==0:
        print("Connection Sucess")
    else:
        print("Connection Failed")
broker_address="107.180.94.60"
port= 18889
client =mqtt.Client("Evoluzn")
client.on_connect =on_connect
client.connect(broker_address,port=port)
client.loop_start()
while connected!=True:
    time.sleep(10)
while True:
    num = random.randint(1, 8)
    print("num",num)
    power = random.randint(0000, 9999)
    print("power",power)
    statues = ['active', 'inactive', 'idle']
    status = random.choice(statues)

    payload = f"{{ID: {num}, name: M{num}, pwc: {power}, status: {status}}}"
    client.publish("powerconsumption/status",payload)
    # client.loop_stop()
    time.sleep(10)