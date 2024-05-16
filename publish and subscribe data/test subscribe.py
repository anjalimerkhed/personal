import paho.mqtt.client as mqtt
import time


def on_connect(client,usedata,flags,rc):
    if rc==0:
        print("Client is connected")
        global connected
        connected=True
    else:
        print("Client is not connected")
def on_message(client,userdata,message):
    print("Message received: "+ str(message.payload.decode("utf-8")))
    print("Topic: "+ str(message.topic))

connected=False
Messagereceived=False
broker_address="107.180.94.60"
port=18889

client=mqtt.Client("MQTT")
client.on_connect=on_connect
client.on_message=on_message
client.connect(broker_address,port=port)
client.loop_start()
client.subscribe("#")
while connected!=True:
    time.sleep(10)
while Messagereceived!=True:
    time.sleep(10)
    
client.loop_stop()
