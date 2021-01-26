# This file is executed on every boot (including wake-boot from deepsleep)
import ujson
import network
import webrepl

# Read in config file for settings
f = open("config.txt")
config = ujson.load(f)
f.close()
# Obscure password in output
_config = config
_config["WIFI_PASSWORD"] = "********"

print("boot.py: Loaded config: %s" % (_config))

SSID = config["SSID"]
WIFI_PASSWORD = config["WIFI_PASSWORD"]

wlan = network.WLAN(network.STA_IF)
if not wlan.isconnected():
    print("Connecting to network...")
    wlan.active(True)
    wlan.connect(SSID, WIFI_PASSWORD)
    while not wlan.isconnected():
        pass
print("Network config:", wlan.ifconfig())

webrepl.start()
