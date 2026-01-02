#!/usr/bin/env python3

############################################
#### 		nvpnMeshPort.py 			####
#### 		Version 20250620 	grid	####
############################################

import sys
import os
import subprocess
import time
import json

import nvpnPort as nvpnT

import logging
import inspect

def dynamic_logging(message):
    frame = inspect.currentframe().f_back
    function_name = frame.f_code.co_name
    file_name = frame.f_code.co_filename
    line_number = frame.f_lineno
    print(f"{'#=-'*30}")
    print(f"Called from {function_name} in {file_name} at line {line_number}:\n{ message }")
    # logging.info(f"{message} - Called from {function_name} in {file_name} at line {line_number}")


"""
	meshnet commands:

	Usage: nordvpn meshnet peer command [command options] [arguments...]

	Manage your Meshnet devices.
	Learn more:

		Managing Meshnet devices:
		https://meshnet.nordvpn.com/getting-started/how-to-start-using-meshnet/using-meshnet-on-linux#manage-devices

		Meshnet permissions explained:
		https://meshnet.nordvpn.com/features/explaining-permissions

		Routing traffic in Meshnet:
		https://meshnet.nordvpn.com/features/routing-traffic-in-meshnet

	Commands:
		list            Lists available peers in a Meshnet.
		remove          Removes a peer from a Meshnet.
		refresh         Refreshes the Meshnet in case it was not updated automatically.
		incoming        Allows/denies a peer device to access this device remotely (incoming connections).
		routing         Allows/denies a peer device to route all traffic through this device.
		local           Allows/denies access to your local network when a peer device is routing traffic through this device.
		fileshare       Allows/denies peer to send files to this device.
		auto-accept     Always accept file transfers from a specific peer. We won’t ask you to approve each transfer - files will start downloading automatically.
		connect         Treats a peer as a VPN server and connects to it if the peer has allowed traffic routing.
		nickname, nick  Sets/removes a peer device nickname within Meshnet.
		help, h         Shows a list of commands or help for one command

		'Allow Incoming Traffic',    	
		'Allows Incoming Traffic', 		
		'Allow Routing', 				
		'Allows Routing', 				
		'Allow Local Network Access',  	
		'Allows Local Network Access',  
		'Allow Sending Files',   		
		'Allows Sending Files', 
		'Accept Fileshare Automatically'
"""

meshCommandOptions = [
	"auto-accept",
	"connect",
	"fileshare",
	"incoming",
	"local",
	"nickname",
	"peer",
	"refresh",
	"remove",
	"routing"
]

meshCommandActions = [
	"incoming",
	"routing",
	"local",
	"fileshare"
]

def nordVPN_Device(args):
	"""
		Hostname and Nickname change place when Nickname is not "-"
		Stores default device object
			 = Hostname: jayvando-everest.nord
			 = Nickname: -
			 = Status: disconnected
			 = IP:
			 = Public Key: 5sXghSLWHHejUXtRdji1sXs6fcOtxh1LT77ke81Emy0=
			 = OS: linux
			 = Distribution: Linux Mint
			 = Allow Incoming Traffic: enabled
			 = Allow Routing: disabled
			 = Allow Local Network Access: disabled
			 = Allow Sending Files: enabled
			 = Allows Incoming Traffic: enabled
			 = Allows Routing: disabled
			 = Allows Local Network Access: disabled
			 = Allows Sending Files: enabled
			 = Accept Fileshare Automatically: disabled
	"""
	retObj = {}
	for l in args:
		retObj[l.split(':')[0].lstrip()] = l.split(':')[1].lstrip()
	return retObj



def meshPort( cmdArgs:[] ):
	# print(f"nordPort: --cmdArgs: { str( cmdArgs ) }")
	meshPortResp = []

	try:
		if len(cmdArgs) > 1:
			meshPortResp = subprocess.check_output( cmdArgs, stderr=subprocess.STDOUT ).decode('utf-8')
		else:
			print(f"meshPort| cmdArgs must have at least 2 items ('nordvpn', 'meshnet') You passed: { cmdArgs }")
			meshPortResp = ["cmdArgs must have at least 2 items"]

	except Exception as meshPortExcptn:
		print( f"meshPort cmdArgs:{ cmdArgs } gives Exception = { meshPortExcptn }\nreturn code { meshPortExcptn.returncode}\nOutput: { meshPortExcptn.output.decode() }" )
		meshPortResp = [f"{meshPortExcptn.output.decode()}"]

	finally:
		return meshPortResp



def meshCmndRouter( item, optVars=[] ):
	# Here we translate the item into an array of command-strings
	# print(f"meshCmndRouter called with item: { item } and optVars: { str( optVars ) }")
	try:
		itemSupported 	= (item in meshCommandOptions)
		npMeshResponse 	= []
		cmndArr 		= [ "nordvpn", "meshnet", item ]

		if itemSupported:

			if item in [ "connect", "remove" , "peer"]:
				# These items may/must have extra arguments
				cmndArr += optVars
				print(f"meshCmndRouter: --item: { item } --supported: { itemSupported } --cmndArr: { str( cmndArr ) }")

		else:
			print(f"meshCmndRouter: --item: { item } --supported? { itemSupported } --cmndArr: { str( cmndArr ) }")

		# print(f"meshCmndRouter: --item: { item } --supported: { itemSupported } --cmndArr: { str( cmndArr ) }")
		npMeshResponse = meshPort( cmndArr )

	except Exception as meshCmndRouterErr:
		print(f"meshCmndRouter- Exception: { meshCmndRouterErr }")
		npMeshResponse = [""]

	finally:
		# Let the json lib clean the output as well as it can.
		# print(f"commandRouter: npMeshResponse returns:\n{ json.loads( json.dumps( npMeshResponse ) ) }" )
		return json.loads( json.dumps( npMeshResponse ) )


