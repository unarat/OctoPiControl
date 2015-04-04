import socket
import time
import Adafruit_SSD1306

import Image
import ImageDraw
import ImageFont

import RPi.GPIO as GPIO

#Raspberry pi pin configurations
RST = 24
BUTTON= 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
ButtonState = False

def my_callback(channel):
	global ButtonState
	ButtonState = not ButtonState
	print('button pressed, new state is ' + str(ButtonState))	

GPIO.add_event_detect(BUTTON, GPIO.RISING, callback=my_callback, bouncetime=300)

loopTime = time.time()
while 1:

	if time.time() - loopTime > 2:
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

	draw.text((2,2), 'Hello World!', font=font, fill=255)
	#IP_Address = [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
	#draw.text((2,22), IP_Address, font=font, fill=255)
	draw.text((2,22), 'Button is '+ str(ButtonState), font=font, fill=255)

	disp.image(image)
	disp.display()
	
	loopTime = time.time()
