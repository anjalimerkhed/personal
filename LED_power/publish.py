import random
import time
from paho.mqtt import client as mqtt_client

broker = 'broker.emqx.io'
port = 1883
topic = "power_consumption"


client_id = f'publish-{random.randint(0, 1000)}'

def connect_mqtt():
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

data = {}

def publish(client):
   
    while True:
        random_id = random.randint(1, 10)
        random_int = random.randint(1, 100)
        random_power = random.randint(1, 100)
        random_temp = random.uniform(25, 45)
        random_lux = random.randint(500, 1000)

        data['device_id'] = f'led{random_id}'
        data['intensity'] = random_int
        data['power'] = random_power
        data['temp'] = round(random_temp, 2)
        data['lux'] = round(random_lux, 2)

        time.sleep(10)
        msg = f"{{'device_id':{data['device_id']}:{data['intensity']}:{data['power']}:{data['temp']}:{data['lux']}}}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]

        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
     


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)
    client.loop_stop()


if __name__ == '__main__':
    run()
