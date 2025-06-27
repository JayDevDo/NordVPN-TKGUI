#!/usr/bin/env python3

############################################
#### 		myTheme.py					####
#### 		Version 20250506 	grid	####
############################################

import os
import tkinter as tk
from tkinter import font as tkFont

# App globals
global baseDir
baseDir = os.path.abspath( os.path.dirname(__file__) )

# logo
global logoPathStr
logoPathStr =  os.path.join( baseDir, "img", "linux-big.png" )

global icoPath
icoPath =  os.path.join( baseDir, "img", "linux-big.png" )

def logoPath():
	return logoPathStr

# Create fonts
def provideFont( size = "N" ):
	mySmallFont = tkFont.Font( family="Arial", size=10, weight=tkFont.NORMAL )
	myNormalFont= tkFont.Font( family="Arial", size=12, weight=tkFont.NORMAL )
	myBigFont 	= tkFont.Font( family="Arial", size=14, weight=tkFont.NORMAL )
	myHugeFont 	= tkFont.Font( family="Arial", size=20, weight=tkFont.NORMAL )

	if size == "S":
		return mySmallFont

	elif size == "N":
		return myNormalFont

	elif size == "B":
		return myBigFont

	elif size == "H":
		return myHugeFont

	elif type(size) == type(1):
		myCustomFont = tkFont.Font( family="Arial", size=size, weight=tkFont.NORMAL )
		# print(f"provideFont {size} = {str(myCustomFont)}")
		return myCustomFont

	else:
		print(f"provideFont unrecognized size = {size} . returning myNormalFont")
		return myNormalFont

##################################################
# TK:

# Buttons
myBttnBG = "#0032B4"
myBttnFG = "#B4FF7D"

# Labels
myLblBG = "#0032B4"
myLblFG = "#B4FF7D"

# ListBoxes/choices
myLbxBG = "#0032B4"
myLbxFG = "#B4FF7D"

# Absolutes
myWhite = "#FFFFFF"
myBlack = "#000000"

myTrue 	= "#AAFF55"
myFalse = "#FF3232"


# Blues
myLBlue = "#96C8FF"
myNBlue = "#329BFF"
myDBlue = "#007DFF"

# Greens
myLGreen= "#00FF7D"
myNGreen= "#00D27D"
myDGreen= "#00AA7D"

# Greys
myLGrey = "#E0E0E0"
myNGrey = "#707070"
myDGrey = "#383838"

# Yellows
myLYellow = "#FFFF28"
myNYellow = "#FFFF55"
myDYellow = "#FFFF7D"

# Reds
myDRed 	= "#FA3232"
myNRed 	= "#FA4B64"
myLRed 	= "#FA9696"
