#!/usr/bin/env python3

################################
#### 	nvpnPort.py 		####
#### 	Version 20260113 	####
################################

import sys
import os
import subprocess
import time
import json
import psutil
import requests	

from datetime import datetime
# Not used here, so far. from pubsub import pub

import nvpnPort as nvpnT
import myTheme as skin

global glbl_serviceActive
glbl_serviceActive = False

global glbl_loginStatus
glbl_loginStatus = False

global glbl_connectedStatus
glbl_connectedStatus = False

global nordVPNCommandOptions
nordVPNCommandOptions = [ 	"account", 
							"cities",
							"connect",
							"countries", 
							"disconnect",
							"groups", 
							"login",
							"logout",
							"rate",
							"set",
							"settings", 
							"status", 
							"version" ]


jsonPath = os.path.join( os.path.abspath( os.path.dirname(__file__) ) , "jsons")
serverURL = "https://api.nordvpn.com/v1/servers/recommendations?limit=0"

global nordVPNGroupList
global nordVPNChosenGroup
nordVPNGroupList 	= []
nordVPNChosenGroup 	= ""
jsonGrpFile = os.path.join( jsonPath, "groups.json")

global nordVPNCountryList
global nordVPNChosenCountry
nordVPNCountryList 		= []
nordVPNChosenCountry 	= ""
jsonCntFile = os.path.join( jsonPath, "countries.json") 

global nordVPNCityList
global nordVPNChosenCity
global jsonCtyFile
nordVPNCityList = []
nordVPNChosenCity = ""
jsonCtyFile = "" # depends on country

global nordVPNServerList
global nordVPNChosenServer
nordVPNServerList 	= []
nordVPNChosenServer = ""
# Eventually the serverlist will be taken from the server and not stored as json.
jsonSrvrFile = os.path.join( jsonPath, "servers.json")


global connStatusArr
global connStatus
connStatusArr = []
connStatus = False
jsonSttsFile = os.path.join( jsonPath, "status.json")


global allConsArr
allConsArr = []
allConnsPath = os.path.join( jsonPath, "allConns.json" )


def nordProcesses():
	"""  
		Nordprocesses are:
		- commandLine: '/usr/bin/norduserd' processName: 'norduserd'
		- commandLine: '/usr/sbin/nordvpnd' processName: 'nordvpnd'
	
		If the process 'nordvpnd' isn't running, we'll have to ask the user to start it with admin rights;
		'systemctl start nordvpnd.service' . It, in turn, will activate the socket.
		Then the app can handle log-in/out, dis-/connect.
	"""
	global glbl_serviceActive
	global glbl_loginStatus

	for p in psutil.process_iter( [ "pid", "name", "cmdline", "status" ] ):

		if p.info["name"] == "nordvpnd":
			glbl_serviceActive = True
			print(f"nordProcesses: found NORDVPND { p.info['status'] } as { p.info['pid'] }-{ p.info['cmdline'] } " )

		elif p.info["name"] == "norduserd":
			glbl_loginStatus = True
			print(f"nordProcesses: found NORDUSERD { p.info['status'] } as { p.info['pid'] }-{ p.info['cmdline'] } " )

	# as of 6.0 psutil.process_iter.cache_clear()
	return ( glbl_serviceActive, glbl_loginStatus )


