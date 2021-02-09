import ujson

from machine import UART
from time import sleep
from umqtt.simple import MQTTClient


def run_command(command, full_command):
    results = {}
    results["command"] = command
    # results["full_command"] = full_command
    print("Using UART %s with baudrate %s" % (uart_no, baudrate))
    u = UART(uart_no, baudrate)
    u.init(baudrate=baudrate, timeout=2000)
    _write = u.write(full_command)
    print("write result %s" % _write)
    # sleep(0.5)  # give serial port time to receive the data
    response = u.read()
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
        # _msg = ujson.loads(msg)
        # print(_msg)
        # command = _msg["command"]
        command = "test"
        full_command = msg
        print("Executing command %s" % (full_command))
        #
        result = run_command(command, full_command)
        print("Got result %s" % (result))
        #
        print("Publishing result to %s" % (result_topic))
        print(mqtt_client)
        mqtt_client.publish(result_topic, result)


def connect():
    c = MQTTClient(client_id, mqtt_broker)
    c.set_callback(sub_cb)
    c.connect()
    c.subscribe(command_topic)
    print("Connected to %s, subscribed to %s topic" % (mqtt_broker, command_topic))
    return c


# Read in config file for settings
f = open("main.cfg")
config = ujson.load(f)
f.close()

print("main.py: Loaded Config: %s" % (config))
# Read main settings
mqtt_broker = config["MQTT_BROKER"]
client_id = config["CLIENT_ID"]
uart_no = config["UART_NO"]
baudrate = config["BAUDRATE"]

command_topic = "%s/command" % (client_id)
result_topic = "%s/result" % (client_id)

mqtt_client = connect()

try:
    while True:
        # micropython.mem_info()
        mqtt_client.check_msg()
        sleep(1)
except Exception as e:
    print("Error", e)
finally:
    mqtt_client.disconnect()
