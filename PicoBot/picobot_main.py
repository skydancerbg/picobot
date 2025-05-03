#import sys
#sys.path.append('/PicoBot')

'''
Wih onboard LED ON on Wi-Fi connection
Use https://jsfiddle.net/ to create the WEB page
'''
import network
import socket
from time import sleep
import machine
#from secrets import secrets
import ubinascii
from picobot import PicoBot
import rp2


# Define led object and set LED pin to OUT
led = machine.Pin('LED', machine.Pin.OUT)
led.off()

# Create robot object
robot = PicoBot()

# Set country to avoid possible errors
rp2.country('BG')


##ssid = 'smart_home'
##password = 'Stem123*'
# Load login data from different file for safety reasons
#ssid = secrets['ssid']
#password = secrets['pw']
ssid = 'picobottest'
password = '12345678'

# Got IP 10.11.12.242

def move_left_forward():
    print ("Left Forward")
    robot.moveLeftForward()
    
def move_forward():
    print ("Forward")
    robot.goForward()
        
def move_right_forward():
    print ("Right Forward")
    robot.moveRightForward()
    
def move_left():
    print ("Left")
    robot.moveLeft()
    
def stop():
    print ("Stop")
    robot.hardStop()
    
def move_right():
    print ("Right")
    robot.moveRight()
    
def move_left_backward():
    print ("Left Backward")
    robot.moveLeftBackward()
    
def move_backward():
    print ("Backward")
    robot.goBackwad()
    
def move_right_backward():
    print ("Right Backward")
    robot.moveRightBackward()
    
def rotate_left():
    print ("Rotate Left")
    robot.rotateLeft()
    
def rotate_right():
    print ("Rotate right")
    robot.rotateRight()


def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    # If you need to disable powersaving mode
    # wlan.config(pm = 0xa11140)

    # Print the MAC address in the wireless chip OTP
    mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
    print('mac = ' + mac)
    # Other things to query
    # print(wlan.config('channel'))
    # print(wlan.config('essid'))
    # print(wlan.config('txpower'))
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    # Turn onboard LED ON when Wi-Fi is connected
    led.on()
    print(f'Connected on {ip}')
    return ip

def create_WiFi_AP():
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=ssid, password=password) 
    ap.active(True)

    while ap.active == False:
        pass
    print("Access point active")
    print(ap.ifconfig())
    led.on()
    return '192.168.4.1'

def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    # from https://forum.micropython.org/viewtopic.php?f=18&t=10412 
    ## Add this line to resolve WiFi issue ???
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ##
    connection.bind(address)
    connection.listen(1)
    return connection

# Function to load in html page    
def get_html(html_name):
    with open("/PicoBot/" + html_name, 'r') as file:
        html = file.read()
        
    return html

def webpage():
#    #Template HTML
#    html = f"""
#            <!DOCTYPE html>
#            <html>
#            <head>
#            <title>Pico Robot Control</title>
#            </head>
#            <center><b>
#            <form action="./forward">
#            <input type="submit" value="Forward" style="height:120px; width:120px" />
#            </form>
#            <table><tr>
#            <td><form action="./left">
#            <input type="submit" value="Left" style="height:120px; width:120px" />
#            </form></td>
#            <td><form action="./stop">
#            <input type="submit" value="Stop" style="height:120px; width:120px" />
#            </form></td>
#            <td><form action="./right">
#            <input type="submit" value="Right" style="height:120px; width:120px" />
#            </form></td>
#            </tr></table>
#            <form action="./back">
#            <input type="submit" value="Back" style="height:120px; width:120px" />
#            </form>
#            </body>
#            </html>
#            """
#    return str(html)
    
    # Return HTML from file
    return str(get_html('index.html'))

def serve(connection):
    #Start web server
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        #print(request)
        #print('##########################################################################################')
        try:
            request = request.split()[1]
        except IndexError:
            pass
 
        
        # Пример за обработка на заявката
        print("Received request:", request)  # За отстраняване на грешки

        # Обработка на стойностите за слайдера и числовото поле
        if 'servo_base_slider' in request:
            slider_angle = int(request.split('servo_base_slider=')[1].split('&')[0])
            print(f"Base slider set to {slider_angle}")
            if slider_angle<0:
                slider_angle=0
            if slider_angle>180:
                slider_angle=180
            robot.arm.smooth_move_servo(0, slider_angle)  # Канал 0 за серво "основа"

        if 'servo_base_value' in request:
            number_angle = int(request.split('servo_base_value=')[1].split('&')[0])
            if number_angle<0:
                number_angle=0
            if number_angle>180:
                number_angle=180
            print(f"Base value set to {number_angle}")
            robot.arm.smooth_move_servo(0, number_angle)  # Канал 0 за серво "основа"

        if 'servo_arm_slider' in request:
            slider_angle = int(request.split('servo_arm_slider=')[1].split('&')[0])  
            if slider_angle<40:
                slider_angle=40
            if slider_angle>140:
                slider_angle=140
            print(f"Arm slider set to {slider_angle}")
            robot.arm.smooth_move_servo(1, slider_angle)  # Канал 1 за серво "ръка"

        if 'servo_arm_value' in request:
            number_angle = int(request.split('servo_arm_value=')[1].split('&')[0])
            if number_angle<40:
                number_angle=40
            if number_angle>140:
                number_angle=140
            print(f"Arm value set to {number_angle}")
            robot.arm.smooth_move_servo(1, number_angle)  # Канал 1 за серво "ръка"

        if 'servo_claw_slider' in request:
            slider_angle = int(request.split('servo_claw_slider=')[1].split('&')[0])
            if slider_angle<40:
                slider_angle=40
            if slider_angle>140:
                slider_angle=140
            print(f"Claw slider set to {slider_angle}")
            robot.arm.smooth_move_servo(2, slider_angle)  # Канал 2 за серво "щипка"

        if 'servo_claw_value' in request:
            number_angle = int(request.split('servo_claw_value=')[1].split('&')[0])
            if number_angle<40:
                number_angle=40
            if number_angle>140:
                number_angle=140
            print(f"Claw value set to {number_angle}")
            robot.arm.smooth_move_servo(2, number_angle)  # Канал 2 за серво "щипка"


        if request == '/reset_to_default?':
            robot.arm.reset_servos()  # Ресет на всички сервомотори
            print("Reset to default.")

                
        
        if request == '/left_forward?':
            move_left_forward()        
        elif request == '/forward?':
            move_forward()
        elif request == '/right_forward?':
            move_right_forward() 
        elif request =='/left?':
            move_left()
        elif request =='/stop?':
            stop()
        elif request =='/right?':
            move_right()
        elif request =='/left_back?':
            move_left_backward()
        elif request =='/back?':
            move_backward()
        elif request =='/right_back?':
            move_right_backward()
        elif request =='/rotate_left?':
            rotate_left()
        elif request =='/rotate_right?':
            rotate_right()

        html = webpage()
        client.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        client.send(html)
        client.close()


try:
    # For STA mode
    #ip = connect()
    # For AP mode
    ip = create_WiFi_AP()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()

