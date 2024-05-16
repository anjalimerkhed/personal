from flask import Flask, render_template, request, jsonify, redirect, url_for
import paho.mqtt.client as mqtt
import sqlite3
import threading
import time
from flask_socketio import SocketIO


app = Flask(__name__)
socketio = SocketIO(app)

broker = "mqtt.evoluzn.in"
port = 18889
topic = "desklightAAAAA7/control"
topic_diffuser = "diffuserAAAAA5/control"
topic_diffuser_9 = "diffuserAAAAA9/control"
mqttc = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print(f"Failed to connect to MQTT broker with return code {rc}")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Disconnected from MQTT broker. Trying to reconnect...")
        mqttc.reconnect()

# Assuming you have a socketIO connection already set up
led_state = {}
def on_message(client, userdata, message):
    global split_payload
    try:
        payload = message.payload.decode()
        topic = message.topic
        split_payload = payload.split(":")
        print("split_payload:1232",split_payload)
        if len(split_payload) >= 3:
            value = split_payload[2]
            print(f"Received value for topic {topic}: {value}")
            # Emit the value with the corresponding topic name
            if topic == "desklightAAAAA7/status":
                desklight_value = value
                socketio.emit('desklight', {'value': desklight_value})
                socketio.emit('split_desklight', {'split_desklight': split_payload})
                led = split_payload[2]
                print("led",led)
                color = split_payload[3]
                print("color",color)
                led_state['color'] = color
                led_state['intensity'] = led
                socketio.emit('desklight_intensity',led_state)
            elif topic == "diffuserAAAAA5/status":
                diffuser_value = value
                socketio.emit('diffuser', {'value': diffuser_value})
                socketio.emit('split_diffuser', {'split_diffuser': split_payload})
            
        else:
            print("Data not received...")
    except Exception as e:
        print(f"Error processing message: {e}")

# display when water_level_low
# split_payload = [""]
# print("split_payload:", split_payload)
# @app.route('/get_split_payload', methods=['GET'])
# def get_split_payload():
#     global split_payload
#     print("Current value of split_payload:", split_payload)
#     water_level_low = False
#     for item in split_payload:
#         if 'Water Level Low' in item:
#             mqttc.publish(topic_diffuser_9, "diffuser:0")
#             water_level_low = True
#             break  # No need to continue iterating if the condition is met
#     if not water_level_low:
#         mqttc.publish(topic_diffuser_9, "diffuser:100")
#     return jsonify("Water Level High" if water_level_low else "")


#  for water level indication.....  
# split_payload = [""]
# print("split_payload:", split_payload)
# @app.route('/get_split_payload', methods=['GET'])
# def get_split_payload():
#     global split_payload
#     print("Current value of split_payload:", split_payload)
#     for item in split_payload:
#         if 'Water Level Low' in item:
#             mqttc.publish(topic_diffuser_9, "diffuser:0")
#             return jsonify("Water Level Low")
#     return jsonify("")
        

mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_message = on_message

def mqtt_connect():
    try:
        print("Connecting to MQTT broker...")
        mqttc.connect(broker, port)
        mqttc.loop_start()
        mqttc.subscribe("desklightAAAAA7/status")
        mqttc.subscribe("diffuserAAAAA5/status")
        mqttc.subscribe("diffuserAAAAA9/status")
    except Exception as e:
        print(f"Error connecting to MQTT broker: {e}")

# publish 200.....
# def publish_200():
#     try:
#         while True:
#             sms = "200"
#             mqttc.publish(topic, sms)
#             mqttc.publish(topic_diffuser, sms)
#             print("publish_200_after 2 second")
#             time.sleep(5)
#     except Exception as e:
#         print(f"Error publishing MQTT messages: {e}")
# mqtt_publish_thread = threading.Thread(target=publish_200)
# mqtt_publish_thread.start()


mqtt_connect_thread = threading.Thread(target=mqtt_connect)
mqtt_connect_thread.start()


# Nikkys code ...........for on/off
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/turnon/api/', methods=['POST'])
def turnon():
    try:
        mqttc.publish(topic, "Light:100")
        # conn = sqlite3.connect('scheduling.db')
        # cursor = conn.cursor()
        # cursor.execute("UPDATE scheduling SET scheduling = 1")
        # conn.commit()
        # conn.close()

        return jsonify({'response': 'Turned ON successfully'})

    except Exception as e:
        print("Error in turnon API:", e)
        return jsonify({'response': 'Error'}), 500

