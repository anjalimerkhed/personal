from flask import Flask, render_template, request, jsonify
import paho.mqtt.client as mqtt

app = Flask(__name__)

# Dictionary to store received MQTT data for each ID
mqtt_data = {}

mqtt_broker = 'broker.emqx.io'
mqtt_port = 1883
mqtt_topic = "dust_particle_data" 

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(mqtt_topic)


def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    data = str(msg.payload.decode('utf-8'))
    data = eval(msg.payload.decode('utf-8'))
    particle_id = data['id']
    mqtt_data[particle_id] = data
    # print('............',data)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(mqtt_broker, mqtt_port, 60)

client.loop_start()
    

@app.route('/')
def test():
	return render_template('index.html')

# Route to provide MQTT data as JSON
@app.route('/dust_particles', methods=['GET'])
def get_dust_particles():
    # print('aaaaaaaaaaaaa',mqtt_data)
    return jsonify(mqtt_data)



if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True)