def parseMeshPeerList( rawPeerList ):
	print(f"parseMeshPeerList - rawPeerList len = { len( rawPeerList ) }")
	tmpWorkArr 	= []
	tmpRetArr = [ {}, {} , {} ]
	tmpWorkArr = rawPeerList.splitlines()

	thisDevice = {
		'Hostname': 	"tmpWorkArr[lnNr+1].split(':')[1]",
		'Nickname': 	"tmpWorkArr[lnNr+2].split(':')[1]",
		'IP': 			"tmpWorkArr[lnNr+3].split(':')[1]",
		'Public_Key': 	"tmpWorkArr[lnNr+4].split(':')[1]",
		'OS': 			"tmpWorkArr[lnNr+5].split(':')[1]",
		'Distribution': "tmpWorkArr[lnNr+6].split(':')[1]"
	}
	tmpRetArr[0] = thisDevice

	# print(f"parseMeshPeerList tmpWorkArr = \n{ tmpWorkArr }")
	#	for lnNr, respItem in enumerate( tmpWorkArr ) :
	#		print(f"parseMeshPeerList line:{ lnNr } -respItem = { respItem }")

	# print(f"Array has { tmpWorkArr.count('Hostname:') } hostnames.")
	# print(f"Array has { tmpWorkArr.count('This device:') } X 'This device'. Line = { tmpWorkArr.index('This device:') }")
	# print(f"Array has { tmpWorkArr.count('Local Peers:') } X 'Local Peers' section. Line = { tmpWorkArr.index('Local Peers:') } ")


	if "This device:" in tmpWorkArr:
		lnNrTD = tmpWorkArr.index("This device:")
		thisNvpnDevice = {
			'Hostname': 	tmpWorkArr[lnNrTD+1].split(':')[1].lstrip(),
			'Nickname': 	tmpWorkArr[lnNrTD+2].split(':')[1].lstrip(),
			'IP': 			tmpWorkArr[lnNrTD+3].split(':')[1].lstrip(),
			'Public_Key': 	tmpWorkArr[lnNrTD+4].split(':')[1].lstrip(),
			'OS': 			tmpWorkArr[lnNrTD+5].split(':')[1].lstrip(),
			'Distribution': tmpWorkArr[lnNrTD+6].split(':')[1].lstrip()
		}
		tmpRetArr[0] = thisNvpnDevice

		# print(f"parseMeshPeerList - this device ->\n{ json.dumps( thisNvpnDevice, indent=2 )}")

	else:
		print(f"parseMeshPeerList - No 'This Device' found !")


	if "Local Peers:" in tmpWorkArr:
		lnNrLP = tmpWorkArr.index('Local Peers:')
		print(f"parseMeshPeerList - Local Peers starts at -> { lnNrLP }")
		curLineNr = lnNrLP
		tmpLclPeerArr = []

		for peerLine in tmpWorkArr[ lnNrLP: ]:
			#  print(f"parseMeshPeerList. {curLineNr} peerLine = {peerLine}")

			if "Hostname" in peerLine:
				print(f"parseMeshPeerList. Found another Hostname at { curLineNr }")
				newPeer = nordVPN_Device( tmpWorkArr[ curLineNr:(curLineNr+16) ] )
				tmpLclPeerArr.append( newPeer )

			curLineNr += 1

		tmpRetArr[1] = tmpLclPeerArr
		#  print(f"parseMeshPeerList - Local Peers ->\n{ json.dumps( tmpLclPeerArr, indent = 2 )}")

	else:
		print(f"parseMeshPeerList - No 'Local Peers' found !")


	if "External Peers:" in tmpWorkArr:
		lnNrEP = tmpWorkArr.index('External Peers:')

		if 'no peers' in tmpWorkArr[ lnNrEP + 1 ] :
			print(f"parseMeshPeerList - NO External Peers")
		else:
			print(f"parseMeshPeerList - External Peers starts at -> { lnNrEP }")

			curLineNrEP = lnNrEP
			tmpExtPeerArr = []

			for extPeerLine in tmpWorkArr[ lnNrEP: ]:
				# print(f"parseMeshPeerList. { curLineNrEP } extPeerLine = { extPeerLine }")

				if "Hostname" in extPeerLine:
					print(f"parseMeshPeerList. Found another External Hostname at { curLineNrEP }")
					newExtPeer = nordVPN_Device( tmpWorkArr[ curLineNr:(curLineNrEP+16) ] )
					tmpExtPeerArr.append( newExtPeer )

				curLineNr += 1

			tmpRetArr[2] = tmpExtPeerArr
			# print(f"parseMeshPeerList - External Peers ->\n{ json.dumps( tmpExtPeerArr, indent=2 )}")


	return tmpRetArr



def splitMeshRights( meshDevice ):
	# print(f"nvpnMeshPort | splitMeshRights meshDevice: { json.dumps( meshDevice, indent = 2 ) }" )
	thisDeviceRights = []
	remotePeerRights = []

	for item in meshDevice:

		# print(f"splitMeshRights item = {item}")

		if "Allows" in item:
			remotePeerRights.append( ( item, meshDevice[item] ) )

		elif "Allow" in item:
			thisDeviceRights.append( ( item, meshDevice[item] ) )

	thisDeviceRights.append( ("Accept Fileshare Automatically", meshDevice[item]) )

	# dynamic_logging(f"splitMeshRights retval[0]: { json.dumps( thisDeviceRights, indent = 4 ) }")
	# dynamic_logging(f"splitMeshRights retval[1]: { json.dumps( remotePeerRights, indent = 4 ) }")

	return [ thisDeviceRights, remotePeerRights ]
