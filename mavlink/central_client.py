import argparse
from itertools import count
from pymavlink import mavutil
import pymavlink.dialects.v20.common as mavlink
import socket
from time import sleep, time

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', type=int,
                    help='UDP port to send to', default=24000)
args = parser.parse_args()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

connection_string = f'udpout:127.0.0.1:{args.port}'
mav: mavutil.mavfile = mavutil.mavlink_connection(connection_string)
print(f'Sending to {connection_string}')

next_send = 0.0
send_interval = 0.5

for i in count():
    if time() >= next_send:
        mav.param_set_send('WP_RADIUS', i, mavlink.MAV_PARAM_TYPE_REAL32)
        next_send = time() + send_interval
        print(f'sent {i}')

    message = mav.recv_msg()
    if message is not None:
        print('received', message)

    sleep(0.1)
