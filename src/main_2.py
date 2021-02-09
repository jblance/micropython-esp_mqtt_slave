import ujson

from machine import UART
from time import sleep

# Read in config file for settings
f = open("config.txt")
config = ujson.load(f)
f.close()
# Obscure password in output
_config = config
_config["WIFI_PASSWORD"] = "********"

print("main_2.py: Loaded config: %s" % (_config))
server = config["SERVER"]
client_id = config["CLIENT_ID"]
uart_no = config["UART_NO"]
baudrate = config["BAUDRATE"]
u = UART(uart_no, baudrate)
print(u)

while True:

    # u.init(baudrate=baudrate, timeout=2000)
    # sleep(0.5)  # give serial port time to receive the data
    response = u.read()
    result = (
        b"(230.0 50.0 0030 42.0 54.0 56.4 46.0 60 0 0 2 0 0 0 0 0 1 1 0 0 1 0 54.0 0 1 000\x9E\x60\r"
    )
    # response = u.read()  # read all available bytes
    if response:
        print("response was: %s" % (response))
        print("sending %s" % (result))
        u.write(result)
    # sleep(1)
