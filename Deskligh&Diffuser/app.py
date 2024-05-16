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
topic = "desklightAAAAA6/control"
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

led_state = {}
 
def on_message(client, userdata, message):
    try:
        payload = message.payload.decode()
        split_payload = payload.split(":")
        if len(split_payload) >= 3:
            led = split_payload[2]
            # print(f"Received ledInt: {led}")
            color = split_payload[3]
            # print(f"Received led: {color}")
            led_state['color'] = color
            led_state['intensity'] = led
            socketio.emit('desklight',led_state)
        else:
            print("Data not received...")
    except Exception as e:
        print(f"Error processing message: {e}")



mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_message = on_message

def mqtt_connect():
    try:
        print("Connecting to MQTT broker...")
        mqttc.connect(broker, port)
        mqttc.loop_start()
        mqttc.subscribe("desklightAAAAA6/status")
    except Exception as e:
        print(f"Error connecting to MQTT broker: {e}")

mqtt_connect_thread = threading.Thread(target=mqtt_connect)
mqtt_connect_thread.start()

# def publish_200():
#     while True:
#         mqttc.publish(topic, "200")
#         print("Published 200 on topic")
#         time.sleep(10)  

# publish_thread = threading.Thread(target=publish_200)
# publish_thread.start()

# Nikkys code ...........
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/turnon/api/', methods=['POST'])
def turnon():
    try:
        mqttc.publish(topic, "Light:100")
        print("publish....on")

        conn = sqlite3.connect('scheduling.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE scheduling SET scheduling = 1")
        conn.commit()
        conn.close()

        return jsonify({'response': 'Turned ON successfully'})

    except Exception as e:
        print("Error in turnon API:", e)
        return jsonify({'response': 'Error'}), 500

@app.route('/turnoff/api/', methods=['POST'])
def turnoff_api():
    try:
        mqttc.publish(topic, "Light:0")
        print("publish....off")

        conn = sqlite3.connect('scheduling.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE scheduling SET scheduling = 1")
        conn.commit()
        conn.close()

        return jsonify({'response': 'Turned OFF successfully'})
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

# Anjali Code
@app.route('/publish-color', methods=['POST'])
def handle_publish_color():
    try:
        color = request.json.get('color')
        color_publish = 'color:'+ color
        print('color', color_publish)
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
        print('topic', payload)
        mqttc.publish(topic, payload)
        return jsonify({'success': True, 'message': 'Intensity updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == "__main__":
      socketio.run(app, host='0.0.0.0', port=2005)
