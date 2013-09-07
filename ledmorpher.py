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
   userDefinedColour = raw_input('Colour? (clear, yellow, orange, red, purple, blue, lightblue, green, lightgreen, white, pink, random/r): ')
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
   elif (userDefinedColour == 'lightblue'):
       userRed = userPalette[8][0]
       userGreen = userPalette[8][1]
       userBlue = userPalette[8][2]                        
   elif (userDefinedColour == 'lightgreen'):
       userRed = userPalette[9][0]
       userGreen = userPalette[9][1]
       userBlue = userPalette[9][2]
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

def colour_Calculator(morphStartColour, morphEndColour):
    print "Calculating colour range: "
    if morphStartColour == 0: morphStartColour = 1 #Calculations require nonzero
    if morphEndColour == 0: morphEndColour = 1 #Calculations require nonzero
    if morphStartColour > morphEndColour:
        colourRange = morphStartColour - morphEndColour
        colourPolarity = 0
    if morphStartColour < morphEndColour:
        colourRange = morphEndColour - morphStartColour
        colourPolarity = 1
    if morphStartColour == morphEndColour:
    	colourRange = 0
    	colourPolarity = 0
    colourStepValue = colourRange / 8
    print "Colour range value is: ", colourRange
    print "Colour step value is: ", colourStepValue
    print "Colour polarity is: ", colourPolarity
    colourList = []
    colourList.append(colourRange)
    colourList.append(colourPolarity)
    colourList.append(colourStepValue)
    return colourList # colourRange, colourPolarity, colourStepValue
    
def morph_sequence(leds, morphStartColour, morphEndColour, morphTransitionColour, redPolarity, redStepValue, greenPolarity, greenStepValue, bluePolarity, blueStepValue):
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
        if greenPolarity == 1:
            morphTransitionColour[2] = (morphStartColour[2] + greenStepValue)
        if greenPolarity == 0:
            morphTransitionColour[2] = (morphStartColour[2] - greenStepValue)
        if bluePolarity == 1:
            morphTransitionColour[3] = (morphStartColour[3] + blueStepValue)
        if bluePolarity == 0:
            morphTransitionColour[3] = (morphStartColour[3] - blueStepValue)
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
    return morphEndColour
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
        colourList = []
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
        userPalette = [[127,0,0],[0,127,0],[0,0,127],[105,50,17],[37,8,92],[83,46,0],[127,127,127],[127,7,29],[10,26,68],[36,74,0]] 
        #red, green, blue, yellow, purple, orange, white, pink

        while (True):
            userDefinedCommand = raw_input('Command? (m to morph, b to bounce, x to exit): ')
            if (userDefinedCommand=='x'): break
            if (userDefinedCommand=='m'): 
                print "Morphing."
            elif (userDefinedCommand=='b'): 
                print "Bouncing."
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
            
            if (userDefinedCommand=='m'):
            	print "Morphing from", morphStartColour[0], "to", morphEndColour[0]
            
            if (userDefinedCommand=='b'):
            	print "Bouncing from", morphStartColour[0], "to", morphEndColour[0]
            	
            # Blanking old variables from the last colour set
            redStepValue = 0
            redRange = 0
            greenStepValue = 0
            greenRange = 0
            blueStepValue = 0
            blueRange = 0
            
            # Running caclulations for the colour morph values
            print "Red spectrum."
            colourList = colour_Calculator(morphStartColour[1], morphEndColour[1])
            redRange = colourList[0]
            redPolarity = colourList[1]
            redStepValue = colourList[2]
            print "Green spectrum."
            colourList = colour_Calculator(morphStartColour[2], morphEndColour[2])
            greenRange = colourList[0]
            greenPolarity = colourList[1]
            greenStepValue = colourList[2]
            print "Blue spectrum."
            colourList = colour_Calculator(morphStartColour[3], morphEndColour[3])
            blueRange = colourList[0]
            bluePolarity = colourList[1]
            blueStepValue = colourList[2]

            morphTransitionColour = morphStartColour
            
            # Morphing
            if (userDefinedCommand=='m'):
            	morph_sequence(leds, morphStartColour, morphEndColour, morphTransitionColour, redPolarity, redStepValue, greenPolarity, greenStepValue, bluePolarity, blueStepValue)
            
            # Bouncing
            if (userDefinedCommand=='b'):
            	while (True):
            	    morphInterim = []
            	    morphTransitionColour = []
            	    morphInterim = morphEndColour
            	    morphEndColour = morphStartColour
            	    morphStartColour = morphInterim
            	    # Blanking old variables from the last colour set
                    redStepValue = 0
                    redRange = 0
                    greenStepValue = 0
                    greenRange = 0
                    blueStepValue = 0
                    blueRange = 0
            	    # Running caclulations for the colour morph values
                    print "Red spectrum."
                    colourList = colour_Calculator(morphStartColour[1], morphEndColour[1])
                    redRange = colourList[0]
                    redPolarity = colourList[1]
                    redStepValue = colourList[2]
                    print "Green spectrum."
                    colourList = colour_Calculator(morphStartColour[2], morphEndColour[2])
                    greenRange = colourList[0]
                    greenPolarity = colourList[1]
                    greenStepValue = colourList[2]
                    print "Blue spectrum."
                    colourList = colour_Calculator(morphStartColour[3], morphEndColour[3])
                    blueRange = colourList[0]
                    bluePolarity = colourList[1]
                    blueStepValue = colourList[2]
                    morphTransitionColour = morphStartColour
                    morph_sequence(leds, morphStartColour, morphEndColour, morphTransitionColour, redPolarity, redStepValue, greenPolarity, greenStepValue, bluePolarity, blueStepValue)
            
if __name__ == "__main__":
	main()
