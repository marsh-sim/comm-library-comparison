import argparse
from pymavlink import mavutil

parser = argparse.ArgumentParser('send_manual.py')
parser.add_argument('-p', '--port', type=int,
                    help='UDP port to listen on', default=24000)
args = parser.parse_args()

connection_string = f'udpin:127.0.0.1:{args.port}'
mav = mavutil.mavlink_connection(connection_string)
print(f'Listening on {connection_string}')

while True:
    msg = mav.recv_msg()
    if msg:
        print(msg)