def nordPort( cmdArgs:[] ):
	# print(f"nordPort: --cmdArgs: { str( cmdArgs ) }")
	nordPortResp = []

	try:
		if len(cmdArgs) > 1:
			nordPortResp = subprocess.check_output( cmdArgs, stderr= subprocess.STDOUT ).decode('utf-8')
			# subprocess.check_output( cmdArgs ).decode('utf-8')
			# print(f"nordPort: --nordPortResp(RAW): { str( nordPortResp ) }")
		else:
			print(f"nordPort| cmdArgs must have at least 2 items ('nordvpn', 'item')")
			nordPortResp = ["cmdArgs must have at least 2 items"]

	except Exception as nordPortExcptn:

		if nordPortExcptn.returncode == 1:
			# So far I only get this when I'm already logged in. ? logout ?
			if( cmdArgs[1].lower() == "login"):
				nordPortResp = ["You are already logged in."]
				print(f"nordPort| --login: has nordPortExcptn:{ nordPortExcptn }")
			else:
				print(f"nordPort| --cmdArgs: {cmdArgs[1]} exit code non zero. nordPortExcptn:{ nordPortExcptn }")
				nordPortResp = [""]

			# print(f"nordPort: Exception returncode == 1: { nordPortExcptn }\ncmd: { nordPortExcptn.cmd }\nstderr: { nordPortExcptn.stderr }\nreturncode: { nordPortExcptn.returncode }")
		else:
			print(f"nordPort: Exception returncode Else: { nordPortExcptn }\ncmd: { nordPortExcptn.cmd }\nstderr: { nordPortExcptn.stderr }\nreturncode: { nordPortExcptn.returncode }")
			nordPortResp = [""]

	finally:
		tabCount 	= nordPortResp.count('\t')
		lineCount 	= nordPortResp.count('\n')
		colonCount 	= nordPortResp.count(':')

		# print(f"nordPort- { cmdArgs[1] } finally: counting: --tabs: { tabCount  } --lineEnds: { lineCount  } --colons: { colonCount  }\n{ nordPortResp } ")

		if lineCount > 0:
			nordPortRetVal = nordPortResp.splitlines() 
		else:
			nordPortRetVal = nordPortResp

		#if nordPortRetVal[ (len(nordPortRetVal) -1) ] in [ None, "", {}, [] ] :
			#print(f"last line in nordPortRetVal is being popped (should be empty): { nordPortRetVal.pop() }")	

		return nordPortRetVal



def commandRouter( item, optVars=[] ):
	# Here we translate the item into an array of command-strings
	# print(f"commandRouter called with item: { item } and optVars: { str( optVars ) }")
	try:
		itemSupported 	= (item in nordVPNCommandOptions)
		npResponse 		= []
		cmndArr 		= [ "nordvpn", item ]

		if itemSupported:

			if item in [ "cities", "connect", "set", "rate" ]:
				# These items may/must have extra arguments
				cmndArr += optVars
				print(f"commandRouter: --item: { item } --supported: { itemSupported } --cmndArr: { str( cmndArr ) }")

		else:
			print(f"commandRouter: --item: { item } --supported? { itemSupported } --cmndArr: { str( cmndArr ) }")

		# print(f"commandRouter: --item: { item } --supported: { itemSupported } --cmndArr: { str( cmndArr ) }")
		npResponse = nordPort( cmndArr )

	except Exception as commandRouterErr:
		print(f"commandRouter- Exception: { commandRouterErr }")
		npResponse = [""]

	finally:
		# Let the json lib clean the output as well as it can.
		# print(f"commandRouter: npResponse returns:\n{ json.loads( json.dumps( npResponse ) ) }" )
		return json.loads( json.dumps( npResponse ) )



