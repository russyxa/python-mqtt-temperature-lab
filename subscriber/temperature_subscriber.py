import os 
import json
import paho.mqtt.client as mqtt

MQTT_BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "mqtt-broker")
MQTT_BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT", "1883"))
CLIENT_ID = "PythonTemperatureSubscriber"
#SUBSCRIBE_TOPIC = "pittsburgh/temperature/#"
SUBSCRIBE_TOPIC = "pittsburgh/temperature/hotTemps" 
QOS = 2

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to MQTT broker at {MQTT_BROKER_HOST}:{MQTT_BROKER_PORT}")
        print(f"Subscribing to topic: {SUBSCRIBE_TOPIC}")
        client.subscribe(SUBSCRIBE_TOPIC, qos=QOS)
    else: 
        print(f"Failed to connect. Return code: {rc}")

def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode("utf-8")

    try:
        data = json.loads(payload)
        temperature = data.get("temperature")
        unit = data.get("unit")
        category = data.get("category")
        timestamp = data.get("timestamp")
        print(f"Received from {topic}: {temperature}°{unit} ({category}) at {timestamp}")
    except json.JSONDecodeError:
        print(f"Received from {topic}: {payload} (not valid JSON)")
    #print(f"Received from {topic}: {payload}")

def main():
    client = mqtt.Client(client_id=CLIENT_ID)
    client.on_connect = on_connect
    client.on_message = on_message
    print(f"Connecting to MQTT broker at {MQTT_BROKER_HOST}:{MQTT_BROKER_PORT}...")
    client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, keepalive=60)
    client.loop_forever()

if __name__ == "__main__":
    main()