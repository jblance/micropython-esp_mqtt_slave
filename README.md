# Building a ESP32 Slave #
document is for use on Ubuntu

## Some pre-reqs / needed tools ##
* make sure user is in dialout group `sudo usermod -a -G dialout <userid>`
* logout / login again
* Install esptool `sudo pip install esptool`
* Install mpfshell `sudo pip install mpfshell`

## Erase the esp ##
`esptool.py --port /dev/ttyUSB0 erase_flash`

## Flash Micropython ##
* Download correct micropython image from https://micropython.org/download/esp32/
* Flash to esp `esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 esp32spiram-idf3-20200902-v1.13.bin`

## Connect to esp ##
* Note: replace ttyUSB0 with the port that the ESP is connected to
* Using mpfshell `mpfshell -c 'open ttyUSB0'`

## Install modules ##
* Connect using mpfshell `mpfshell -c 'open ttyUSB0'`
* Go to repl mode `repl`
* Install MQTT module
```
>>> import upip
>>> upip.install("micropython-umqtt.simple2")
```

## Put files on to esp ##
* Download files to local directory
* Edit config.txt to your details
* Connect using mpfshell `mpfshell -c 'open ttyUSB0'`
* `put boot.py`
* `put main.py`
* `put config.txt`
* Go to repl mode `repl`
* Reset ESP `Control-D`

```
MicroPython v1.13 on 2020-09-02; ESP32 module (spiram) with ESP32
Type "help()" for more information.
>>>
MPY: soft reboot
Network config: ('192.168.1.86', '255.255.255.0', '192.168.1.1', '192.168.1.1')
Loaded config: {'SERVER': 'mqttbroker', 'UART_NO': 2, 'CLIENT_ID': 'ESP32-Sensor', 'BAUDRATE': 2400}
Connected to mqttbroker, subscribed to ESP32-Sensor/command topic
```