def getNvpnItem( item, optVars=[] ):
	global nordVPNGroupList, nordVPNChosenGroup
	global nordVPNCountryList, nordVPNChosenCountry 
	global nordVPNCityList, nordVPNChosenCity, jsonCtyFile
	global connStatusArr, connStatus

	termRetVal = []
	nvpnTnnlResponse = []

	try:
		itemSupported 	= ( item in nordVPNCommandOptions )
		#==================================================================================================================================
		if item == "account" :
			rawAccsResponse  = commandRouter( item="account" )
			nvpnTnnlResponse = handleResponseTuples( rawAccsResponse )
			# print(f"getNvpnItem - at End of --ACCOUNT-- nvpnTnnlResponse: { str( nvpnTnnlResponse ) }")

		#==================================================================================================================================
		elif item == "cities" :
			# Can only get citites if the country is known
			if len( nordVPNChosenCountry ) > 0:

				rawCityResponse  = commandRouter( item="cities", optVars=[ nordVPNChosenCountry ] )
				nvpnTnnlResponse = cleanCityResponse(rawCityResponse)
				# saveJson( getCityJsonFlNm(), nvpnTnnlResponse )

			else:
				if len(optVars) > 0:
					for i, argum in enumerate( optVars ):
						print(f"getNvpnItem --CITIES-- optVars[{i}] argum: { argum }")		

				nvpnTnnlResponse = [ "first select a country" ]

			# print(f"getNvpnItem - at End of --CITIES-- nvpnTnnlResponse: { str( nvpnTnnlResponse ) }")		

		#==================================================================================================================================
		elif item == "connect" :
			print(f"getNvpnItem: at Start of --CONNECT-- \n optvars: { str(optVars) }")
			rawConnectResponse 	= commandRouter( item="connect" , optVars=optVars )
			nvpnTnnlResponse = handleResponseStrings( rawConnectResponse )
			print(f"getNvpnItem: at End of --CONNECT-- nvpnTnnlResponse: { str( nvpnTnnlResponse ) }")
		
		#==================================================================================================================================
		elif item == "countries":

			if hasJson("countries"):
				cntJsonRetVal = loadJson( jsonCntFile )
				# print(f"getNvpnItem: got countries from json: { str( cntJsonRetVal ) }" )
				nvpnTnnlResponse = cntJsonRetVal

			else: 
				rawCntrsResponse = commandRouter( item="countries" )
				nvpnTnnlResponse = handleResponseArrays( rawCntrsResponse )
				nvpnTnnlResponse.sort() 
				saveJson( jsonCntFile, nvpnTnnlResponse )

			# print(f"getNvpnItem - at End of --COUNTRIES-- nvpnTnnlResponse  : { str( nvpnTnnlResponse ) }")
		
		#==================================================================================================================================
		elif item == "disconnect" :
			rawDisCnnctResponse = commandRouter( item="disconnect" )
			nvpnTnnlResponse = handleResponseStrings( rawDisCnnctResponse )

			# print(f"getNvpnItem - at End of --DISCONNECT-- nvpnTnnlResponse: { str( nvpnTnnlResponse ) }")
		
		#==================================================================================================================================
		elif item == "groups" :

			if hasJson("groups"):
				grpJsonRetVal = loadJson( jsonGrpFile )
				# print(f"getNvpnItem: got groups from json: { str( grpJsonRetVal ) }" )
				nvpnTnnlResponse = grpJsonRetVal

			else: # hasJson("groups") = False
				rawGrpResponse = commandRouter( item="groups" )
				# treat as handleResponseArrays 
				nvpnTnnlResponse = handleResponseArrays( rawGrpResponse )
				nvpnTnnlResponse.sort() 
				saveJson( jsonGrpFile,nvpnTnnlResponse )

			# print(f"getNvpnItem - at End of --GROUPS-- nvpnTnnlResponse: { str( nvpnTnnlResponse ) }")

		#==================================================================================================================================
		elif item == "login" :
			rawLginResponse 	= commandRouter( item="login" )
			# Either the user is already logged in. The response will be "You are already logged in." or ...
			# A html link is returned to be opened in a browser window
			# e.g.: "Continue in the browser: https://api.nordvpn.com/v1/users/oauth/login-redirect?attempt=2e7e88d5-1ee5-4ac4-9a47-3ded0f0307a2"
			# embedded html because of authentication occurs outside this app.
			nvpnTnnlResponse = rawLginResponse
			# "https://api.nordvpn.com/v1/users/oauth/login-redirect?"# 
			# handleResponseStrings( rawLginResponse )

			print(f"getNvpnItem - at End of --LOGIN-- nvpnTnnlResponse: { str( nvpnTnnlResponse ) }")

		#==================================================================================================================================
		elif item == "logout" :
			rawLgoutResponse 	= commandRouter( item="logout" )
			nvpnTnnlResponse = rawLgoutResponse

			print(f"getNvpnItem - at End of --LOGOUT-- nvpnTnnlResponse: { str( nvpnTnnlResponse ) }")

		#==================================================================================================================================
		elif item == "rate" :
			print(f"getNvpnItem: at Start of --RATING-- \n optvars: { str(optVars) }")
			rawRatingResponse = commandRouter( item="rate", optVars=optVars )
			nvpnTnnlResponse = handleResponseStrings( rawRatingResponse )

			print(f"getNvpnItem - at End of --RATING-- nvpnTnnlResponse: { str( nvpnTnnlResponse ) }")
		
		#==================================================================================================================================
		elif item == "set" :
			# The output after setting a setting is 1 line of text. treated as splittable string
			# To activate a setting we can use: 	enable, true,   True, 1, on,   On 
			# To de-activate a setting we can use: disable, false, False, 0, off, Off
			# Using as default: nordvpn set notify enable

			if len(optVars) == 0:
				# print(f"getNvpnItem: --SET--START: No optvars passed. Using 'notify' 'enable' ")
				configItem 	= "notify" 
				configValue = "True" 

			elif len(optVars) == 1:
				# print(f"getNvpnItem: --SET--START: Only 1 optvars passed. Assuming the var is 'configItem': { optVars[0] } by default it will be activated" )
				configItem 	= optVars[0]
				configValue = "True" 

			elif len(optVars) == 2:
				# print(f"getNvpnItem: --SET--START: 2 optvars passed. Assuming item[0]='configItem': { optVars[0] } and item[1]='configValue': { optVars[1] }")
				configItem 	= optVars[0] 
				configValue = str(optVars[1]) 

			else:
				print(f"getNvpnItem: --SET--START: ELSE ")
				for i, argum in enumerate( optVars ):
					print(f"getNvpnItem: --SET-- loop optVars: {i} argum: { argum }" ) 

			rawSttngsSetResponse = commandRouter( item="set", optVars=[ configItem, configValue ] )
			nvpnTnnlResponse	 = handleResponseStrings( rawSttngsSetResponse )

			# print(f"getNvpnItem - at End of --SET-- nvpnTnnlResponse: { str( nvpnTnnlResponse ) }")
		
		#==================================================================================================================================
		elif item == "settings" :
			rawSttngsResponse = commandRouter( item="settings" )
			nvpnTnnlResponse = handleResponseTuples( rawSttngsResponse )

			# print(f"getNvpnItem - at End of --SETTINGS-- nvpnTnnlResponse: { str( nvpnTnnlResponse ) }")
		
		#==================================================================================================================================
		elif item == "status":
			# print(f"getNvpnItem - at START of --STATUS--  getConnStatus: { getConnStatus() }")
			rawSttsResponse 	= commandRouter( item="status" )
			nvpnTnnlResponse 	= handleResponseTuples( rawSttsResponse )
			saveJson( jsonSttsFile, nvpnTnnlResponse )
			connStatusArr 		= nvpnTnnlResponse
			connStatus 			= getConnStatus() 

			# print(f"getNvpnItem - at End of --STATUS-- connStatusArr   : { str( connStatusArr ) }")
			# print(f"getNvpnItem - at End of --STATUS-- nvpnTnnlResponse: { str( nvpnTnnlResponse ) }")
			# print(f"getNvpnItem - at END of --STATUS-- getConnStatus   : { connStatus }")
		
		#==================================================================================================================================
		elif item == "version" :
			rawVrsResponse 	= commandRouter( item="version" )
			nvpnTnnlResponse = handleResponseStrings( rawVrsResponse )

			# print(f"getNvpnItem - at End of --VERSION-- nvpnTnnlResponse: { str( nvpnTnnlResponse ) }")

		#==================================================================================================================================
		else:
			print(f"getNvpnItem: item == Else --unknown item -> { item }")
			nvpnTnnlResponse = []

		#==================================================================================================================================
		#==================================================================================================================================

	except Exception as e:
		print(f"getNvpnItem Exception= {e}")


	finally:
		# print(f"getNvpnItem- finally: { str(nvpnTnnlResponse) }")
		return nvpnTnnlResponse



