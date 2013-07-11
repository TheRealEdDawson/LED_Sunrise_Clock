#!/usr/bin/python

# A fully sick ghetto "Sunrise Alarm Clock Light" made with Raspberry Pi and LED Strip lighting.
# Based on the example code provided on this page: http://julioterra.com/journal/2013/02/raspberry-pi-and-led-strips-new-python-library/
# You will need this "ledstrip" Python library to run this code: https://github.com/labatrockwell/raspberrypi-experiments/tree/ledstrip_v0.0.2
 
from ledStrip import ledstrip
import time
import random 
import argparse

# Define app description and optional paramerters
parser = argparse.ArgumentParser(description='Example sketch that controls an LED strip via Spacesb. It uses the 	LED Strip Python library for Adafruit\'s LPD8806 LED strips.')

# Define the leds strip length optional parameter
parser.add_argument('-l', '--leds', '--pixels', 
					nargs=1, type=int, default=32,
					help='length of led strip in leds, or pixels')

# read all command line parameters
args = parser.parse_args()

# function that initializes all the things
def main():

	# initialize spi and leds objects
	spidev		= file("/dev/spidev0.0", "wb")  # ref to spi connection to the led bar
	leds 		= ledstrip.LEDStrip(pixels=args.leds, spi=spidev)

	pixel_edge = 0 	# current pixel whose state will be flipped
	turn_on = False  # holds whether pixel will be switched on or off

        red_value = 127
        green_value = 127
        blue_value = 0
                
        t = time.localtime()
        initial_time_hrs = 999
        initial_time_mins = 999
        time_elapsed = 0
        alarm_time = 6 #Setting the alarm time in 24 hour.
        bed_time = 0
        pixel_step = 0
        #wait_time = 0
        #pixel_array = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]

        # Blank out the strip to begin. 
        for each in range(32):
           leds.setPixelColorRGB(pixel=each, red=0, green=0, blue=0)
           leds.show() 
        
        # Blink one light to show boot-up success
        for each in range(5):
            leds.setPixelColorRGB(pixel=1, red=127, green=127, blue=127)
            leds.show()
            time.sleep(1)
            leds.setPixelColorRGB(pixel=1, red=0, green=0, blue=0)
            leds.show()
            time.sleep(1)

	while (True):
                t = time.localtime()
                print "The current time is:", t.tm_hour,":",t.tm_min,":",t.tm_sec, "Light Show mins: ",time_elapsed
                if alarm_time > t.tm_hour:
                    wait_time = alarm_time - t.tm_hour
                    if wait_time <= 1: 
                        print (60 - t.tm_min), "mins until alarm time."
                    if wait_time > 1:
                        print wait_time, "hrs ", (60 - t.tm_min), "mins until alarm time."
                if alarm_time < t.tm_hour:
                    wait_time = (24 - t.tm_hour) + alarm_time 
                    print wait_time, "hrs ", (60 - t.tm_min), "mins until alarm time."
                # Trigger lighting when the time is right
                if (alarm_time == t.tm_hour) and (t.tm_min == 0) and (t.tm_sec < 2):
                    turn_on = True
                    print "Alarm time reached. Switching on light sequence."
                    initial_time_hrs = t.tm_hour
                    initial_time_mins = t.tm_min
                if initial_time_hrs == t.tm_hour:
                    time_elapsed = (t.tm_min - initial_time_mins)
                    pixel_step = time_elapsed
                if initial_time_hrs < t.tm_hour:
                    time_elapsed = (t.tm_min + pixel_step)
                if time_elapsed > 31: time_elapsed = 31
		# update the pixel at the edge of the animation
		if (turn_on == True) and (time_elapsed < 31):
                    leds.setPixelColorRGB(pixel=pixel_edge, red=red_value, green=green_value, blue=blue_value)

		# update all leds
		leds.show()
                #print ("Pixels: ",time_elapsed," Red=",red_value," Green=",green_value," Blue=",blue_value,)

		# advance forward in pixels
		pixel_edge = time_elapsed

                # Fully light up the strip with white, once it has filled with yellow. 
                if pixel_edge == 31:
                    for each in range(32):
                        leds.setPixelColorRGB(pixel=each, red=127, green=127, blue=127)
                        leds.show()

                # Reset everything two hours after the sequence began
                if (t.tm_hour - initial_time_hrs) > 2:
                    time_elapsed = 0
                    pixel_step = 0
                    turn_on = False
                  
		# delay for 1 second
		time.sleep(1)

if __name__ == "__main__":
	main()
