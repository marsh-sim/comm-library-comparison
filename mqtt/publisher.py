import paho.mqtt.client as mqtt

broker_address = 'localhost'

client = mqtt.Client('Publisher')
client.connect(broker_address)
client.publish('area/data', 'hello')