def getConnStatus():
	global connStatusArr
	try:
		if connStatusArr[0][1].lower():	
			if connStatusArr[0][1].lower() == "connected":
				return True

	except Exception as e:
		connStatus = False

	return False



def getSetting( setting:str ):
	allSettings = getNvpnItem("settings")
	for sttng, val in allSettings:
		if sttng.upper() == setting.upper():
			return val



def getAllItems():
	"""
		Only used in testing commandrouter results
	"""
	nordVPNCountryList = []
	for nvpnCmd in nordVPNCommandOptions:
		if nvpnCmd == "logout":
			pass 
		else:
			print(f"getNvpnItem('{nvpnCmd}')\n { json.dumps( getNvpnItem( nvpnCmd ), indent=4 ) }  ")
		print(f"\n\n")



############################################################################
# For treating account, settings, status, version
def handleResponseTuples( nvpnResponse ):
	# print(f"handleResponseTuples nvpnResponse: { str(nvpnResponse) }")
	treatedArray = []

	try:

		for i, entry in enumerate( nvpnResponse ):

			key, value = entry.split(":")
			if ( value.strip() == "enabled" ):
				val = True
			elif ( value.strip() == "disabled" ):
				val = False
			else:
				val = value.strip()

			treatedArray.append( ( key.replace( " ", "_" ).upper() , val ) )

		return treatedArray
		
	except Exception as myErr1:
		print(f"handleResponseTuples Exception: { myErr1 }")
		return []


