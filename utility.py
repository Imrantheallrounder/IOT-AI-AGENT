import paho.mqtt.client as mqtt

class utility:
    def get_topic_msg(response):
        floor = response.get('floor', None)
        space = response.get('space', None)
        appliance = response.get('appliance', None)
        state = response.get('state', None)
        if not floor:
            floor = 1
        topic = f"{floor}/{space}"
        message = {appliance:state}
        return topic, message

    def publish_message(topic, msg):
        BROKER_IP="localhost"
        MQTT_PORT=1883
        mqtt_client = mqtt.Client()
        mqtt_client.connect(BROKER_IP, MQTT_PORT, 60)
        mqtt_client.publish(topic, msg)
        mqtt_client.disconnect()
        print(f"Sent msg: {msg} | on topic: {topic}")