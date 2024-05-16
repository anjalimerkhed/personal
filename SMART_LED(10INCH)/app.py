from flask import Flask, render_template, request, jsonify
import paho.mqtt.client as mqtt

app = Flask(__name__)

mqtt_broker = "107.180.94.60"
mqtt_port = 18889
mqtt_topic = "ledAAAAAC/control"

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code "+str(rc))

client = mqtt.Client()
client.on_connect = on_connect
client.connect(mqtt_broker, mqtt_port)

@app.route('/update_intensity', methods=['POST'])
def update_intensity():
    try:
        data = request.get_json()
        led_intensity = data.get('ledIntensity')
        topic = 'ledIntensity:'+ led_intensity
        print('topic', topic)
        client.publish(mqtt_topic, topic)
        return jsonify({'success': True, 'message': 'Intensity updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    
@app.route('/')
def test():
	return render_template('index.html')


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5002, debug=True)
