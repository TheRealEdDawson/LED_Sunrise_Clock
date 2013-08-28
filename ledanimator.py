#!/usr/bin/python

# A fully sick ghetto "Sunrise Alarm Clock Light" made with Raspberry Pi and LED Strip lighting.
# Based on the example code provided on this page: http://julioterra.com/journal/2013/02/raspberry-pi-and-led-strips-new-python-library/
# You will need this "ledstrip" Python library to run this code: https://github.com/labatrockwell/raspberrypi-experiments/tree/ledstrip_v0.0.2
 
from ledStrip import ledstrip
import time
import random 
import argparse
import re

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

        # Blank out the strip to begin. 
        for each in range(32):
           leds.setPixelColorRGB(pixel=each, red=0, green=0, blue=0)
           leds.show() 
        
        # Blink one light to show boot-up success
        for each in range(1):
            leds.setPixelColorRGB(pixel=1, red=127, green=0, blue=0)
            leds.show()
            time.sleep(1)
            leds.setPixelColorRGB(pixel=1, red=0, green=0, blue=0)
            leds.show()
            time.sleep(1)

        #Defining a bunch of variables for colour transitions
        userDefinedPixel = 'blank'
        userDefinedPixelInt = 0
        userDefinedColour = 'blank'
        userRed = 0
        userGreen = 0
        userBlue = 0
        userPalette = [[127,0,0],[0,127,0],[0,0,127],[124,51,1],[37,8,92],[83,46,0],[127,127,127],[127,7,29]] 
        #red, green, blue, yellow, purple, orange, white, pink

        while (True):
            userDefinedPixel = raw_input('Command? (a to animate, x to exit): ')
            if (userDefinedPixel=='x'): break
            if not re.search('\d+', userDefinedPixel):
                pass # 'No numbers in command'
            else: 
                userDefinedPixelInt  = int(userDefinedPixel)
            if (userDefinedPixelInt > 31):
                print ('Pixel out of range.')
                break
            elif (userDefinedPixelInt < 0):
                print ('Pixel out of range.')
                break
            userDefinedColour = raw_input('Colour? (clear, yellow, orange, red, purple, blue, green, white, pink, random/r): ')
            if (userDefinedColour == 'red'):
                userRed = userPalette[0][0]
                userGreen = userPalette[0][1]
                userBlue = userPalette[0][2]
            elif (userDefinedColour == 'green'):
                userRed = userPalette[1][0]
                userGreen = userPalette[1][1]
                userBlue = userPalette[1][2]
            elif (userDefinedColour == 'blue'):
                userRed = userPalette[2][0]
                userGreen = userPalette[2][1]
                userBlue = userPalette[2][2]
            elif (userDefinedColour == 'yellow'):
                userRed = userPalette[3][0]
                userGreen = userPalette[3][1]
                userBlue = userPalette[3][2]
            elif (userDefinedColour == 'purple'):
                userRed = userPalette[4][0]
                userGreen = userPalette[4][1]
                userBlue = userPalette[4][2]    
            elif (userDefinedColour == 'orange'):
                userRed = userPalette[5][0]
                userGreen = userPalette[5][1]
                userBlue = userPalette[5][2]
            elif (userDefinedColour == 'white'):
                userRed = userPalette[6][0]
                userGreen = userPalette[6][1]
                userBlue = userPalette[6][2]
            elif (userDefinedColour == 'pink'):
                userRed = userPalette[7][0]
                userGreen = userPalette[7][1]
                userBlue = userPalette[7][2]                 
            elif (userDefinedColour == 'clear'):
                userRed = 0
                userGreen = 0
                userBlue = 0
            elif (userDefinedColour=='random' or userDefinedColour=='r'):
                userRed = random.randint(0,127)
                userGreen = random.randint(0,127)
                userBlue = random.randint(0,127)
                print 'Random colour -- Red:',userRed,' Green:',userGreen,' Blue:',userBlue
            else:
                print 'Colour not found'
                        
            
            startColour = []
            startcolour = [127,0,0]
            print "startColour: ", startColour[]
            endColour = []
            endColour = [0,127,0]
            print "endColour: ", endColour[]
            #Calculating midpoint between old and new colours
            redRange = []
            for each in range(startColour[0], endColour[0]):
                redRange[each] = each
            print "redRange = ", redRange
            # Calculate range of values between old and new r,g,b
            
            
            
            # Setting single pixel           
            #leds.setPixelColorRGB(pixel=userDefinedPixelInt, red=userRed, green=userGreen, blue=userBlue)
            # Setting entire range
            if (userDefinedPixel =='all' or userDefinedPixel =='a'):
                for each in range(32):
                    leds.setPixelColorRGB(pixel=each, red=userRed, green=userGreen, blue=userBlue)
            leds.show()

            # Capturing current colour values to morph to
            oldUserRed = userRed
            oldUserGreen = userGreen
            oldUserBlue = userBlue
            
            # delay for 1 seconds
	    time.sleep(0.1)

if __name__ == "__main__":
	main()
