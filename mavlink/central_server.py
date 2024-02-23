import argparse
from dataclasses import dataclass
from io import BytesIO
from math import sin
from pymavlink import mavutil
import pymavlink.dialects.v20.common as mavlink
import socket
from time import time
from typing import Dict, Optional, Tuple

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', type=int,
                    help='UDP port to listen on', default=24400)
args = parser.parse_args()

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(0.001)
sock.bind(('0.0.0.0', args.port))

print(f'Server listening on port {args.port}')


@dataclass
class Client:
    datafile: BytesIO
    mav: mavlink.MAVLink
    last_heartbeat_time: Optional[float] = None
    system_id = 0
    component_id = 0


Address = Tuple[str, int]

clients: Dict[Address, Client] = {}
client_timeout = 5.0

next_controls = 0.0
controls_interval = 0.001

while True:
    try:
        data, address = sock.recvfrom(1024)
        if address not in clients:
            datafile = BytesIO()
            clients[address] = Client(
                datafile, mavlink.MAVLink(datafile))
        try:
            messages = clients[address].mav.parse_buffer(data)
            if messages is not None:
                for msg in messages:
                    if msg.get_msgId() == mavlink.MAVLINK_MSG_ID_HEARTBEAT:
                        if (clients[address]).last_heartbeat_time is None:
                            print('Connected {} on port {} in state {}'.format(
                                  mavlink.enums['MAV_COMPONENT'][msg.get_srcComponent(
                                  )].name,
                                  address[1],
                                  mavlink.enums['MAV_STATE'][msg.system_status].name))

                        clients[address].last_heartbeat_time = time()
                        clients[address].system_id = msg.get_srcSystem()
                        clients[address].component_id = msg.get_srcComponent()
                    else:
                        print(address[1], msg)

        except Exception as e:
            print(e)
    except KeyboardInterrupt:
        break
    except Exception:
        pass

    if time() >= next_controls:
        for address, client in clients.items():
            if client.component_id == mavlink.MAV_COMP_ID_USER2:
                msg = client.mav.manual_control_encode(
                    1,  # target system
                    int(1000 * sin(time())),  # pitch
                    int(1000 * sin(time() + 1)),  # roll
                    int(500 + 500 * sin(time() + 2)),  # throttle
                    int(1000 * sin(time() + 3)),  # yaw
                    0,  # buttons
                )
                msg.pack(client.mav)
                sock.sendto(msg.get_msgbuf(), address)

    timeout_time = time() - client_timeout
    addresses_to_remove = []
    for address, client in clients.items():
        if client.last_heartbeat_time is not None and client.last_heartbeat_time < timeout_time:
            print('Disconnected {} on port {}'.format(
                mavlink.enums['MAV_COMPONENT'][client.component_id].name, address[1]))
            # can't change dictionary size during iterating over it
            addresses_to_remove.append(address)
    for address in addresses_to_remove:
        del clients[address]
