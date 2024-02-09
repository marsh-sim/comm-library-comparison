import paho.mqtt.client as mqtt

broker_address = 'localhost'


def on_connect(client, userdata, flags, result_code):
    print(f'Connected, result code {result_code}')
    client.subscribe('area/data')


def on_message(client, userdata, msg):
    print(f'Received: {msg.payload}')


client = mqtt.Client()
client.connect(broker_address)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
