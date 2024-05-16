from flask import Flask, render_template
from flask_socketio import SocketIO
import paho.mqtt.client as mqtt

app = Flask(__name__)
socketio = SocketIO(app)

mqtt_broker = 'broker.emqx.io'
mqtt_port = 1883
mqtt_topic = "power_consumption"

cumulative_power = {}
total_power = 0

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(mqtt_topic)

def update_power_consumption(device_id, power):
    global total_power

    if device_id not in cumulative_power:
        cumulative_power[device_id] = 0
    cumulative_power[device_id] += power

    # Update total power consumption
    total_power += power

    avg = total_power / 360  # Calculate average power consumption across all devices
    avg_kwh = avg / 1000

    print("Total Average Power Consumption for all devices:", avg_kwh, "kWh")

    # Emit the updated total power consumption
    emit_total_power_consumption()

def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    data = str(msg.payload.decode('utf-8'))
    split_data = data[1:-1].split(":")
    device_id = split_data[1]
    power = int(split_data[3])

    try:
        update_power_consumption(device_id, power)
    except KeyError:
        print("Received message is not in the expected format.")

def emit_total_power_consumption():
    total_kwh = f"{(total_power / 360 / 1000)} kWh"  # Convert to kWh
    socketio.emit('update_total_kwh', {'total_kwh': total_kwh}, namespace='/')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_broker, mqtt_port, 60)
client.loop_start()

@app.route('/')
def test():
    return render_template('pract.html', total_kwh="0 kWh")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5005, debug=True)
