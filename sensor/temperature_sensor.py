import os 
import random
import time
from datetime import datetime

import paho.mqtt.client as mqtt

TOPIC_TEMP_COLD = "pittsburgh/temperature/coldTemps"
TOPIC_TEMP_NICE = "pittsburgh/temperature/niceTemps"
TOPIC_TEMP_HOT = "pittsburgh/temperature/hotTemps"

MQTT_BROKER_HOST = os.getenv("MQTT_BROKER_HOST", "mqtt-broker")
MQTT_BROKER_PORT = int(os.getenv("MQTT_BROKER_PORT", "1883"))
CLIENT_ID = "PythonTemperatureSensor"
QOS = 2

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def classify_temperature(temperature):
    if temperature <= 45:
        return TOPIC_TEMP_COLD
    elif temperature <= 80:
        return TOPIC_TEMP_NICE
    else: 
        return TOPIC_TEMP_HOT
    
def main():
    client = mqtt.Client(client_id=CLIENT_ID)
    print(f"Connecting to MQTT broker at {MQTT_BROKER_HOST}:{MQTT_BROKER_PORT}...")
    client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, keepalive=60)
    print("Connected to MQTT broker.")
    client.loop_start()

    try:
        while True:
            temperature = random.randint(0,100)
            topic = classify_temperature(temperature)
            message = f"{temperature} degrees - {get_timestamp()}"
            result = client.publish(topic, message, qos=QOS)
            result.wait_for_publish()
            print(f"Published to {topic}: {message}")
            time.sleep(5)
    except KeyboardInterrupt: 
        print("Stopping temperature sensor...")
    finally:
        client.loop_stop()
        client.disconnect()
        print("Disconnected from MQTT broker.")

if __name__ == "__main__":
    main()