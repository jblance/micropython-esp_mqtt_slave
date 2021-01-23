import ujson

from machine import UART
from time import sleep
from umqtt.simple import MQTTClient


def run_command(command, full_command):
    results = {}
    results["command"] = command
    results["full_command"] = full_command
    u = UART(uart_no, baudrate)
    u.init(baudrate=baudrate, timeout=1000)
    u.write(full_command)
    sleep(0.5)  # give serial port time to receive the data
    response = u.readline()
    # response = u.read()  # read all available bytes
    print("response was: %s" % (response))
    results["result"] = response
    return ujson.dumps(results)


def sub_cb(*args, **kwargs):
    """
    MQTT Subscription Callback function
    - listens to topic for a command
    - runs the command
    - publishes the result to result_topic
    """
    if len(args) > 1:
        topic = args[0]
        msg = args[1]
        print("Got msg %s on topic: %s" % (msg, topic))
        _msg = ujson.loads(msg)
        print(_msg)
        command = _msg["command"]
        full_command = _msg["full_command"]
        print("Executing command %s" % (command))
        #
        result = run_command(command, full_command)
        print("Got result %s" % (result))
        #
        print("Publishing result to %s" % (result_topic))
        mqtt_client.publish(result_topic, result)


def connect():
    c = MQTTClient(client_id, server)
    c.set_callback(sub_cb)
    c.connect()
    c.subscribe(topic)
    print("Connected to %s, subscribed to %s topic" % (server, topic))
    return c


# Read in config file for settings
f = open("config.txt")
config = ujson.load(f)
f.close()
print("Loaded config: %s" % (config))
server = config["SERVER"]
client_id = config["CLIENT_ID"]
uart_no = config["UART_NO"]
baudrate = config["BAUDRATE"]

topic = "%s/command" % (client_id)
result_topic = "%s/result" % (client_id)

mqtt_client = connect()

try:
    while True:
        # micropython.mem_info()
        mqtt_client.check_msg()
        sleep(1)
finally:
    mqtt_client.disconnect()
