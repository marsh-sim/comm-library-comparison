import argparse
from pymavlink import mavutil

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', type=int,
                    help='UDP port to listen on', default=24000)
args = parser.parse_args()

connection_string = f'mcast:239.255.145.50:{args.port}'
mav = mavutil.mavlink_connection(connection_string)
print(f'Listening on {connection_string}')

while True:
    msg = mav.recv_msg()
    if msg:
        print(msg)