# For treating groups, countries, cities
def handleResponseArrays( nvpnResponse ):
	# print(f"handleResponseArrays nvpnResponse: { str(nvpnResponse) }")
	treatedArray = []
	try:
		for i, entry in enumerate( nvpnResponse ):
			tmpSplitEntry =  [ value for value in entry.replace( '\t', ',' ).split(',') if value not in [ None, "", "\t", {}, [] ]  ]
			treatedArray += tmpSplitEntry

		return treatedArray
		
	except Exception as myErr2:
		print(f"handleResponseArrays Exception: { myErr2 }")
		return []


# For treating set, version, ...
def handleResponseStrings( nvpnResponse ):
	return [ datetime.now().isoformat(' ')[0:-7] , " ".join( nvpnResponse ) ]


def cleanCityResponse( nvpnResponse ):
	global nordVPNCityList
	newCleanArray = []
	if type( nvpnResponse ) == type([]):
		# print(f"cleanCityResponse: type [] =  { nvpnResponse }")
		# print(f"cleanCityResponse: len =  { len( nvpnResponse ) }")
		for i,ln in enumerate(nvpnResponse):
			# print(f"newDirtyArray {i} = { ln }")
			newDirtyArray = ln.split(" ")
			# print(f"newDirtyArray[{i}] = {newDirtyArray}")

			for d in newDirtyArray:
				if len(d) > 0:
					newCleanArray.append(d)

	elif( type(nvpnResponse) == type("") ):
		print(f"cleanCityResponse: type '' =  { nvpnResponse }")
		newDirtyArray = str(nvpnResponse).split(" ")
		for d in newDirtyArray:
			if len(d) > 0:
				newCleanArray.append(d)

	else:
		print(f"cleanCityResponse: type unknown =  { type( nvpnResponse ) }")

	# print(f"\n\ncleanCityResponse: after clean =  { json.dumps( newCleanArray, indent = 4 ) }\n\n")
	#nordVPNCityList = newCleanArray
	return newCleanArray

