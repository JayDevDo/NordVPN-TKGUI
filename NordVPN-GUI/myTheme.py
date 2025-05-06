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
logoPathStr =  os.path.join( baseDir, "img", "nordVPNLogo180x50.png" )

global icoPath
icoPath =  os.path.join( baseDir, "img", "nordvpn.png" )
# ! Make/get a better png logo / icon file

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

myTrue 	= "#AAFF55"
myFalse = "#FF3232"

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

# reds
myDRed 	= "#FA3232"
myNRed 	= "#FA4B64"
myLRed 	= "#FA9696"


##################################################
# WX:

"""
myTrue 	= wx.Colour( 170, 255,  85 )
myFalse = wx.Colour( 255,  50,  50 )

# Buttons
myBttnBG = wx.Colour(  0,  50, 180 )
myBttnFG = wx.Colour(180, 255, 125 )

# Labels
myLblBG = wx.Colour(  0,  50, 180 )
myLblFG = wx.Colour(180, 255, 125 )

# ListBoxes/choices
myLbxBG = wx.Colour(  0,  50, 180 )
myLbxFG = wx.Colour(180, 255, 125 )

# Absolutes
myWhite = wx.Colour(255, 255, 255 )
myBlack = wx.Colour(  0,   0,   0 )

# Blues
myLBlue = wx.Colour( 150, 200, 255 )
myNBlue = wx.Colour(  50, 155, 255 )
myDBlue = wx.Colour(   0, 125, 255 )

# Greens
myLGreen= wx.Colour(  0, 255, 125 )
myNGreen= wx.Colour(  0, 210, 125 )
myDGreen= wx.Colour(  0, 170, 125 )

# Greys
myLGrey = wx.Colour(224, 224, 224 )
myNGrey = wx.Colour(112, 112, 112 )
myDGrey = wx.Colour( 56,  56,  56 )

# Yellows
myLYellow = wx.Colour(255, 255,  40 )
myNYellow = wx.Colour(255, 255,  85 )
myDYellow = wx.Colour(255, 255, 125 )

# reds
myDRed 	= wx.Colour( 250,  50,  50 )
myNRed 	= wx.Colour( 250,  75, 100 )
myLRed 	= wx.Colour( 250, 150, 150 )

"""
