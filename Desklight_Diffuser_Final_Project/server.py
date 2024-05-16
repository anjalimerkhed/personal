import time
import sqlite3
import paho.mqtt.client as mqtt
import schedule
import re

# MQTT broker details
mqtt_broker = 'mqtt.evoluzn.in'
mqtt_port = 18889
# topic_desklight = 'desklightAAAAA6/control'
# desklight_sub_topic = 'desklightAAAAA6/status'
# diffuser_sub_topic = "diffuserAAAAA5/status"
# topic_diffuser = "diffuserAAAAA5/control"
mqttc = mqtt.Client()
# publish_messages_100 = {100}
# publish_messages_100 = {i for i in range(1, 256)}
# publish_messages_0 = {0}
# numeric_value = None
# publish_200_job = None
# publish_messages_100 = "{'device_id:led{SrNo}:100"
# publish_messages_0 = "{'device_id:led{SrNo}:0"



def connect_to_mqtt():
    try:
        mqttc.connect(mqtt_broker, mqtt_port)
    except Exception as e:
        print(f"Error connecting to MQTT broker: {e}")

def check_schedule():
    # global publish_messages_100, publish_messages_0, numeric_value
    try:
        conn = sqlite3.connect('scheduling.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM scheduling')
        scheduled_events = cursor.fetchall()

        current_time = time.strftime('%H:%M')

        for scheduled_event in scheduled_events:
            SrNo = scheduled_event[1]
            ScheduleStartTime = scheduled_event[2]
            ScheduleEndTime = scheduled_event[3]
            scheduling = scheduled_event[4]

            if scheduling == 0:
                if current_time >= ScheduleStartTime and current_time < ScheduleEndTime:
                    # if numeric_value != int(next(iter(publish_messages_100))):
                        # Publish messages to both topics with the same value
                        mqttc.publish(f'{SrNo}/control', "Light:100")
                        mqttc.publish(f'{SrNo}/control', "diffuser:100")
                        print(f"Publishing_100 for SrNo: {SrNo}")
                elif current_time == ScheduleEndTime:
                    # if numeric_value != int(next(iter(publish_messages_0))):
                        # Publish messages to both topics with the same value
                        mqttc.publish(f'{SrNo}/control', "Light:0")
                        mqttc.publish(f'{SrNo}/control', "diffuser:0")
                        print(f"Publishing_0 for SrNo: {SrNo}")

        conn.close()

    except Exception as e:
        print(f"An error occurred: {e}")


# def mqtt_publish():
#     global publish_200_job
#     try:
#         if numeric_value is None:
#             mqttc.publish(topic_desklight, '200')
#             # print("Published 200 to MQTT")
#         elif numeric_value != int(next(iter(publish_messages_100))):
#             mqttc.publish(topic_desklight, '200')
#             # print("Published 200 to MQTT")
#         else:
#             schedule.cancel_job(publish_200_job) 
#             publish_200_job = None 
#     except Exception as e:
#         print(f"Error publishing message to MQTT: {e}")

# def on_connect(client, userdata, flags, rc):
#     try:
#         if rc == 0:
#             mqttc.subscribe(diffuser_sub_topic)
#             mqttc.subscribe(desklight_sub_topic)
#             print(f"Subscribed to MQTT topic: {diffuser_sub_topic}")
#             print(f"Subscribed to MQTT topic: {desklight_sub_topic}")
#         else:
#             print(f"Connection to MQTT broker failed with result code {rc}")
#     except Exception as e:
#         print(f"Error in on_connect: {e}")

        
# def on_message(client, userdata, message):
#     global received_message, numeric_value
#     try:
#         received_message = message.payload.decode()
#         topic = message.topic
#         if topic == diffuser_sub_topic:
#             numeric_value = int(received_message.split(":")[2])
#             print("Diffuser numeric value:", numeric_value)
#             # Handle diffuser value here
#         elif topic == desklight_sub_topic:
#             numeric_value = int(received_message.split(":")[2])
#             print("Desklight numeric value:", numeric_value)
#             # Handle desklight value here
#         else:
#             print("Unknown topic:", topic)
#     except Exception as e:
#         print(f"Error handling message: {e}")


# schedule.every(20).seconds.do(mqtt_publish)

# mqttc.on_connect = on_connect
# mqttc.on_message = on_message

connect_to_mqtt() 
schedule.every(60).seconds.do(check_schedule)

while True:
    schedule.run_pending()
    mqttc.loop(timeout=5)
    time.sleep(1)
