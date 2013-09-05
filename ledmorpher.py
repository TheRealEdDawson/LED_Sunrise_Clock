#!/usr/bin/python

# Raspberry Pi and LED Strip lighting -- morphs between any two colours.
# It uses the LED Strip Python library for Adafruit\'s LPD8806 LED strips.
# http://www.adafruit.com/products/306
# You will need this "ledstrip" Python library to run this code: 
# https://github.com/labatrockwell/raspberrypi-experiments/tree/ledstrip_v0.0.2
# Based on the library example code provided on this page: 
# http://julioterra.com/journal/2013/02/raspberry-pi-and-led-strips-new-python-library/

from ledStrip import ledstrip
import time
import random 
import argparse
import re

# Define app description and optional parameters
parser = argparse.ArgumentParser(description='A "LED Strip Light Show" made with Raspberry Pi.')

# Define the leds strip length optional parameter
parser.add_argument('-l', '--leds', '--pixels', 
					nargs=1, type=int, default=32,
					help='length of led strip in leds, or pixels')

# read all command line parameters
args = parser.parse_args()

# Function for taking user's input on colour choices.
def choose_a_colour(userPalette, userDefinedColour, userRed, userGreen, userBlue):
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
   #print "Returning values:"
   #print "userDefinedColour: ", userDefinedColour
   #print " userRed:", userRed, " userGreen:", userGreen, " userBlue:", userBlue
   morphList = []
   morphList.append(userDefinedColour)
   morphList.append(userRed)
   morphList.append(userGreen)
   morphList.append(userBlue)
   return morphList # userDefinedColour, userRed, userGreen, userBlue

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
        
        # Blink one green light to show boot-up success
        for each in range(1):
            leds.setPixelColorRGB(pixel=1, red=0, green=127, blue=0)
            leds.show()
            time.sleep(1)
            leds.setPixelColorRGB(pixel=1, red=0, green=0, blue=0)
            leds.show()
            time.sleep(1)

        #Defining a bunch of variables for colour transitions
        userDefinedPixel = 'all'
        userDefinedPixelInt = 0
        userDefinedColour = 'blank'
        userDefinedCommand = 'blank'
        morphStartColour = []
        morphEndColour = []
        morphTransitionColour = []
        morphRange = []
        redRange = 0
        redStepValue = 0
        redPolarity = 0
        greenRange = 0
        greenStepValue = 0
        greenPolarity = 0
        blueRange = 0
        blueStepValue = 0
        bluePolarity = 0
        userRed = 0
        userGreen = 0
        userBlue = 0
        userPalette = [[127,0,0],[0,127,0],[0,0,127],[124,51,1],[37,8,92],[83,46,0],[127,127,127],[127,7,29]] 
        #red, green, blue, yellow, purple, orange, white, pink

        while (True):
            userDefinedCommand = raw_input('Command? (m to morph, x to exit): ')
            if (userDefinedCommand=='x'): break
            if (userDefinedCommand=='m'): 
                print "Morphing."
            else:
            	print "Couldn't understand your command."
            	break
            if not re.search('\d+', userDefinedCommand):
                pass # 'No numbers in command'
            # Capturing the user's choice of colours
            print "Choose a starting colour."
            morphStartColour = choose_a_colour(userPalette, userDefinedColour, userRed, userGreen, userBlue)
            #print "Printing the returned values:"
            #for i in morphStartColour: print i
            print "Choose an ending colour."
            morphEndColour = choose_a_colour(userPalette, userDefinedColour, userRed, userGreen, userBlue)
            #print "Printing the returned values:"
            #for i in morphEndColour: print i
            
            print "Morphing from", morphStartColour[0], "to", morphEndColour[0]
            # Blanking old variables from the last colour set
            redStepValue = 0
            redRange = 0
            greenStepValue = 0
            greenRange = 0
            blueStepValue = 0
            blueRange = 0
            
            print "Calculating red range: "
            if morphStartColour[1] == 0: morphStartColour[1] = 1 #Calculations require nonzero
            if morphEndColour[1] == 0: morphEndColour[1] = 1 #Calculations require nonzero
            if morphStartColour[1] > morphEndColour[1]:
                redRange = morphStartColour[1] - morphEndColour[1]
                redPolarity = 0
            if morphStartColour[1] < morphEndColour[1]:
                redRange = morphEndColour[1] - morphStartColour[1]
                redPolarity = 1
            redStepValue = redRange / 8
            print "Red range value is: ", redRange
            print "Red Step value is: ", redStepValue
            print "Red polarity is: ", redPolarity
            print "Calculating green range: "
            if morphStartColour[2] == 0: morphStartColour[2] = 1 #Calculations require nonzero
            if morphEndColour[2] == 0: morphEndColour[2] = 1 #Calculations require nonzero
            if morphStartColour[2] > morphEndColour[2]:
                greenRange = morphStartColour[2] - morphEndColour[2]
                greenPolarity = 0
            if morphStartColour[2] < morphEndColour[2]:
                greenRange = morphEndColour[2] - morphStartColour[2]
                greenPolarity = 1
            greenStepValue = greenRange / 8
            print "Green range value is: ", greenRange
            print "Green Step value is: ", greenStepValue
            print "Green polarity is: ", greenPolarity
            print "Calculating blue range: "
            if morphStartColour[3] == 0: morphStartColour[3] = 1 #Calculations require nonzero
            if morphEndColour[3] == 0: morphEndColour[3] = 1 #Calculations require nonzero
            if morphStartColour[3] > morphEndColour[3]:
                blueRange = morphStartColour[3] - morphEndColour[3]
                bluePolarity = 0
            if morphStartColour[3] < morphEndColour[3]:
                blueRange = morphEndColour[3] - morphStartColour[3]
                bluePolarity = 1
            blueStepValue = blueRange / 8
            print "Blue range value is: ", blueRange
            print "Blue Step value is: ", blueStepValue
            print "Blue polarity is: ", bluePolarity
            
            morphTransitionColour = morphStartColour
            
            # Morphing
            # Showing initial colour
            for each in range(32):
                leds.setPixelColorRGB(pixel=each, red=morphStartColour[1], green=morphStartColour[2], blue=morphStartColour[3])
            leds.show()
            print "%d, %d, %d" % (morphStartColour[1], morphStartColour[2], morphStartColour[3])
            time.sleep(0.1)
            # Iterating through morph values 2-8 (of 10)
            for i in range (1,8):
                if redPolarity == 1:
                    morphTransitionColour[1] = (morphStartColour[1] + redStepValue)
                if redPolarity == 0:
                    morphTransitionColour[1] = (morphStartColour[1] - redStepValue)
                    print "Subtracted %d from %d" % (redStepValue, morphStartColour[1])
                if greenPolarity == 1:
                    morphTransitionColour[2] = (morphStartColour[2] + greenStepValue)
                if greenPolarity == 0:
                    morphTransitionColour[2] = (morphStartColour[2] - greenStepValue)
                    print "Subtracted %d from %d" % (greenStepValue, morphStartColour[2])
                if bluePolarity == 1:
                    morphTransitionColour[3] = (morphStartColour[3] + blueStepValue)
                if bluePolarity == 0:
                    morphTransitionColour[3] = (morphStartColour[3] - blueStepValue)
                    print "Subtracted %d from %d" % (blueStepValue, morphStartColour[3])
                print "%d, %d, %d" % (morphTransitionColour[1], morphTransitionColour[2], morphTransitionColour[3])
                for each in range(32):
                    leds.setPixelColorRGB(pixel=each, red=morphTransitionColour[1], green=morphTransitionColour[2], blue=morphTransitionColour[3])
                    leds.show()
                time.sleep(0.1)
            # Setting end colour
            for each in range(32):
                leds.setPixelColorRGB(pixel=each, red=morphEndColour[1], green=morphEndColour[2], blue=morphEndColour[3])
            leds.show()
            print "%d, %d, %d" % (morphEndColour[1], morphEndColour[2], morphEndColour[3])
            time.sleep(0.1)
            
            # delay for 1 second
	    #time.sleep(0.1)

if __name__ == "__main__":
	main()
