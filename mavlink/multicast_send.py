import argparse
from itertools import count
from pymavlink import mavutil
import pymavlink.dialects.v20.common as mavlink
from time import sleep

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', type=int,
                    help='UDP port to send on', default=24400)
args = parser.parse_args()

connection_string = f'mcast:239.255.145.50:{args.port}'
mav = mavutil.mavlink_connection(connection_string)
print(f'Sending to {connection_string}')

for i in count():
    mav.param_set_send('WP_RADIUS', 100 + i, mavlink.MAV_PARAM_TYPE_REAL32)
    print(f'sent {i}')
    sleep(1.0)
