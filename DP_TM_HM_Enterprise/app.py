from flask import Flask, render_template, jsonify, request, url_for, redirect, session
from flask_cors import CORS
from datetime import datetime
from database import mydb,cursor
import random
from paho.mqtt import client as mqtt_client

app = Flask(__name__) 
CORS(app)

broker = 'mqtt.evoluzn.in'
port = 18889
topic = "thdpF0BDE7/status"
client_id = f'python-mqtt-{random.randint(0, 1000)}'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    # client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def on_message(client, userdata, message):
    print("message received ", str(message.payload.decode("utf-8")))
    value = str(message.payload.decode("utf-8"))
    print("value", value)
    topic = message.topic
    print("topic :" , topic)
    
    # Define the expected prefix for the topic
    expected_prefix = "thdp"

    # Check if the received topic starts with the expected prefix
    if topic.startswith(expected_prefix):
        print('topic matched')
        
        # Remove the leading and trailing braces
        value_str = value.strip("{}")

        # Split the string by colon
        components = value_str.split(":")

        # Extract values
        device_name = components[1]
        temperature = components[2]
        humidity = components[3]
        dp = components[4]
        # Print extracted values
        print("Device Name:", device_name)
        print("Temperature:", temperature)
        print("Humidity:", humidity)
        print("DP:", dp)

def subscribe(client):
    client.on_message = on_message 
    print("inside subscribe") 
    client.subscribe("#")
    
   
def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == "__main__":
    run()
    app.run(host="0.0.0.0", port=5005, debug = True)