@app.route('/turnoff/api/', methods=['POST'])
def turnoff_api():
    try:
        mqttc.publish(topic, "Light:0")
        # conn = sqlite3.connect('scheduling.db')
        # cursor = conn.cursor()
        # cursor.execute("UPDATE scheduling SET scheduling = 1")
        # conn.commit()
        # conn.close()

        return jsonify({'response': 'Turned OFF successfully'})
    except Exception as e:
        print("Error in turnoff API:", e)
        return jsonify({'response': 'Error'}), 500
    

@app.route('/autobrightnessEnable/api/', methods=['POST'])
def autobrightnessEnable():
    try:
        mqttc.publish(topic, "Autobrightness:Enable")
        print("Turned AutobrightnessEnable")
        return jsonify({'response': 'Turned autobrightnessEnable successfully'})
    except Exception as e:
        print("Error in turnoff API:", e)
        return jsonify({'response': 'Error'}), 500


@app.route('/autobrightnessDisable/api/', methods=['POST'])
def autobrightnessDisable():
    try:
        mqttc.publish(topic, "Autobrightness:Disable")
        print("Turned AutobrightnessDisable")
        return jsonify({'response': 'Turned autobrightnessDisable successfully'})
    except Exception as e:
        print("Error in turnoff API:", e)
        return jsonify({'response': 'Error'}), 500


@app.route('/schedule', methods=['POST'])
def schedule():
    SrNo = request.form.get('SrNo')
    ScheduleStartTime = request.form.get('startTime')
    ScheduleEndTime = request.form.get('endTime')
    scheduling = request.form.get('scheduling')
    save_to_database(SrNo, ScheduleStartTime, ScheduleEndTime, scheduling)
    return redirect(url_for('index'))

def save_to_database(SrNo, ScheduleStartTime, ScheduleEndTime, scheduling):
    conn = sqlite3.connect('scheduling.db')
    cursor = conn.cursor()

    cursor.execute('INSERT INTO scheduling (SrNo, ScheduleStartTime, ScheduleEndTime, scheduling) VALUES (?, ?, ?, ?)', (SrNo, ScheduleStartTime, ScheduleEndTime, scheduling))
    
    conn.commit()
    conn.close()


# code for diffuser............
@app.route('/diffuseron/api/', methods=['POST'])
def diffuseron():
    try:
        mqttc.publish(topic_diffuser, "diffuser:100")
        return jsonify({'response': 'Turned ON successfully'})

    except Exception as e:
        print("Error in turnon API:", e)
        return jsonify({'response': 'Error'}), 500

@app.route('/diffuseroff/api/', methods=['POST'])
def diffuseroff():
    try:
        mqttc.publish(topic_diffuser, "diffuser:0")
        return jsonify({'response': 'Turned OFF successfully'})
    except Exception as e:
        print("Error in turnoff API:", e)
        return jsonify({'response': 'Error'}), 500

# ContinuousONOFF...as per minutes...
@app.route('/ContinuousONOFF', methods=['POST'])
def ContinuousONOFF():
    try:
        data = request.json
        ContinuousONOFF = data.get('ContinuousONOFF')
        # print('ContinuousONOFF:', ContinuousONOFF)
        mqttc.publish(topic_diffuser, "ContinuousONOFF:"+ ContinuousONOFF)
        return jsonify({'message': 'ContinuousONOFF published successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


# diffuser DiffuserEnable.......  
@app.route('/DiffuserEnable/api/', methods=['POST'])
def DiffuserEnable():
    try:
        mqttc.publish(topic_diffuser, "ContinuousONOFF:Enable")
        return jsonify({'response': 'Turned ContinuousON successfully'})
    except Exception as e:
        print("Error in turnoff API:", e)
        return jsonify({'response': 'Error'}), 500


@app.route('/DiffuserDisable/api/', methods=['POST'])
def DiffuserDisable():
    try:
        mqttc.publish(topic_diffuser, "ContinuousONOFF:Disable")
        return jsonify({'response': 'Turned ContinuousOFF successfully'})
    except Exception as e:
        print("Error in turnoff API:", e)
        return jsonify({'response': 'Error'}), 500



# Anjali Code......................
@app.route('/publish-color', methods=['POST'])
def handle_publish_color():
    try:
        color = request.json.get('color')
        color_publish = 'color:'+ color
        # print('color', color_publish)
        mqttc.publish(topic, color_publish)
        return jsonify({'message': 'Color published successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/update_intensity', methods=['POST'])
def update_intensity():
    try:
        data = request.get_json()
        led_intensity = data.get('ledIntensity')
        payload = 'ledIntensity:'+ str(led_intensity)
        print('led_intensity...........................', led_intensity)
        mqttc.publish(topic, payload)
        return jsonify({'success': True, 'message': 'Intensity updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    

if __name__ == "__main__":
    # app.run(host="0.0.0.0", port=2005)
    socketio.run(app, host='0.0.0.0', port=2005)

