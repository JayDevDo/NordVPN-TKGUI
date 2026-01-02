#!/usr/bin/env python3

########################################
#### 		myTheme.py				####
#### 	Version 20250723 	grid	####
########################################

import os
import tkinter as tk
from tkinter import font as tkFont
from cairosvg import svg2png


# App globals
global baseDir
baseDir = os.path.abspath( os.path.dirname(__file__) )

# logo
global logoPathStr
logoPathStr =  os.path.join( baseDir, "img", "linux-big.png" )
print(f"myTheme | logoPathStr exists? { os.path.isfile( logoPathStr ) } ")

global icoPath
icoPath =  os.path.join( baseDir, "img", "linux-big.png" )
print(f"myTheme | icoPath exists? { os.path.isfile( icoPath ) } ")

global inAppSvgPaths
inAppSvgPaths =  os.path.join( baseDir, "img/fontawesome7.0.0/svgs/solid/" )
print(f"myTheme | inAppSvgPaths exists? { os.path.isdir( inAppSvgPaths ) } ")

global inAppIconsPath
inAppIconsPath =  os.path.join( baseDir, "img", "inAppIcons" )
print(f"myTheme | inAppIconsPath exists? { os.path.isdir( inAppIconsPath ) } ")


def logoPath():
	return logoPathStr


def convertToPNG( svgName ):
	srcName = os.path.join( inAppSvgPaths, f"{svgName}.svg" )
	pngName = os.path.join( inAppIconsPath, f"{svgName}.png" )

	if os.path.exists( pngName ):
		print(f"myTheme | convertToPNG --svgName: { svgName } = { srcName }\nexists already as\n{ pngName }" )
	else:
		if os.path.exists( srcName ):
			svg_code = open( srcName, 'rt').read()
			svg2png( bytestring = svg_code, write_to = pngName )

	return pngName



def iconPath( iconName="pan-down-symbolic"):
	retValPath = convertToPNG( iconName )
	print(f"returning iconPath: { retValPath }")
	if os.path.isfile(retValPath):
		return retValPath
	else:
		return os.path.join( inAppIconsPath, "arrow-rotate-left.png" )


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
myLblBG = "#0032B4" # dark blue
myLblFG = "#B4FF7D" # light green

# ListBoxes/choices
myLbxBG = "#0032B4"
myLbxFG = "#B4FF7D"

# Absolutes
myWhite = "#FFFFFF"
myBlack = "#000000"

myTrue 	= "#AAFF55"
myFalse = "#FF3232"

# Oranges
myLOrange = "#FFCC80"
myNOrange = "#FFB546"
myDOrange = "#FF9900"

# Blues
myLBlue = "#96C8FF"
myNBlue = "#329BFF"
myDBlue = "#007DFF"
myDDBlue = "#1F1F7A"

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

# Purples
myLPurple = "#FF00FF"
myNPurple = "#BB00BB"
myDPurple = "#990099"
