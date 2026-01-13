#!/usr/bin/env python3

########################################
#### cls_Frm_Mesh_ActionButtons.py 	####
#### 	Version 20250701 	grid	####
########################################

import tkinter as tk
from tkinter import ttk

from pubsub import pub

import myTheme as skin
import meshnet.nvpnMeshPort as meshPort
import json

from idlelib.tooltip import Hovertip


class MeshButtonFrame( tk.Frame ):

	def __init__(
			self,
			master = None ,
			dimensions = [ 1000, 600 ],
			deviceNames = ["", ""]
		):

		super().__init__( master )

		self.master = master
		self.dimensions = dimensions

		print(f"MeshButtonFrame| --dimensions: { self.dimensions }")
		print(f"MeshButtonFrame| --deviceNames: { deviceNames }")

		self.thisDevice 		= []
		self.thisDeviceName 	= deviceNames[0]
		self.thisDeviceRights 	= []

		self.chosenPeerDevice 	= []
		self.chosenPeerName 	= deviceNames[1]
		self.chosenPeerRights 	= []

		self.configure( background = skin.myBlack )
		self.grid()

		self.meshActionsGrid = tk.Frame( 
			self, 
			height = self.dimensions[0], 
			width = self.dimensions[1], 
			bg = skin.myBlack 
		)

		self.actionsArr = [
			'Allow Incoming Traffic',    	# 0 
			'Allows Incoming Traffic', 		# 1
			'Allow Routing', 				# 2
			'Allows Routing', 				# 3
			'Allow Local Network Access',  	# 4
			'Allows Local Network Access',  # 5
			'Allow Sending Files',   		# 6
			'Allows Sending Files'   		# 7 , 'Accept Fileshare Automatically'# 8
		]

		self.meshActions = [
			( "incoming", 	[ 0, 1 ] ),
			( "routing", 	[ 2, 3 ] ), 
			( "local", 		[ 4, 5 ] ),
			( "fileshare",  [ 6, 7 ] )
		]

		# Create grid with rights labels in column 0
		rightsLabelRow = 0
		for rightObj in self.meshActions:
			tdRightsLabel = tk.Label(
				self.meshActionsGrid,
				text 	= rightObj[0],
				font  	= skin.provideFont("N"),
				fg 		= skin.myBlack,
				bg 		= skin.myWhite
			)
			tdRightsLabel.grid( row = rightsLabelRow, column = 0 )
			rightsLabelRow +=1

		pub.subscribe( self.peerSelectionListener, 'newPeerSelected' )

		self.doLayOut()


	# actionCommands is called when users click on change to denay/allow
	def actionCommands( self, event, args ):
		try:
			print(f"MeshButtonFrame | Active peer is: { self.chosenPeerName }")
			print(f"MeshButtonFrame | actionCommands args = { args }")

		except Exception as actionsCmdExc:
			print(f"Exception during actionCommands = { actionsCmdExc }")

		finally:
			portCommandArr 	= [ args[0], args[1], self.chosenPeerName ]
			print(f"portCommandArr = { portCommandArr }")
			if len(self.chosenPeerName) > 5:
				commandResponse = meshPort.meshCmndRouter("peer", portCommandArr )
				pubMsg = ""
				for respLine in commandResponse:
					pubMsg += respLine.replace('\n', ' ')

				pubMsg += "Please refresh meshnet devices"	
				pub.sendMessage( "myStatusBarUpdate", anyArgs=pubMsg )
				
			else:
				print(f"MeshButtonFrame | chosenPeer len < 6. {self.chosenPeerName}")


	# peerSelectionListener is called when the user selects a peer from the dropdown in cls_tabFrm_Meshnet
	def peerSelectionListener( self, anyArgs ):
		print(f"MeshButtonFrame | peerSelectionListener - { anyArgs }")
		self.chosenPeerName 	= anyArgs[0]
		self.chosenPeerDevice 	= anyArgs[1]

		self.thisDeviceRights 	= anyArgs[2][0]
		self.chosenPeerRights 	= anyArgs[2][1]

		print(f"MeshButtonFrame | peerSelectionListener --chosenPeerName: { self.chosenPeerName } =? --chosenPeerDevice['Hostname']: { self.chosenPeerDevice['Hostname'] }")
		print(f"MeshButtonFrame | peerSelectionListener --self.thisDeviceRights { self.thisDeviceRights }")
		print(f"MeshButtonFrame | peerSelectionListener --self.chosenPeerRights { self.chosenPeerRights }")
		self.doLayOut()


	# makeButtons is called by doLayOut if a peer was chosen
	def makeButtons( self, parentFrame ):
		print(f"MeshButtonFrame | makeButtons. size of actionsArr = { len( self.actionsArr ) }")
		# For each action 2 buttons. 'Allow' + 'Deny'
		rowNr = 1
		"""
			column groups 
				r1: 3, 	3
				r2: 1,	4, 1
		"""
		for a in self.meshActions:
			actNm = a[0]
			actRights = [
				self.chosenPeerDevice[ self.actionsArr[ a[1][0] ] ] ,
				self.chosenPeerDevice[ self.actionsArr[ a[1][1] ] ] 
			] 

			chngRightsCmmnd = ["disabled","disabled"]
			if actRights[0] == "enabled":
				chngRightsCmmnd[0] = "deny"
				rightsClr = skin.myTrue
			else:
				chngRightsCmmnd[0] = "allow"
				rightsClr = skin.myFalse

			if actRights[1] == "enabled":
				chngRightsCmmnd[1] = "deny"
			else:
				chngRightsCmmnd[1] = "allow"

			print(f"makeButtons action = { actNm }")
			print(f"makeButtons {actNm} thisDevice. val = { self.thisDeviceName  }")
			print(f"makeButtons {actNm} chosenPeerDevice[ action ] = { actNm } { actRights }")
			print(f"makeButtons {actNm} chosenPeerDevice[ chngRightsCmmnd = { chngRightsCmmnd }")

			tdRightsLabel = tk.Label(
				parentFrame,
				text 	= chngRightsCmmnd[0],
				font  	= skin.provideFont("S"),
				fg 		= skin.myBlack,
				bg 		= skin.myWhite
			)
			tdRightsLabel.grid( row = rowNr, column = 0 )
			tdRightsLabel.bind( "<ButtonPress-1>", lambda event, arg=[ actNm , chngRightsCmmnd[0] ]: self.actionCommands( event, arg ) )
			tdRightsLabelToolTip = Hovertip( tdRightsLabel, f"Click to change the {actNm} setting\non this device to '{ chngRightsCmmnd[0] }'\nfor { self.chosenPeerName }")

			actionLabel = tk.Label(
				parentFrame,
				text 	= f"{ actNm.upper() }",
				font  	= skin.provideFont("S"),
				fg 		= skin.myBlack,
				bg 		= rightsClr
			)
			actionLabel.grid( row = rowNr, column = 1, columnspan=4 ,sticky = 'WE' )

			peerRightsLabel = tk.Label(
				parentFrame,
				text 	= actRights[1],
				font  	= skin.provideFont("S"),
				fg 		= skin.myBlack,
				bg 		= skin.myWhite
			)
			peerRightsLabel.grid( row = rowNr, column = 5, sticky = 'WE' )

			rowNr += 1

		allowAuto = self.chosenPeerDevice[ 'Accept Fileshare Automatically' ] 
		if allowAuto == "enabled":
			chngRightsCmmnd[0] = "disable"
			rightsClr = skin.myTrue
		else:
			chngRightsCmmnd[0] = "enable"
			rightsClr = skin.myFalse

		tdRightsLabelA = tk.Label(
			parentFrame,
			text 	= chngRightsCmmnd[0],
			font  	= skin.provideFont("S"),
			fg 		= skin.myBlack,
			bg 		= skin.myWhite
		)
		tdRightsLabelA.grid( row = rowNr, column = 0 )
		tdRightsLabelA.bind( "<ButtonPress-1>", lambda event, arg=['auto-accept', chngRightsCmmnd[0] ]: self.actionCommands( event, arg ) )
		tdRightsLabelToolTip = Hovertip( tdRightsLabelA, f"Click to change the {actNm} setting\non this device to '{ chngRightsCmmnd[0] }'\nfor { self.chosenPeerName }")

		actionLabelA = tk.Label(
			parentFrame,
			text 	= "Allow Automatic Fileshare ",
			font  	= skin.provideFont("S"),
			fg 		= skin.myBlack,
			bg 		= rightsClr
		)
		actionLabelA.grid( row = rowNr, column = 1, columnspan = 4 ,sticky = 'WE' )

		peerRightsLabelA = tk.Label(
			parentFrame,
			text 	= "NA",
			font  	= skin.provideFont("S"),
			fg 		= skin.myBlack,
			bg 		= skin.myWhite
		)
		peerRightsLabelA.grid( row = rowNr, column = 5, sticky = 'WE' )



	def doLayOut( self ):
		"""
			Meshnet actions buttons has 2 columns
			Actions are always relative to the chosen peer
			column 0 Always shown contains the labels of the actions
			column 1 (if peer selected) contains the 4 rights that the selected peer has for this device (display only)
		"""
		if len(self.chosenPeerDevice)>0:
			self.makeButtons(self.meshActionsGrid)
		else:
			print(f"No peer device selected")

		# Finally draw the main grid
		self.meshActionsGrid.grid( row = 0, column = 0, sticky = 'WENS' )
		