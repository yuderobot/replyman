import socket
import struct
from traceback import print_exc
DEST_PORT = 7

def send_magic_packet(addr):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        mac_ = addr.upper().replace("-", "").replace(":", "")
        if len(mac_) != 12:
            raise Exception("[Warn] MAC address format is invalid: {}".format(addr))
        buf_ = b'f' * 12 + (mac_ * 20).encode()
        magicp = b''
        for i in range(0, len(buf_), 2):
            magicp += struct.pack('B', int(buf_[i:i + 2], 16))
 
        print("[Info] Sent magic packet to host {}".format(addr))
        s.sendto(magicp, ('<broadcast>', DEST_PORT))

def issue_wol(host):
    if host == "zen":
        addr = "24:4b:fe:ce:9b:74"
        send_magic_packet(addr)
        return True
    else:
        return False