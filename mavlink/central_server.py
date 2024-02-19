import argparse
from dataclasses import dataclass
from io import BytesIO
from pymavlink import mavutil
import pymavlink.dialects.v20.common as mavlink
import socket
from time import time
from typing import Dict, Tuple

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', type=int,
                    help='UDP port to listen on', default=24000)
args = parser.parse_args()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(0.1)
sock.bind(('0.0.0.0', args.port))


@dataclass
class Client:
    datafile: BytesIO
    mav: mavlink.MAVLink
    last_heartbeat_time: float


clients: Dict[Tuple[str, int], Client] = {}
next_broadcast = 0.0
broadcast_interval = 2.0

while True:
    try:
        data, address = sock.recvfrom(1024)
        if address not in clients:
            datafile = BytesIO()
            clients[address] = Client(
                datafile, mavlink.MAVLink(datafile), 0.0)
        try:
            messages = clients[address].mav.parse_buffer(data)
            if messages is not None:
                for msg in messages:
                    print(address[1], msg)
        except Exception as e:
            print(e)
    except KeyboardInterrupt:
        break
    except Exception:
        pass

    if time() >= next_broadcast:
        for address in clients:
            mav = clients[address].mav
            msg = mav.param_set_encode(
                7, 1, b'WP_RADIUS', 200, mavlink.MAV_PARAM_TYPE_REAL32)
            msg.pack(mav)
            out_data = msg.get_msgbuf()
            sock.sendto(out_data, address)

        next_broadcast = time() + broadcast_interval
