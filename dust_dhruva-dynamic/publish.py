import random
import time

from paho.mqtt import client as mqtt_client

broker = 'broker.emqx.io'
port = 1883
topic = "dust_particle_data"


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

data = {'id':1, 'dust': 100000}

def publish(client):
   
    while True:
        random_id = random.randint(1,5)
        # print("random_id",random_id)
        random_dust = random.randint(100000,999999)
        # print("random_dust",random_dust)

        data['id'] = random_id
        data['dust'] = random_dust
        time.sleep(1)
        msg = f"{data}"
        result = client.publish(topic, msg)
    #     result: [0, 1]
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
