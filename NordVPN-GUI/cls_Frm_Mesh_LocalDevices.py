#!/usr/bin/env python3

########################################
#### cls_Frm_Mesh_LocalDevices.py 	####
#### 	Version 20250624 	grid	####
########################################

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json

import myTheme as skin
import nvpnMeshPort as meshPort

from myTable import TkTable as tableMaker

trueLabel 	= [skin.myTrue, skin.myBlack ]
falseLabel 	= [skin.myFalse, skin.myWhite ]

def setLabelColor( lblValue = False, bgOrfg = 0 ):
	# lblValue = False/disabled or True/enabled 
	# bgOrfg = 0. 0=bg, 1=fg
	# if lblValue = True or enabled -> return skin.myTrue for bg and skin.myBlack for fg
	if ( "ENABLED" == lblValue.upper() ) or ( lblValue == True):
		return trueLabel[bgOrfg]
	else:
		return falseLabel[bgOrfg]


class PeerList( tk.Frame ):
	"""
		Frame peerlist has 2 frames.
		Left: list of peers ( tk.Listbox )
		Right: selected peer info ( tk.Frame )
	"""

	def __init__( 
			self, 
			master = None , 
			dimensions = [ 1000, 600 ],
			peerArray = [] 
		):
	
		super().__init__( master )
	
		self.master = master
		self.configure( background = skin.myBlack )
		self.grid()

		print(f"PeerList| --dimensions: { dimensions }")
		self.dimensions = dimensions

		self.peerListGrid = tk.Frame( self, height = self.dimensions[0], width = self.dimensions[1], bg = skin.myLRed )

		self.peerLB_PeerVar = tk.StringVar()
		self.fullPeerArr = peerArray
		self.peerLBArr = tk.StringVar()
		self.peerNames = []

		self.parsePeerArray( peerArray )
		self.doLayOut()



	def parsePeerArray( self, peerListFull ):
		print(f"PeerList start of treat full peer Array")
		print(f"PeerList.peerListFull = { json.dumps( peerListFull, indent = 2 ) }")
		self.peerNames = []
		for p in peerListFull:
			print(f"parsePeerArray p = { p }")
			self.peerNames.append(p['Hostname'])

		print(f"PeerList.peerNames = { json.dumps( self.peerNames, indent = 2 ) }")		
		self.peerLBArr.set( self.peerNames )



	def updatePeerInfoFrame( self, event ):
		pickedPeer = ""
		print(f"updatePeerInfoFrame.self.selectPeerLb.curselection()[0] = { self.selectPeerLb.curselection()[0] }")

		if ( len( self.selectPeerLb.curselection() ) > 0 ):
			pickedPeerIdx = self.selectPeerLb.curselection()[0]
			pickedPeer = event.widget.get( pickedPeerIdx )
			peerFromArray = self.fullPeerArr[ pickedPeerIdx ]
			print(f"updatePeerInfoFrame.pickedPeerIdx = { pickedPeerIdx } = updatePeerInfoFrame.pickedPeer = { pickedPeer }")
			print(f"updatePeerInfoFrame.peerFromArray { json.dumps( peerFromArray, indent = 2 ) }")

			try:
				self.rFrameL.grid_info()
				self.rFrameR.grid_info()

				self.rFrameL.grid_forget()
				self.rFrameR.grid_forget()


			except Exception as e:
				print(f"updatePeerInfoFrame Exception on self.rFrameL- or rFrameR.grid_info() = {e}")

			finally:
				self.rFrameL 	= tk.Frame(	self.rightFrame, bg = skin.myBlack )
				self.rFrameR 	= tk.Frame(	self.rightFrame, bg = skin.myBlack )

				# right frame left labels: 
				hostNameLbl = tk.Label( self.rFrameL, text = "Hostname: ", bg = skin.myBlack, fg = skin.myDGreen, font = skin.provideFont('B') ).grid( 	row = 0, column = 0, padx = 2, sticky = 'E' )
				nickNameLbl = tk.Label( self.rFrameL, text = "Nickname: ", bg = skin.myBlack, fg = skin.myDGreen, font = skin.provideFont('B') ).grid( 	row = 1, column = 0, padx = 2, sticky = 'E' )
				statusLbl 	= tk.Label( self.rFrameL, text = "Status: ", bg = skin.myBlack, fg = skin.myDGreen, font = skin.provideFont('B') ).grid( 	row = 2, column = 0, padx = 2, sticky = 'E' )
				ipLbl 		= tk.Label( self.rFrameL, text = "IP: ", bg = skin.myBlack, fg = skin.myDGreen, font = skin.provideFont('B') ).grid( 		row = 3, column = 0, padx = 2, sticky = 'E' )
				osLbl 		= tk.Label( self.rFrameL, text = "OS: ", bg = skin.myBlack, fg = skin.myDGreen, font = skin.provideFont('B') ).grid( 		row = 4, column = 0, padx = 2, sticky = 'E' )
				distriLbl 	= tk.Label( self.rFrameL, text = "Distribution: ", bg = skin.myBlack, fg = skin.myDGreen, font = skin.provideFont('B') ).grid( row = 5, column = 0, padx = 2, sticky = 'E' )
				pubKeyLbl 	= tk.Label( self.rFrameL, text = "Public Key: ", bg = skin.myBlack, fg = skin.myDGreen, font = skin.provideFont('B') ).grid( row = 6, column = 0, padx = 2, sticky = 'E' )

				# right frame left values: 
				hostNameTxt = tk.Label( self.rFrameL, text = peerFromArray['Hostname'], bg = skin.myBlack, fg = skin.myDBlue, font = skin.provideFont('N') ).grid( 	row = 0, column = 1, padx = 2, sticky = 'W' )
				nickNameTxt = tk.Label( self.rFrameL, text = peerFromArray['Nickname'], bg = skin.myBlack, fg = skin.myDBlue, font = skin.provideFont('N') ).grid( 	row = 1, column = 1, padx = 2, sticky = 'W' )
				statusTxt 	= tk.Label( self.rFrameL, text = peerFromArray['Status'], bg = skin.myBlack, fg = skin.myDBlue, font = skin.provideFont('N') ).grid( 	row = 2, column = 1, padx = 2, sticky = 'W' )
				ipTxt 		= tk.Label( self.rFrameL, text = peerFromArray['IP'], bg = skin.myBlack, fg = skin.myDBlue, font = skin.provideFont('N') ).grid( 		row = 3, column = 1, padx = 2, sticky = 'W' )
				osTxt 		= tk.Label( self.rFrameL, text = peerFromArray['OS'], bg = skin.myBlack, fg = skin.myDBlue, font = skin.provideFont('N') ).grid( 		row = 4, column = 1, padx = 2, sticky = 'W' )
				distriTxt 	= tk.Label( self.rFrameL, text = peerFromArray['Distribution'], bg = skin.myBlack, fg = skin.myDBlue, font = skin.provideFont('N') ).grid(row = 5, column = 1, padx = 2, sticky = 'W' )
				pubKeyTxt 	= tk.Label( self.rFrameL, text = f"{ peerFromArray['Public Key'][0:12]} ..." , bg = skin.myBlack, fg = skin.myDBlue, font = skin.provideFont('N') ).grid( row = 6, column = 1, padx = 2, sticky = 'W' )

				# right frame right labels: 
				aitNameLbl = tk.Label( self.rFrameR, text = "Allow Incoming Traffic", bg = skin.myBlack, fg = skin.myWhite, font = skin.provideFont('N') ).grid( row = 0, column = 0, padx = 2, sticky = 'E' )
				artNameLbl = tk.Label( self.rFrameR, text = "Allow Routing", bg = skin.myBlack, fg = skin.myWhite, font = skin.provideFont('N') ).grid( row = 1, column = 0, padx = 2, sticky = 'E' )
				alnNameLbl = tk.Label( self.rFrameR, text = "Allow Local Network", bg = skin.myBlack, fg = skin.myWhite, font = skin.provideFont('N') ).grid( row = 2, column = 0, padx = 2, sticky = 'E' )
				asfNameLbl = tk.Label( self.rFrameR, text = "Allow Sending Files", bg = skin.myBlack, fg = skin.myWhite, font = skin.provideFont('N') ).grid( row = 3, column = 0, padx = 2, sticky = 'E' )
				astNameLbl = tk.Label( self.rFrameR, text = "Allows Incoming Traffic", bg = skin.myBlack, fg = skin.myWhite, font = skin.provideFont('N') ).grid(row = 4, column = 0, padx = 2, sticky = 'E' )
				asrNameLbl = tk.Label( self.rFrameR, text = "Allows Routing", bg = skin.myBlack, fg = skin.myWhite, font = skin.provideFont('N') ).grid( row = 5, column = 0, padx = 2, sticky = 'E' )
				asnNameLbl = tk.Label( self.rFrameR, text = "Allows Local Network Access", bg = skin.myBlack, fg = skin.myWhite, font = skin.provideFont('N') ).grid(row = 6, column = 0, padx = 2, sticky = 'E' )
				asflNameLbl = tk.Label( self.rFrameR, text = "Allows Sending Files", bg = skin.myBlack, fg = skin.myWhite, font = skin.provideFont('N') ).grid(	row = 7, column = 0, padx = 2, sticky = 'E' )
				afsNameLbl = tk.Label( self.rFrameR, text = "Accept Fileshare Automatically", bg = skin.myBlack, fg = skin.myWhite, font = skin.provideFont('N') ).grid( row = 8, column = 0, padx = 2, sticky = 'E' )
				
				# right frame right values: 
				aitNameTxt = tk.Label( 
					self.rFrameR, 
					text = peerFromArray['Allow Incoming Traffic'], 
					bg = setLabelColor(peerFromArray['Allow Incoming Traffic'],0), 
					fg = setLabelColor(peerFromArray['Allow Incoming Traffic'],1) 
				).grid( row = 0, column = 1, padx = 2, sticky = 'W' )

				artNameTxt = tk.Label( 
					self.rFrameR, 
					text = peerFromArray['Allow Routing'],
					bg = setLabelColor(peerFromArray['Allow Routing'],0), 
					fg = setLabelColor(peerFromArray['Allow Routing'],1) 
				).grid( row = 1, column = 1, padx = 2, sticky = 'W' )
				
				alnNameTxt = tk.Label( 
					self.rFrameR, 
					text = peerFromArray['Allow Local Network Access'],
					bg = setLabelColor(peerFromArray['Allow Local Network Access'],0), 
					fg = setLabelColor(peerFromArray['Allow Local Network Access'],1) 
				).grid( row = 2, column = 1, padx = 2, sticky = 'W' )
				
				asfNameTxt = tk.Label( 
					self.rFrameR, 
					text = peerFromArray['Allow Sending Files'],
					bg = setLabelColor(peerFromArray['Allow Sending Files'],0), 
					fg = setLabelColor(peerFromArray['Allow Sending Files'],1) 
				).grid( row = 3, column = 1, padx = 2, sticky = 'W' )

				astNameTxt = tk.Label( 
					self.rFrameR, 
					text = peerFromArray['Allows Incoming Traffic'],
					bg = setLabelColor(peerFromArray['Allows Incoming Traffic'],0), 
					fg = setLabelColor(peerFromArray['Allows Incoming Traffic'],1) 
				).grid( row = 4, column = 1, padx = 2, sticky = 'W' )
				
				asrNameTxt = tk.Label( 
					self.rFrameR, 
					text = peerFromArray['Allows Routing'],
					bg = setLabelColor(peerFromArray['Allows Routing'],0), 
					fg = setLabelColor(peerFromArray['Allows Routing'],1) 
				).grid( row = 5, column = 1, padx = 2, sticky = 'W' )
				
				asnNameTxt = tk.Label( 
					self.rFrameR, 
					text = peerFromArray['Allows Local Network Access'],
					bg = setLabelColor(peerFromArray['Allows Local Network Access'],0), 
					fg = setLabelColor(peerFromArray['Allows Local Network Access'],1) 
				).grid( row = 6, column = 1, padx = 2, sticky = 'W' )
				
				asflNameTxt = tk.Label( 
					self.rFrameR, 
					text = peerFromArray['Allows Sending Files'],
					bg = setLabelColor(peerFromArray['Allows Sending Files'],0), 
					fg = setLabelColor(peerFromArray['Allows Sending Files'],1) 
				).grid( row = 7, column = 1, padx = 2, sticky = 'W' )
				
				afsNameTxt = tk.Label( 
					self.rFrameR, 
					text = peerFromArray['Accept Fileshare Automatically'],
					bg = setLabelColor(peerFromArray['Accept Fileshare Automatically'],0), 
					fg = setLabelColor(peerFromArray['Accept Fileshare Automatically'],1) 
				).grid( row = 8, column = 1, padx = 2, sticky = 'W' )


				self.rFrameL.grid( row = 0, column = 0, padx = 2, pady = 2, sticky = 'WENS' )
				self.rFrameR.grid( row = 0, column = 1, padx = 2, pady = 2, sticky = 'WENS' )

			"""
				"Hostname": "jayvando-olympic.nord",
				"Nickname": "-",
				"Status": "disconnected",
				"IP": "",
				"OS": "linux",
				"Distribution": "Debian GNU/Linux",
				"Public Key": "MrXmG8JIAmpwePngSOUBgBpIk7n/OoUa++bxewuh4jQ=",

				"Allow Incoming Traffic": "enabled",
				"Allow Routing": "disabled",
				"Allow Local Network Access": "disabled",
				"Allow Sending Files": "enabled",
				"Allows Incoming Traffic": "enabled",
				"Allows Routing": "disabled",
				"Allows Local Network Access": "disabled",
				"Allows Sending Files": "enabled",
				"Accept Fileshare Automatically": "disabled"
			"""



	def peerActionCommands( self, event, args ):
		try:
			selectedPeerIdx = self.selectPeerLb.curselection()[0]
			print(f"Active selection is: { self.selectPeerLb.curselection() }")
		
		except:
			print(f"No active selection yet, using zero")
			selectedPeerIdx = 0
		
		finally:
			print(f"peerActionAllowAccess { args }, idx: { selectedPeerIdx } = { self.fullPeerArr[selectedPeerIdx] }")
			portCommandArr 	= [ args[0], args[1], self.fullPeerArr[selectedPeerIdx]['Hostname'] ]
			commandResponse = meshPort.meshCmndRouter("peer", portCommandArr )
			print(f"peerActionAllowAccess.commandResponse = { commandResponse }")



	def doLayOut( self ):
		print(f"PeerList start of doLayOut")
		self.leftFrame 	= tk.Frame(	self.peerListGrid, bg = skin.myBlack )
		self.rightFrame = tk.Frame(	self.peerListGrid, bg = skin.myBlack )
		self.rFrameL 	= tk.Frame(	self.rightFrame, bg = skin.myBlack )
		self.rFrameR 	= tk.Frame(	self.rightFrame, bg = skin.myBlack )
		self.actionsFrame = tk.Frame( self.peerListGrid, bg = skin.myLYellow )

		self.selectPeerLb = tk.Listbox(
			self.leftFrame,
			selectbackground= skin.myNGreen,
			background 		= skin.myBlack,
			foreground 		= skin.myLbxFG,
			height 			= len(self.fullPeerArr),
			selectmode 		= tk.SINGLE,
			listvariable 	= self.peerLBArr,
			font 			= skin.provideFont(14) 
		)
		self.selectPeerLb.configure( exportselection = False )
		self.selectPeerLb.bind( "<<ListboxSelect>>", self.updatePeerInfoFrame )
		self.selectPeerLb.grid( row = 0, column = 0, padx = 2, pady = 2, sticky = 'WENS' )


		self.bttnAllowIncoming = tk.Button(
			self.actionsFrame,
			text 	= "Allow incoming",
			font  	= skin.provideFont("B"),
			bg 		= skin.myWhite,
			fg 		= skin.myDGreen
		)
		self.bttnAllowIncoming.bind(
			"<ButtonPress-1>", 
			lambda event, arg=["incoming", "allow" ]: self.peerActionCommands( event, arg )
		)
		self.bttnAllowIncoming.grid( row = 0, column = 0 )


		self.bttnDenyIncoming = tk.Button(
			self.actionsFrame,
			text 	= "Deny incoming",
			font  	= skin.provideFont("B"),
			bg 		= skin.myWhite,
			fg 		= skin.myDGreen
		)
		self.bttnDenyIncoming.bind(
			"<ButtonPress-1>", 
			lambda event, arg=["incoming", "deny" ]: self.peerActionCommands( event, arg )
		)
		self.bttnDenyIncoming.grid( row = 1, column = 0 )


		self.bttnAllowFileshare = tk.Button(
			self.actionsFrame,
			text 	= "Allow fileshare",
			font  	= skin.provideFont("B"),
			bg 		= skin.myWhite,
			fg 		= skin.myDGreen
		)
		self.bttnAllowFileshare.bind(
			"<ButtonPress-1>", 
			lambda event, arg=["fileshare", "allow" ]: self.peerActionCommands( event, arg )
		)
		self.bttnAllowFileshare.grid( row = 0, column = 1 )

		self.bttnDenyFileshare = tk.Button(
			self.actionsFrame,
			text 	= "Deny fileshare",
			font  	= skin.provideFont("B"),
			bg 		= skin.myWhite,
			fg 		= skin.myDGreen
		)
		self.bttnDenyFileshare.bind(
			"<ButtonPress-1>", 
			lambda event, arg=["fileshare", "deny" ]: self.peerActionCommands( event, arg )
		)
		self.bttnDenyFileshare.grid( row = 1, column = 1 )


		self.bttnEnableAutoAccept = tk.Button(
			self.actionsFrame,
			text 	= "Allow auto accept",
			font  	= skin.provideFont("B"),
			bg 		= skin.myWhite,
			fg 		= skin.myDGreen
		)
		self.bttnEnableAutoAccept.bind(
			"<ButtonPress-1>", 
			lambda event, arg=[ "auto-accept", "enable" ]: self.peerActionCommands( event, arg )
		)
		self.bttnEnableAutoAccept.grid( row = 0, column = 2 )

		self.bttnDisableAutoAccept = tk.Button(
			self.actionsFrame,
			text 	= "Deny auto accept",
			font  	= skin.provideFont("B"),
			bg 		= skin.myWhite,
			fg 		= skin.myDGreen
		)
		self.bttnDisableAutoAccept.bind(
			"<ButtonPress-1>", 
			lambda event, arg=["auto-accept", "disable" ]: self.peerActionCommands( event, arg )
		)
		self.bttnDisableAutoAccept.grid( row = 1, column = 2 )


		self.bttnAllowRouting = tk.Button(
			self.actionsFrame,
			text 	= "Allow routing",
			font  	= skin.provideFont("B"),
			bg 		= skin.myWhite,
			fg 		= skin.myDGreen
		)
		self.bttnAllowRouting.bind(
			"<ButtonPress-1>", 
			lambda event, arg=[ "routing", "allow" ]: self.peerActionCommands( event, arg )
		)
		self.bttnAllowRouting.grid( row = 2, column = 0 )

		self.bttnDenyRouting = tk.Button(
			self.actionsFrame,
			text 	= "Deny routing",
			font  	= skin.provideFont("B"),
			bg 		= skin.myWhite,
			fg 		= skin.myDGreen
		)
		self.bttnDenyRouting.bind(
			"<ButtonPress-1>", 
			lambda event, arg=["routing", "deny" ]: self.peerActionCommands( event, arg )
		)
		self.bttnDenyRouting.grid( row = 3, column = 0 )

	
		self.bttnAllowLocal = tk.Button(
			self.actionsFrame,
			text 	= "Allow local",
			font  	= skin.provideFont("B"),
			bg 		= skin.myWhite,
			fg 		= skin.myDGreen
		)
		self.bttnAllowLocal.bind(
			"<ButtonPress-1>", 
			lambda event, arg=[ "local", "allow" ]: self.peerActionCommands( event, arg )
		)
		self.bttnAllowLocal.grid( row = 2, column = 1 )

		self.bttnDenyLocal = tk.Button(
			self.actionsFrame,
			text 	= "Deny local",
			font  	= skin.provideFont("B"),
			bg 		= skin.myWhite,
			fg 		= skin.myDGreen
		)
		self.bttnDenyLocal.bind(
			"<ButtonPress-1>", 
			lambda event, arg=["local", "deny" ]: self.peerActionCommands( event, arg )
		)
		self.bttnDenyLocal.grid( row = 3, column = 1 )


		self.bttnConnectPeer = tk.Button(
			self.actionsFrame,
			text 	= "Connect peer",
			font  	= skin.provideFont("B"),
			bg 		= skin.myWhite,
			fg 		= skin.myDGreen
		)
		self.bttnConnectPeer.bind(
			"<ButtonPress-1>", 
			lambda event, arg=[ "connect", "" ]: self.peerActionCommands( event, arg )
		)
		self.bttnConnectPeer.grid( row = 2, column = 2 )

		self.bttnDisconnectPeer = tk.Button(
			self.actionsFrame,
			text 	= "Disconnect peer",
			font  	= skin.provideFont("B"),
			bg 		= skin.myWhite,
			fg 		= skin.myDGreen
		)
		self.bttnDisconnectPeer.bind(
			"<ButtonPress-1>", 
			lambda event, arg=["disconnect", "" ]: self.peerActionCommands( event, arg )
		)
		self.bttnDisconnectPeer.grid( row = 3, column = 2 )


		self.leftFrame.grid( row = 0, column = 0, padx = 2,	pady = 2, sticky = 'NS')
		self.rightFrame.grid( row = 0, column = 1, padx = 2, pady = 2, sticky = 'NS')

		self.actionsFrame.grid( row = 1, column = 0, columnspan = 2, padx = 2, pady = 2, sticky = 'WENS' )
		self.peerListGrid.grid( row = 0, column = 0, padx = 2, pady = 2, sticky = 'WENS' )