############################################################################
# 	GROUP
def groupListManager( action:str ):
	global nordVPNGroupList
	chosenGroupManager( "clear" )
	if action == "get":
		return nordVPNGroupList
	elif action == "set":
		nordVPNGroupList = getNvpnItem( "groups" )
	elif action == "clear":
		nordVPNGroupList = []
	else:
		print(f"groupListManager action==ELSE ")


def chosenGroupManager( action:str, newVal="" ):
	global nordVPNChosenGroup	
	if action == "get":
		return nordVPNChosenGroup
	elif action == "set":
		nordVPNChosenGroup = newVal
	elif action == "clear":
		nordVPNChosenGroup = ""
	else:
		print(f"chosenGroupManager action==ELSE ")

############################################################################
# 	COUNTRIES
def countryListManager( action:str , filterStr="" ):
	global nordVPNCountryList
	chosenCountryManager( "clear" )
	if action == "get":
		return nordVPNCountryList
	elif action == "set":
		nordVPNCountryList = getNvpnItem("countries")
	elif action == "clear":
		nordVPNCountryList = []
	elif action == "filter":
		countryArray = nordVPNCountryList
		countryArrayFiltered = []
		if len(filterStr) > 0:
			for i, cntry in enumerate( countryArray ):
				if filterStr.lower() in cntry.lower():
					countryArrayFiltered.append( cntry )
		else:
			countryArrayFiltered = countryArray

		return countryArrayFiltered

	else:
		print(f"countryListManager action==ELSE ")


def chosenCountryManager( action:str, newVal="" ):
	print(f"chosenCountryManager { newVal }")
	global nordVPNChosenCountry
	if action == "get":
		return nordVPNChosenCountry
	elif action == "set":
		nordVPNChosenCountry = newVal
		cityListManager("set")
	elif action == "clear":
		nordVPNChosenCountry = ""
		cityListManager("clear")
	else:
		print(f"chosenCountryManager action==ELSE ")


############################################################################
# CITIES
def cityListManager( action:str ):
	global nordVPNCityList
	chosenCityManager("clear")	
	if action == "get" :
		return nordVPNCityList
	elif action == "set" :
		nordVPNCityList = getNvpnItem("cities")
	elif action == "clear" :
		nordVPNCityList = []
	else:
		print(f"cityListManager action == ELSE ")


def chosenCityManager( action:str, newVal="" ):
	global nordVPNChosenCity
	if action == "get":
		return nordVPNChosenCity
	elif action == "set":
		nordVPNChosenCity = newVal
	elif action == "clear":
		nordVPNChosenCity = ""
	else:
		print(f"chosenCityManager action==ELSE ")


def getCityJsonFlNm():
	return os.path.join( jsonPath, "cities", f"{ nordVPNChosenCountry }.json" )


############################################################################
# SERVERS -framework is present but not implemented
def serverListManager( action:str ):
	global nordVPNServerList
	chosenServerManager("clear")	
	if action == "get" :
		return nordVPNServerList
	elif action == "set" :
		srvrRaw 	= requests.get( serverURL )
		srvrList 	= srvrRaw.json()
		print(f"serverListManager-SET: { srvrList } ")
		# just to check the format do only once
		saveJson( jsonSrvrFile, srvrList )
		nordVPNServerList = srvrList
	elif action == "clear" :
		nordVPNServerList = []
	else:
		print(f"cityListManager action == ELSE ")


def chosenServerManager( action:str, newVal="" ):
	global nordVPNChosenServer
	if action == "get":
		return nordVPNChosenServer
	elif action == "set":
		nordVPNChosenServer = newVal
	elif action == "clear":
		nordVPNChosenServer = ""
	else:
		print(f"chosenServerManager action==ELSE ") 


