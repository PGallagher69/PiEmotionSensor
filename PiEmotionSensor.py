#!/usr/bin/python3

#
#################################################
#                                               #
# Title:        PiEmotionSensor                 #
# FileName:     PiEmotionSensor.py              #
# Author:       Pete Gallagher                  #
# Date:         07/03/2017                      #
# Version:      1.0                             #
#                                               #
#################################################
#

#################################################
#                                               #
#                   Imports                     #
#                                               #
#################################################

from picamera import PiCamera               # The Pi Camera
from time import sleep                      # Timing
from threading import Thread                # Threading
from gpiozero import Button                 # GPIO Zero for the Buttons
from signal import pause                    # Delays
from blinkt import set_pixel, show          # The Blinkt Hat Control
from scrollphathd.fonts import font5x7      # The Scroll PHAT HD Control
from datetime import datetime               # Date Time

import http.client, urllib.request, urllib.parse, urllib.error, base64
import time
import json
import sys
import os
import subprocess
import scrollphathd
import blinkt

#################################################
#                                               #
#         Import Tweepy for Twitter             #
#                                               #
#################################################

try:
    import tweepy
    from tweepy import Stream, OAuthHandler
    from tweepy.streaming import StreamListener
except ImportError:
    exit("This script requires the tweepy module\nInstall with: sudo pip install tweepy")

#################################################
#                                               #
#           Twitter Authentication              #
#                                               #
#################################################

ckey = ''           # Consumer key
csecret = ''        # Consumer secret
atoken = ''         # Access token
asecret = ''        # Access secret

#################################################
#                                               #
#           Azure Authentication                #
#                                               #
#################################################

subscription_key = ''       # Azure Subsrciption Key 

#################################################
#                                               #
#               Global Variables                #
#                                               #
#################################################

global inProgress           # Currently Processing an Emotion
global camera               # The Camera Instance
global scrollText           # The Text to Scroll on the Screen
global displayBrightness    # The Display Brightness
global rootFilePath         # The File Root Path

#################################################
#                                               #
#               Faces Definitions               #
#                                               #
#################################################

#
# Smiley Face
#    
def SmileyFace():

    global displayBrightness

    I = displayBrightness
    O = 0.0

    return [[O,O,O,O,O,O,O],
            [O,O,O,O,O,O,O],
            [O,O,O,O,O,O,O],
            [O,O,O,O,O,O,O],
            [O,O,O,O,O,O,O],
            [O,O,O,O,I,O,O],
            [O,I,O,O,O,I,O],
            [O,O,O,O,O,O,I],
            [O,O,O,I,O,O,I],
            [O,O,O,O,O,O,I],
            [O,I,O,O,O,I,O],
            [O,O,O,O,I,O,O],
            [O,O,O,O,O,O,O],
            [O,O,O,O,O,O,O],
            [O,O,O,O,O,O,O],
            [O,O,O,O,O,O,O],
            [O,O,O,O,O,O,O]]

#
# Sad Face
#    
def SadFace():
    
    global displayBrightness

    I = displayBrightness
    O = 0.0

    return [[O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,I,O,O], 
            [O,O,O,I,O,O,O], 
            [I,O,I,O,O,O,O], 
            [O,O,I,O,O,O,O], 
            [O,I,I,O,O,O,O], 
            [O,O,I,O,O,O,O], 
            [I,O,I,O,O,O,O], 
            [O,O,O,I,O,O,O], 
            [O,O,O,O,I,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O]]

