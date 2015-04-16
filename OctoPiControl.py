import socket
import time
import Adafruit_SSD1306
from Adafruit_LED_Backpack import AlphaNum4
import Image
import ImageDraw
import ImageFont
import os
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

import requests
import json

#Constants
#octopi
#apiurl = "http://192.168.1.191:5000/api"
#apikey = "D3C09432B9B14506B00DDE3392814D68"

#x60
apiurl = "http://192.168.1.200:5000/api"
apikey = "2AE19BC0BE0C4E7296B03325DF2C4489"

#Raspberry pi pin configurations
#Oled display:
RST = 4

#CONFIGURE INPUTS
UP_BUTTON = 17
HOME_BUTTON = 18
DOWN_BUTTON = 27
CONNECT_BUTTON = 22  

INPUT_X_AXIS = 23
INPUT_Y_AXIS = 24
INPUT_Z_AXIS = 25
INPUT_E = 5

INPUT_SCALE_1 = 6
INPUT_SCALE_2 = 12
INPUT_SCALE_3 = 13
INPUT_SCALE_4 = 16

#Configure LED outputs
UP_LED = 19
HOME_LED = 20
DOWN_LED = 21
CONNECT_LED = 7 #CE1 pin


GPIO.setup(UP_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(HOME_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(DOWN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(CONNECT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(INPUT_X_AXIS, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(INPUT_Y_AXIS, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(INPUT_Z_AXIS, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(INPUT_E, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.setup(INPUT_SCALE_1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(INPUT_SCALE_2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(INPUT_SCALE_3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(INPUT_SCALE_4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#add hot end heater switch?

GPIO.setup(UP_LED, GPIO.OUT)
GPIO.setup(HOME_LED, GPIO.OUT)
GPIO.setup(DOWN_LED, GPIO.OUT)
GPIO.setup(CONNECT_LED, GPIO.OUT)

#=====OLED display configuration

#128x64 display with hardware I2C
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=0x3D)

#Initialise library
disp.begin()

#Clear display
disp.clear()
disp.display()

#Create blank image for drawing
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

#Get drawing object to draw on image
draw = ImageDraw.Draw(image)
draw.rectangle((0,0,width,height), outline=0, fill=0)

#load default font
#font = ImageFont.load_default()

font = ImageFont.truetype('Minecraftia-Regular.ttf',8)

#=====AlphaNumeric Display setup
ANDisplay = AlphaNum4.AlphaNum4()

ANDisplay.begin()
ANDisplay.clear()

#=====Button functions
def ReadScale():
	global SelectedAxis
	if GPIO.input(INPUT_SCALE_1):
		SelectedScale = 0.1
	elif GPIO.input(INPUT_SCALE_2):
		SelectedScale = 1
	elif GPIO.input(INPUT_SCALE_3):
		SelectedScale = 10
	elif GPIO.input(INPUT_SCALE_4)
		SelectedScale = 100
	else:
		SelectedScale = 1

def ReadAxis():
	global SelectedScale
	if GPIO.input(INPUT_X_AXIS):
		SelectedAxis = 'x'
		GPIO.output(HOME_LED, 1)
	elif GPIO.input(INPUT_Y_AXIS):
		SelectedAxis = 'y'
		GPIO.output(HOME_LED, 1)
	elif GPIO.input(INPUT_Z_AXIS):
		SelectedAxis = 'z'
		GPIO.output(HOME_LED, 1)
	else:
		SelectedAxis = 'e'
		GPIO.output(HOME_LED, 0)

def HomeButtonCallback(channel):
	ReadAxis()
	uri = apiurl + "/printer/printhead"
	if SelectedAxis = 'e'
		return
	else:
		body = { 'command': 'home', 'axes': SelectedAxis }
	r = requests.post(uri, headers=headers, data=json.dumps(body))

def UpButtonCallback(channel):
	ReadAxis()
	ReadScale()
	body = { 'command': 'jog', 'X-Api-Key': apikey }
	uri = apiurl + "/printer/printhead"
	if SelectedAxis = 'e':
		body = { 'command': 'extrude', 'amount' : SelectedScale }
	else:
		body = { 'command': 'home', SelectedAxis : SelectedScale }
	r = requests.post(uri, headers=headers, data=json.dumps(body))

def DownButtonCallback(channel):
	ReadAxis()
	ReadScale()
	body = { 'command': 'jog', 'X-Api-Key': apikey }
	uri = apiurl + "/printer/printhead"
	if SelectedAxis = 'e':
		body = { 'command': 'extrude', 'amount' : -SelectedScale }
	else:
		body = { 'command': 'home', SelectedAxis : -SelectedScale }
	r = requests.post(uri, headers=headers, data=json.dumps(body))

def ConnectButtonCallback(channel):
	#===update this with correct API call for toggling connection state
	#===add long press for system shutdown?
	uri = apiurl + "/printer/printhead"
	body = { 'command': 'home', 'axes': SelectedAxis }
	r = requests.post(uri, headers=headers, data=json.dumps(body))

def CheckConnectionStatus():
	if PrinterStatus <> "Connected":
		GPIO.output(CONNECT_LED,0)
	else:
		GPIO.output(CONNECT_LED,1)

#=====LED output
GPIO.output(HOME_LED, 1)
GPIO.output(UP_LED, 1)
GPIO.output(DOWN_LED, 1)

GPIO.add_event_detect(HOME_BUTTON, GPIO.RISING, callback=HomeButtonCallback, bouncetime=300)
GPIO.add_event_detect(UP_BUTTON, GPIO.RISING, callback=UpButtonCallback, bouncetime=300)
GPIO.add_event_detect(DOWN_BUTTON, GPIO.RISING, callback=DownButtonCallback, bouncetime=300)

loopTime = time.time()

while 1:

	if time.time() - loopTime > 1:

		#get printer status for OLED display
		uri = apiurl + "/state"
		headers = { 'Content-type': 'application/json', 'X-Api-Key': apikey }
		r = requests.get(uri, headers=headers)
		j = r.json()

		PrinterStatus = str(j['state']['stateString'])
		BedTempActual = str(j['temperatures']['bed']['actual'])
 		BedTempTarget = str(j['temperatures']['bed']['target'])
 		HotEndTempActual = str(j['temperatures']['tool0']['actual'])
 		HotEndTempTarget = str(j['temperatures']['tool0']['target'])
 		#===add job progress here?

 		image = Image.new('1', (width,height))
		draw=ImageDraw.Draw(image)
		
		draw.text((1,1), 'Printer State: ' + PrinterStatus, font=font, fill=255)
		draw.text((1,11), 'Hot End Temp: ' + HotEndTempActual +"/"+HotEndTempTarget, font=font, fill=255)
		draw.text((1,21), 'Bed Temp: ' + BedTempActual +"/"+BedTempTarget, font=font, fill=255)
		#IP_Address = [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
		#draw.text((2,22), IP_Address, font=font, fill=255)
		
		disp.image(image)
		disp.display()
		
		ReadAxis()
		ReadScale()

		#Alphanumeric display
		ANDisplay.print_str(SelectedAxis.upper()+SelectedScale.rjust(3," "))
		ANDisplay.write_display()
		
		loopTime = time.time()

GPIO.cleanup()