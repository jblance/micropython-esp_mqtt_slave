# This file is executed on every boot (including wake-boot from deepsleep)
import network
import time
import ujson

# import webrepl

# Read in config file for settings
f = open("boot.cfg")
config = ujson.load(f)
f.close()

# Read network settings
SSID = config["SSID"]
WIFI_PASSWORD = config["WIFI_PASSWORD"]
# Obscure password in output
config["WIFI_PASSWORD"] = "********"
print("boot.py: Loaded Config: %s" % (config))


wlan = network.WLAN(network.STA_IF)
print("Connecting to network...")
wlan.active(True)
for _ in range(10):
    wlan.connect(SSID, WIFI_PASSWORD)
    time.sleep(1)
    if wlan.isconnected():
        print("Connected.")
        print("Network config:", wlan.ifconfig())
        break
    time.sleep(5)
else:
    print("Wifi connection failed")

# webrepl.start()