#
# Surprised Face
#    
def SurprisedFace():
    
    global displayBrightness

    I = displayBrightness
    O = 0.0

    return [[O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [I,O,O,I,O,O,O], 
            [O,O,I,O,I,O,O], 
            [O,O,I,O,I,O,O], 
            [O,O,I,O,I,O,O], 
            [I,O,O,I,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O]]

#
# Neutral Face
#    
def NeutralFace():
    
    global displayBrightness

    I = displayBrightness
    O = 0.0

    return [[O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,I,O,O,O], 
            [I,O,O,I,O,O,O], 
            [O,O,O,I,O,O,O], 
            [O,I,O,I,O,O,O], 
            [O,O,O,I,O,O,O], 
            [I,O,O,I,O,O,O], 
            [O,O,O,I,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O]]

#
# Angry Face
#    
def AngryFace():
    
    global displayBrightness

    I = displayBrightness
    O = 0.0

    return [[O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,I,O,O], 
            [I,O,O,I,O,O,O], 
            [O,I,O,I,O,O,O], 
            [O,O,O,I,O,O,O], 
            [O,O,O,I,O,O,O], 
            [O,O,O,I,O,O,O], 
            [O,I,O,I,O,O,O], 
            [I,O,O,I,O,O,O], 
            [O,O,O,O,I,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O]]

#
# Contemptful Face
#    
def ContemptfulFace():
    
    global displayBrightness

    I = displayBrightness
    O = 0.0

    return [[O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,I,O,O,O,O], 
            [I,O,I,O,O,O,O], 
            [O,O,I,O,O,O,O], 
            [O,I,O,I,O,O,O], 
            [O,O,O,I,O,O,O], 
            [I,O,O,O,I,O,O], 
            [O,O,O,O,I,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O]]

#
# Disgusted Face
#    
def DisgustedFace():
    
    global displayBrightness

    I = displayBrightness
    O = 0.0

    return [[O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [I,O,O,I,I,O,O], 
            [I,O,I,O,I,O,O], 
            [O,I,I,O,I,O,O], 
            [I,O,I,O,I,O,O], 
            [I,O,O,I,I,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O]]

#
# Fearful Face
#    
def FearfulFace():
    
    global displayBrightness

    I = displayBrightness
    O = 0.0

    return [[O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,I,O,O,O,O,O], 
            [I,O,O,I,O,O,O], 
            [O,O,I,O,I,O,O], 
            [O,O,I,O,I,O,O], 
            [O,O,I,O,I,O,O], 
            [I,O,O,I,O,O,O], 
            [O,I,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O]]

#
# Question Mark (Actually an X!)
#    
def QuestionMark():
    
    global displayBrightness

    I = displayBrightness
    O = 0.0

    return [[O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [I,O,O,O,I,O,O], 
            [O,I,O,I,O,O,O], 
            [O,O,I,O,O,O,O], 
            [O,I,O,I,O,O,O], 
            [I,O,O,O,I,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O], 
            [O,O,O,O,O,O,O]]

#################################################
#                                               #
#               Clear the Display               #
#                                               #
#################################################

def clearScrollPhatHD():

    scrollphathd.scroll_to(0,0)
    scrollphathd.clear()
    scrollphathd.show()


#################################################
#                                               #
#               Clear the Blinkt                #
#                                               #
#################################################

def clearBlinkt():

    blinkt.clear()
    blinkt.show()

#################################################
#                                               #
#               Show a Smiley Face              #
#                                               #
#################################################
   
def showFace(faceToShow):
    
    print("Showing Face")

    clearScrollPhatHD()

    for column in range(0,17):

        for row in range(0,7):

            scrollphathd.set_pixel(column, row, faceToShow[column][row])

    scrollphathd.show()

#################################################
#                                               #
#         Show some Text on the Display         #
#                                               #
#################################################

def setScrollPhatHDText( textToShow, xOffset ):

    global displayBrightness

    #
    # Clear and Reset the ScrollPhatHD Display
    #
    clearScrollPhatHD()

    #
    # Write a Text String to the Displa
    #
    scrollphathd.write_string(textToShow, x=xOffset, y=0, font=font5x7, brightness=displayBrightness)
    scrollphathd.show()

    #
    # Return it's length incase we're scrolling
    #
    return len(textToShow)

#################################################
#                                               #
#               Scroll Some Text                #
#                                               #
#################################################
#
# Scroll Text once across the Scroll PHAT HD
#
# Note: This is intended to be used in threading, as it blocks the main application
#
class scrollTextClass:
    
    def __init__(self):
        self._running = True

    def terminate(self):  
        self._running = False  

    def run(self, textToScroll):

        self._running = True            # Set that we're currently Scrolling Text
        
        length = setScrollPhatHDText(textToScroll, 0)

        for i in range(length):

            if self._running == False:
                clearScrollPhatHD()
                break
            
            try:
                scrollphathd.scroll(1)
                scrollphathd.show()
                sleep(0.1)

            except KeyboardInterrupt:
                clearScrollPhatHD()
                sys.exit(-1)
                break
                
#################################################
#                                               #
#           Scroll Some Text (Loop)             #
#                                               #
#################################################
#
# Scroll Text Forever across the Scroll PHAT HD
#
# Note: This is intended to be used in threading, as it blocks the main application
#
class scrollTextForeverClass:
    
    def __init__(self):
        self._running = True

    def terminate(self):  
        self._running = False  

    def run(self, textToScroll):

        self._running = True

        print("Starting to Scroll: " + textToScroll)
        print(textToScroll)

        setScrollPhatHDText(textToScroll, 0)
            
        while True:

            if self._running == False:
                print("Exitting Scroll Forever")
                clearScrollPhatHD()
                break
            
            try:
                scrollphathd.scroll(1)
                scrollphathd.show()
                sleep(0.05)

            except KeyboardInterrupt:
                clearScrollPhatHD()
                sys.exit(-1)
                break
                
#################################################
#                                               #
#               Show Blinkt Attract             #
#                                               #
#################################################
#
# Shows a moving sequence of LEDs on the Blinkt
#
# Note: This is intended to be used in threading, as it blocks the main application
#
class showBlinkAttractClass:
    
    def __init__(self):
        self._running = True

    def terminate(self):  
        self._running = False  

    def run(self):

        self._running = True

        print("Showing Blinkt Attract")
        
        blinkt.clear()
        blinkt.show()

        while True:

            try:
                for j in range(0, 8, 1):

                    if self._running == False:
                        print("Exitting Show Blinkt Attract")
                        clearBlinkt()
                        return

                    set_pixel(j, 255, 0, 0, 0.1)
                    blinkt.show()
                    time.sleep(0.05)

                for j in range(0, 7, 1):

                    if self._running == False:
                        print("Exitting Show Blinkt Attract")
                        clearBlinkt()
                        return

                    set_pixel(j, 0, 0, 0, 0.1)
                    blinkt.show()
                    time.sleep(0.05)

                for j in range(7, -1, -1):

                    if self._running == False:
                        print("Exitting Show Blinkt Attract")
                        clearBlinkt()
                        return

                    set_pixel(j, 255, 0, 0, 0.1)
                    blinkt.show()
                    time.sleep(0.05)

                for j in range(7, 0, -1):

                    if self._running == False:
                        print("Exitting Show Blinkt Attract")
                        clearBlinkt()
                        return

                    set_pixel(j, 0, 0, 0, 0.1)
                    blinkt.show()
                    time.sleep(0.05)

            except KeyboardInterrupt:
                clearBlinkt()
                sys.exit(-1)
                break

#################################################
#                                               #
#               Show the Attract Text           #
#                                               #
#################################################

def BeginAttractMode():

    #
    # Show the Blinkt Attract mode
    #
    ShowBlinkAttractThread = Thread(target=showBlinktAttract.run) 
    ShowBlinkAttractThread.start()

    #
    # Show the Text Attract Message
    #
    ScrollTextForeverThread = Thread(target=scrollTextForever.run, args=("LET ME SENSE YOUR EMOTION...    ",)) 
    ScrollTextForeverThread.start()

#################################################
#                                               #
#               Scroll Some Text                #
#                                               #
#################################################

def ScrollSomeText( textToScroll ):

    global scrollText

    scrollphathd.scroll_to(0,0)
    ScrollTextThread = Thread(target=scrollText.run, args=(textToScroll,)) 
    ScrollTextThread.start()

#################################################
#                                               #
#               Turn the Flash On               #
#                                               #
#################################################

def flashOn():

    #
    # Set the Blinkt LED's to all white
    #
    blinkt.set_all(255, 255, 255, 0.3)  # Set the Blinkt LED's all on and white
    blinkt.show()

    clearScrollPhatHD()                 # Clear the Display
                
    #
    # Show a bright rectangle as a flash
    #
    for i in range(0,17): # loop through the numbers 0 to 10
        scrollphathd.set_pixel(i, 0, 1) # set the pixel on the row

    for i in range(0,7): # loop through the numbers 0 to 10
        scrollphathd.set_pixel(0, i, 1) # set the pixel on the row

    for i in range(0,17): # loop through the numbers 0 to 10
        scrollphathd.set_pixel(i, 6, 1) # set the pixel on the row

    for i in range(0,7): # loop through the numbers 0 to 10
        scrollphathd.set_pixel(16, i, 1) # set the pixel on the row

    scrollphathd.show()

#################################################
#                                               #
#               Turn the Flash Off              #
#                                               #
#################################################

def flashOff():

    clearScrollPhatHD()                         # Turn off the Flash
    clearBlinkt()                               # Turn off the Blinkt

#################################################
#                                               #
#          Display a Countdown Timer            #
#                                               #
#################################################

def showCountdown():

    clearScrollPhatHD()

    for x in range(3, 0, -1):
        try:
            setScrollPhatHDText(str(x), 5)
            sleep(0.35)
        except KeyboardInterrupt:
            clearScrollPhatHD()
            sys.exit(-1)

    setScrollPhatHDText("GO!", 2)
            
#################################################
#                                               #
#               Send out a Tweet                #
#                                               #
#################################################

def sendTweet( tweetMessage ):

    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    
    api = tweepy.API(auth)
    api.update_status(tweetMessage)

#################################################
#                                               #
#        Send out a Tweet with a Picture        #
#                                               #
#################################################

def tweetImage(url, message):
    
    auth = OAuthHandler(ckey, csecret)
    auth.set_access_token(atoken, asecret)
    
    api = tweepy.API(auth)
    api.update_with_media(url, message)

#################################################
#                                               #
#        Convert and Tweet Image Class          #
#                                               #
#################################################
#
# Note: This is intended to be used in threading, as it blocks the main application
#
class convertAndTweetImageClass:
    
    def __init__(self):
        self._running = True

    def terminate(self):  
        self._running = False  

    def run(self, emotionToTweet, textToTweet, originalFileName):

        self._running = True

        #
        # Get the File Paths
        #
        global rootFilePath

        originalFileNameOnly = os.path.splitext(os.path.basename(originalFileName))[0]
        overlayFilename = rootFilePath + originalFileNameOnly + "-" + emotionToTweet + ".png"
        finalFilename = rootFilePath + originalFileNameOnly + "-" + emotionToTweet + "-caption.png"
        emotionFilename = rootFilePath + "EmotionImages/" + emotionToTweet + ".png"
        
        #
        # Create our new picture using the Original and the corresponding overlay
        #
        os.system("convert -composite '" + originalFileName + "' '" + emotionFilename + "' '" + overlayFilename + "'")

        #
        # Add the Text Caption
        #
        os.system("convert '" + overlayFilename + "' -fill '#0008' -draw 'rectangle 5,400,715,480' -fill white -pointsize 30 -gravity South -annotate +0+30 '" + textToTweet + "' '" + finalFilename + "'")

        #
        # Tweet our new Image
        #
        tweetImage(finalFilename, "The Pi Emotion Sensor thinks you're " + emotionToTweet + "! #PiEmotionSensor")
        
        #
        # Delete the files...
        #
        if os.path.exists(originalFileName):
            os.remove(originalFileName)    

        if os.path.exists(overlayFilename):
            os.remove(overlayFilename)

        if os.path.exists(finalFilename):
            os.remove(finalFilename)    

#################################################
#                                               #
#               Take a Picture                  #
#                                               #
#################################################

def takePicture():

    global camera                               # Get a reference to the Camera Class
    global rootFilePath                         # Get a reference to the root File Path

    clearScrollPhatHD()                         # Clear the Display

    camera.resolution = (720, 480)              # Set the Camera Resolution

    camera.start_preview()                      # Start the Camera Preview (Needs to "warm up" the Camera)

    showCountdown()                             # Show a countdown timer to pass the time while the camera warms up

    sleep(0.5)                                  # A Small Delay

    flashOn()                                   # Turn on the Flash

    sleep(0.5)                                  # A Small Delay

    photoFileName = datetime.now().strftime("%e-%m-%Y-%H-%M-%S") + ".jpg"     # Create a Unique Filename

    photoFileName = os.path.join(rootFilePath, photoFileName)                 # Prepend the correct path to the FileName

    camera.capture(photoFileName)               # Capture an Image

    camera.stop_preview()                       # Turn off the Camera Preview

    flashOff()                                  # Turn off the Flash

    return photoFileName                        # Return the Photo FileName

#################################################
#                                               #
#          Get the Emotion from a Picture       #
#                                               #
#################################################

def getEmotion():
    
    #
    # Get references to our Global Variables
    #
    global inProgress           # the In Progress Flag
    global scrollText           # The Scroll Text Function
    global rootFilePath         # Get a reference to the root File Path

    #
    # Begin by taking a picture using the Raspberry Pi Camera
    #
    photoFilename = takePicture()
    
    #
    # While we're waiting for the Emotion to be Analysed... Scroll some text (This is done in a multi-threaded way)
    #
    ScrollSomeText("Analysing Emotion")
    
    #
    # Prepare the API Call Headers
    #
    headers = {
       # Basic Authorization Sample
       # 'Authorization': 'Basic %s' % base64.encodestring('{username}:{password}'),
       'Content-type': 'application/octet-stream',
    }
 
    #
    # Prepare the API Call Paramaters
    #
    params = urllib.parse.urlencode({
       # Specify your subscription key
       'subscription-key': subscription_key,
       # Specify values for optional parameters, as needed
       #'analyzesFaceLandmarks': 'false',
       #'analyzesAge': 'yes',
       #'analyzesGender': 'false',
       #'analyzesHeadPose': 'false',
    })
    
    #
    # Get the recently taken file and append it to the API call body
    #
    body = ""
    
    f = open(photoFilename, "rb")
    body = f.read()
    f.close()
    
    #
    # Begin our API Call
    #
    try:

        #
        # Setup and perform the Request URL adding the Paramaters, the File (in the Body) and the headers 
        #
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body, headers)
        response = conn.getresponse()
        
        #
        # Get the response from the API Call
        #
        data = response.read()
        
        #
        # Close the connection and decode the JSON data
        #
        conn.close()
        data = json.loads(data.decode("utf-8"))
        
        print("Checking if we have a person")

        #
        # Check if the API Found any faces...
        #
        if 0 < len(data) :

            #
            # We're only interested in one person at the moment, so get the first person found...
            #
            firstPerson = data[0]
            
            #
            # Get the Emotion Scores
            #
            firstPersonScores = firstPerson["scores"]
            
            #
            # Create a custom JSON object to hold the data in a more friendly way
            #
            emotions = {'Happy': firstPersonScores["happiness"] * 100,
                        'Sad' : firstPersonScores["sadness"] * 100,
                        'Surprised' : firstPersonScores["surprise"] * 100,
                        'Neutral' : firstPersonScores["neutral"] * 100,
                        'Angry' : firstPersonScores["anger"] * 100,
                        'Contemptful' : firstPersonScores["contempt"] * 100,
                        'Disgusted' : firstPersonScores["disgust"] * 100,
                        'Fearful' : firstPersonScores["fear"] * 100} 

            #
            # Sort the emotions found by the value in a decending order, so the highest result is the first item in the list
            #
            sortedEmotions = sorted(emotions.items(), key=lambda x: x[1], reverse = True)

            #
            # Get the Key and Value of the first item in the list (the Emotion with the highest score)
            #
            k, v = next(iter(sortedEmotions))

            #
            # Stop the scrolling "Analysing Emotion" text, and pause briefly to let the Display settle 
            #
            scrollText.terminate()
            sleep(0.5)

            #
            # Show the relevant face depending upon which emotion is ranked highest by the API
            #
            textToAddToImage = ""

            if k == "Happy":
                textToAddToImage = "Had a nice day then?"
                blinkt.set_all(255, 0, 128, 0.1)
                blinkt.show()
                showFace(SmileyFace())
            elif k == "Sad":
                textToAddToImage = "Cheer Up, could be worse!"
                blinkt.set_all(0, 0, 255, 0.1)
                blinkt.show()
                showFace(SadFace())
            elif k == "Surprised":
                textToAddToImage = "Won the Lottery?"
                blinkt.set_all(255, 255, 255, 0.1)
                blinkt.show()
                showFace(SurprisedFace())
            elif k == "Neutral":
                textToAddToImage = "Get off the fence!"
                blinkt.set_all(255, 255, 255, 0.1)
                blinkt.show()
                showFace(NeutralFace())
            elif k == "Angry":
                textToAddToImage = "Calm down... Calm down!"
                blinkt.set_all(255, 0, 0, 0.1)
                blinkt.show()
                showFace(AngryFace())
            elif k == "Contemptful":
                textToAddToImage = "Don't hate me"
                blinkt.set_all(255, 128, 0, 0.1)
                blinkt.show()
                showFace(ContemptfulFace())
            elif k == "Disgusted":
                textToAddToImage = "Trod in something icky?"
                blinkt.set_all(0, 255, 0, 0.1)
                blinkt.show()
                showFace(DisgustedFace())
            elif k == "Fearful":
                textToAddToImage = "Seen a ghost?"
                blinkt.set_all(255, 255, 0, 0.1)
                blinkt.show()
                showFace(FearfulFace())

            #
            # Convert and Tweet our Image in another thread, so we can go back and analyse another face quickly!
            #
            tweeter = convertAndTweetImageClass()
            tweeterThread = Thread(target=tweeter.run, args=( k, textToAddToImage, photoFilename, ) ) 
            tweeterThread.start()
            
            #
            # Pause, clean up and revert to the Attract mode
            #
            sleep(5)                    # Wait for 5 seconds just to give the user some time to see the face...
            BeginAttractMode()          # Revert to Attract Mode
            inProgress = False          # Clear the In Progress flag
            
            return data                 # Return our data

        else:

            scrollText.terminate()      # Stop scrolling any text
            sleep(0.5)                  # Let the display settle
            showFace(QuestionMark())    # Show a Question Mark
            sleep(5)                    # Wait for 5 seconds...
            BeginAttractMode()          # Revert to Attract Mode
            inProgress = False          # Clear the In Progress flag
            return                      # Return nothing

    except Exception as e:
        
        print(e)
        scrollText.terminate()          # Stop scrolling any text
        sleep(0.5)                      # Let the display settle
        showFace(QuestionMark())        # Show a Question Mark       
        inProgress = False              # Clear the In Progress flag
        return                          # Return nothing

#################################################
#                                               #
#               Initial Setup                   #
#                                               #
#################################################

print("Begin Initial Setup")

inProgress = False                                  # Make sure we clear that we're currently processing an image
camera = PiCamera()                                 # Create an instance of the PiCamera

startButton = Button(17)                            # Initialise the Start button (Note, current button is push to break!)
quitButton = Button(25)                             # Initialise the Quit button (Note, current button is push to break!)

displayBrightness = 0.1                             # Set the Display Brightness
clearScrollPhatHD()                                 # Clear the Display

scrollText = scrollTextClass()                      # Create the Scroll Text Class
scrollTextForever = scrollTextForeverClass()        # Create the Scroll Forever Class
showBlinktAttract = showBlinkAttractClass()         # Create the Show Blinkt Attract Class

rootFilePath = os.path.dirname(os.path.realpath('__file__')) + '/'           # Get the Root File Path

print("Initial Setup Complete")

#################################################
#                                               #
#            Begin the Main Application         #
#                                               #
#################################################

BeginAttractMode()                                   # Show the main Attract Text

sleep(1)                                            # Startup Delay

exitStart = -1                                      # Used to time exitting the application

#################################################
#                                               #
#              Main Program Loop                #
#                                               #
#################################################

while True:
    
    #
    # If the Start Button is pressed...
    #
    if startButton.is_pressed == False and inProgress == False:

        scrollTextForever.terminate()       # Stop scrolling any text
        showBlinktAttract.terminate()       # Stop the Blinkt Attract Mode
        
        print("Starting")
        inProgress = True                   # Set that we're now Processing an Emotion
        getEmotion()                        # Begin Processing an Emotion

    #
    # If the Quit Button is pressed and we're not in the middle of Sensing and Emotion....
    #
    elif quitButton.is_pressed == False and inProgress == False:

        if  exitStart == -1:
            exitStart = time.perf_counter()
            print("Quit Pressed at " + str(exitStart))

        #
        # Only if we've held the button down for a good while to we actually exit!
        #
        if (time.perf_counter() - exitStart) > 5:

            scrollTextForever.terminate()   # Stop scrolling any text
            showBlinktAttract.terminate()       # Stop the Blinkt Attract Mode
        
            ScrollSomeText("SHUTTING DOWN") # Say Bye!
            sleep(4)                        # Slight Delay
            clearScrollPhatHD()             # Clear the Display
            print("Shutting Down")
            os.system('shutdown now -h')    # Shut Down the System (May require root privelages)
            sys.exit()                      # Exit the Application
    
    #
    # If the Quit button isn't pressed anymore, 
    # but we've held it for long enough then quit instead of shutting down...
    #
    elif quitButton.is_pressed == True and exitStart != -1 and (time.perf_counter() - exitStart) > 2 and inProgress == False:

        scrollTextForever.terminate()   # Stop scrolling any text
        showBlinktAttract.terminate()       # Stop the Blinkt Attract Mode
        
        ScrollSomeText("QUITTING")      # Say Bye!
        sleep(4)                        # Slight Delay
        clearScrollPhatHD()             # Clear the Display
        print("Exitting")
        GPIO.cleanup()                  # Cleanup the GPIO
        sys.exit()                      # Exit the Applicaiton

    #
    # If the Quit button isn't pressed anymore...
    #
    elif quitButton.is_pressed == True and exitStart > -1:

        exitStart = -1                     # Clear the Exit Counter
