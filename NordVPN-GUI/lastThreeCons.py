#!/usr/bin/env python3

############################################
#### 		lastThreeCons.py 			####
#### 		Version 250405_1800 		####
############################################

import sys
import os
import subprocess
import time
import json
import psutil
import requests	

from datetime import datetime
#from pubsub import pub

import nvpnPort as nvpnT
import myTheme as skin

global allConsArray
allConsArray = []

global lastConsArray
lastConsArray = []


def getJsonList():
	global lastConsArray
	print(f"getJsonList: @start lastConsArray is: \n{ json.dumps( lastConsArray, indent = 4 ) }")
	fromJsonArr = nvpnT.loadJson(nvpnT.jsonlastConsFile)
	print(f"getJsonList: @start jsonFile is: \n{ json.dumps( fromJsonArr, indent = 4 ) }")



def addToList(newCon):
	print(f"addToList: {newCon}")
	allConsArray.append(newCon)
	nvpnT.saveJson( nvpnT.jsonAllConsFile, allConsArray )

	if( len(lastConsArray) > 2 ):
		# add to array at index 0
		# slice array keeping 0,1,2
	else:
		# add to array at index 0

	nvpnT.saveJson( nvpnT.jsonlastConsFile, lastConsArray )


def updateButtons():
	print(f"updateButtons: ")


def saveJson( fileName, data ):
	#print(f"saving Json to { fileName }")
	fl = open( fileName, "w+" )
	fl.write( json.dumps( data, indent = 4 ) )
	fl.close()
