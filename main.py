from picamera import PiCamera, Color
from time import sleep
from datetime import datetime

import RPi.GPIO as GPIO
import numpy as np

import os


class Photobooth:
    def __init__(self):
	self.picture_count = 1
	self.event_name = "bryllup"

	self.base_path  = "/home/pi/photobooth/google-photos-uploader/" + self.event_name
	self.assert_path_exist()	
	self.width = 1280
	self.height = 720

        self.flash_overlay = np.zeros((self.width, self.height, 3), dtype=np.uint8)
	self.flash_overlay[:, :, :] = 0xff
	self.flash_overlay[:, :, :] = 0xff	
		
	self.camera = PiCamera()

	# xdpyinfo  | grep 'dimensions:'
	# https://picamera.readthedocs.io/en/release-1.10/fov.html
	self.camera.resolution = (self.width, self.height)
	self.camera.framerate = 15
	self.camera.image_effect = 'denoise'
	self.camera.brightness = 50
		
		
	# TODO: consider using board for wider Pi support
	# https://raspberrypi.stackexchange.com/questions/12966/what-is-the-difference-between-board-and-bcm-for-gpio-pin-numbering
	GPIO.setmode(GPIO.BCM)
	GPIO.setwarnings(False)
	GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def start(self):
	preview = self.camera.start_preview()
	while True:
		self.start_button_listener()
		#sleep(10)
		for i in range(self.picture_count):
			photobooth.start_countdown()
			photobooth.capture()
	self.stop()
    
    def stop(self):
	self.camera.stop_preview()
	self.camera.close()
		
	
    def capture(self):
	dt = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
	filename = self.base_path + "/" + self.event_name + "-" + dt + ".jpg"
	
	o = self.camera.add_overlay(np.getbuffer(self.flash_overlay), layer=3, alpha=200)
	sleep(.1)
	self.camera.remove_overlay(o)
	self.camera.capture(filename)
	

    def start_button_listener(self):
	while True:
		# wait until button is pressed
		if GPIO.input(15) == GPIO.HIGH:
			return
		
    def start_countdown(self):
	sleep(1)
	
	# red light
	GPIO.setup(17,GPIO.OUT)
	GPIO.output(17,GPIO.HIGH)
	sleep(1)
	GPIO.output(17,GPIO.LOW)
	
	# yellow ligth
	GPIO.setup(18,GPIO.OUT)
	GPIO.output(18,GPIO.HIGH)
	sleep(1)
	GPIO.output(18,GPIO.LOW)
	
	# green light
	GPIO.setup(27,GPIO.OUT)
	GPIO.output(27,GPIO.HIGH)
	sleep(1)
	GPIO.output(27,GPIO.LOW)
	
    def assert_path_exist(self):
           assert (os.path.exists(self.base_path) is True), "path does not exist: " + self.base_path

if __name__ == "__main__":
    photobooth = Photobooth()
    photobooth.start()

"""
TODO

- Fullscreen - need the actual screen
- Mutliple pictures - DONE 
- Visual feedback - DONE
- Make sure you can`t start multiple sessions at once - DONE
- Upload somewhere
- Display images on secondary screen

Nice to have 
- QR register
"""


