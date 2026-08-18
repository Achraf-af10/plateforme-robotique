import xmlrpc.client
import time

GRIPPER_IP = "10.120.0.11"
PORT = 41414

def pince_open(width=5.0, force=80, speed=100):
    proxy = xmlrpc.client.ServerProxy(
        "http://10.120.0.11:41414/",
        allow_none=True
    )
    proxy.twofg_grip_external(0, float(width), force, speed)
    time.sleep(1.5)

def pince_close(width=0.0, force=80, speed=100):
    proxy = xmlrpc.client.ServerProxy(
        "http://10.120.0.11:41414/",
        allow_none=True
    )
    proxy.twofg_grip_external(0, float(width), force, speed)
    time.sleep(1.5)
