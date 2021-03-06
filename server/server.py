from flask import Flask, render_template, send_from_directory, Response
import time
import serial
from ChooseSerialPort import choose_port, set_port
from DetectSerialPort import serial_ports
import socket
'''
#Find what serial porn the arduino is on
list_serial_ports = serial_ports()
print(type(list_serial_ports))
print(list_serial_ports)
if len(list_serial_ports) == 1:
    tmp_port = list_serial_ports[0]
    ser = serial.Serial(tmp_port, 9600, timeout=1)
else:
    print("There is more than one available serialport from the following serial ports")
    for i in range(len(list_serial_ports)):
        print('Choice [' + str(i) + '] is called ' + str(list_serial_ports[i]))
    serial_port_choice = int(input('Please make your choice : '))
    print('You chose port ' + str(list_serial_ports[serial_port_choice]))
    ser = serial.Serial(list_serial_ports[serial_port_choice], 9600, timeout=1)
'''
#Get the ip address of the device this is running
#Praise to the stack overflow gods are in order 
#https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib/166520#166520
ip_setup = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ip_setup.connect(("8.8.8.8", 80))
ip = ip_setup.getsockname()[0]
ip_setup.close()
print(ip)
#Praise have been given to the beloved ones who give detailed answers on stack overflow

#set defult direction and speed of robot of the robot
direction = 'stop'
speed = 0

def set_direction(tmp_direction):
    direction = tmp_direction

#Set the serial port, been getting errors about that
ser = serial.Serial(serial_ports()[0], 9600, timeout=1)

app = Flask(__name__, static_url_path='/js')  
@app.route('/')
def hello_world():
    return render_template('index.html', ip = ip, direction = direction, speed = speed, port = 5000)

@app.route('/get_serial_ports/')
def set_serial_port():
    return str(serial_ports())

@app.route('/forward')
def forward():
    global direction
    direction = 'forward'
    return direction

@app.route('/backward')
def backward():
    global direction
    direction = 'backward'
    return direction

@app.route('/left')
def left():
    global direction
    direction = 'left'
    return direction

@app.route('/right')
def right():
    global direction
    direction = 'right'
    return direction

@app.route('/stop')
def stop():
    global direction
    direction = 'stop'
    return direction

@app.route('/led_on')
def led_on():
   ser.write('O'.encode())
   return 'led_on'

@app.route('/led_off')
def led_off():
   ser.write('P'.encode())
   return 'led_off'

@app.route('/jquery.js')
def jquery():
     return render_template('./jquery.min.js')

@app.route('/robot_state')
def robot_state():
    print(direction)
    return "The robot is going " + str(direction) + "At a speed of " + str(speed)
 
if __name__ == '__main__':
    #app.debug = True
    app.run(host= '0.0.0.0')