############################################################################
# JSON
def hasJson(item):
	content = []
	if item in [ "groups", "countries", "cities", "status" ]:
		if item == "groups" :
			content =  loadJson( jsonGrpFile )
		elif item == "countries" :
			content =  loadJson( jsonCntFile )
		elif item == "cities" :
			content =  loadJson( getCityJsonFlNm() )
		elif item == "status" :
			content =  loadJson( jsonSttsFile )
	else:
		print(f"hasJson ELSE item: {item} ")

	return len(content) > 0


def loadJson( fileName ):
	try:	
		if os.path.exists( fileName ):
			print(f"loadJson fileName {fileName} exists Yeay!")
			fl = open( fileName )
			content = json.load( fl )
			fl.close()
		else:
			content = []

	except ValueError as e:
		# When the file is empty
		content = []

	finally:
		# print(f"loadJson { fileName } returns { json.dumps( content, indent=2 ) } ")
		return content


def saveJson( fileName, data ):
	#print(f"saving Json to { fileName }")
	fl = open( fileName, "w+" )
	fl.write( json.dumps( data, indent = 4 ) )
	fl.close()


############################################################################
# Connections HIS 
def loadAllConns():
	global allConsArr
	allConsArr = loadJson( allConnsPath )
	print(f"loadAllConns. allConsArr has { len( allConsArr ) } items.")	


def addToConns(newCon):
	global allConsArr

	if newCon in allConsArr:
		allConsArr.remove(newCon)
	
	allConsArr.insert( 0, newCon )
	
	if len(allConsArr) < 3:
		saveJson( allConnsPath, allConsArr )
	else:
		saveJson( allConnsPath, allConsArr[0:3] )

############################################################################
# App-Levels
def appLevels(step=0):
	scrptPth = os.path.abspath( os.path.dirname(__file__) )
	# print(f"scrptPth: { scrptPth }")
	return scrptPth






"""
	--- > INFO
		x	account               Shows account information
		x 	settings              Shows current settings
		x 	status                Shows connection status
		x 	version               Shows the app version

	--- > CONNECTIONS
		x 	login                 Logs you in
		x 	logout                Logs you out
		x 	connect, c            Connects you to VPN
		x 	disconnect, d         Disconnects you from VPN

		x 	cities                Shows a list of cities where servers are available
		x 	countries             Shows a list of countries where servers are available
		x 	groups                Shows a list of available server groups
		x 	rate                  Rates your last connection quality ( 1-5 )

	---> SERVICES
		x 	socket-daemon 		Shows if the necessary system service "nordvpnd" is running and starts it (admin prompt)
		x 	user 				Shows if the necessary system service "norduserd" is running

	--- >  	CONFIGURATION

		x 	set, s              Sets a configuration option
		allowlist, whitelist	Adds or removes an option from the allowlist
		meshnet, mesh         	Meshnet is a way to safely access other devices, no matter where in the world they are. Once set up,
								Meshnet functions just like a secure local area network (LAN) — it connects devices directly. It also
								allows securely sending files to other devices. 
								Use the "nordvpn set meshnet on" command to enable Meshnet.
								Learn more: https://meshnet.nordvpn.com/
		fileshare				Transfer files of any size between Meshnet peers securely and privately


	--- >  	Not included:
			register              Registers a new user account



# Command-line examples:

nordvpn login — log in.
nordvpn connect or nordvpn c — connect to VPN. To connect to specific servers, use nordvpn connect <country_code server_number> (eg. nordvpn connect uk715).
nordvpn disconnect or nordvpn d — disconnect from VPN.
nordvpn c double_vpn — connect to the closest Double VPN server.
nordvpn connect --group double_vpn <country_code> — connect to a specific country using Double VPN servers.
nordvpn connect --group p2p <country_code> — Connect to a specific country using P2P servers.

nordvpn connect P2P — connect to a P2P server.
nordvpn connect The_Americas — connect to servers located in the Americas.
nordvpn connect Dedicated_IP — connect to a Dedicated IP server.

"""
