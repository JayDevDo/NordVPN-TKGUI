#!/usr/bin/env python3

########################################
#### 	cls_tabFrm_Meshnet.py 		####
#### 	Version 20260113 			####
########################################

"""
Version 202601-LM
Works when logged in on a Linux Mint environment.
MESHNET:
	Working:
		- identifying this Device (tD)
		- selecting local peer 	(lP)
		- changing permissions for this tD-lP combo

	To Implement:
		- Changing nickname tD
		- removing lP
"""

import tkinter as tk
from tkinter import ttk
import json

from pubsub import pub

import myTheme as skin
import nvpnPort as nvpnT
import meshnet.nvpnMeshPort as meshPort

from meshnet.cls_Frm_Mesh_ThisDevice import ThisDevice
from meshnet.cls_Frm_Mesh_LocalDevices import SelectedPeer
from meshnet.cls_Frm_Mesh_Rightslabels import MeshRightsLabels

class TabMeshDevices( tk.Frame ):

	def __init__( 
			self, 
			master = None , 
			dimensions = [ 1000, 800 ] 
		):
	
		super().__init__(master)
	
		self.master = master
		self.configure( background = skin.myBlack )
		self.grid()
		self.dimensions = dimensions
		# print(f"TabMeshDevices| --dimensions: { self.dimensions }")

		self.meshNetActivated = nvpnT.getSetting('Meshnet')
		# print(f"self.meshNetActivated = {self.meshNetActivated}")

		self.tabDevices_Refresh_bttn = tk.Button(
			self,
			text = "Refresh Peer List", 
			command = self.getMeshList,
			bg = skin.myBlack,
			fg = skin.myNGreen,
			font = skin.provideFont("B")
		)

		self.tabDevices_GridFrm = tk.LabelFrame(
			self, 
			labelwidget = self.tabDevices_Refresh_bttn, 
			bg = skin.myBlack,
			width 	= self.dimensions[0],
			height 	= self.dimensions[1], 
			padx 	= 5,
			pady 	= 5,
			labelanchor = 's'
		)

		self.meshDevices 		= [] 	# After getMeshList this should have 3 items [thisDevice, localPeers, externalPeers ]
		self.peerNames 			= [] 	# Hostnames gathered from localPeers
		self.selectedPeerIdx 	= 0 	# index of selected peer in localPeers
		self.selectedPeerName 	= ""  	# hostName of selectedPeer from localPeers
		self.selectedPeerArr 	= [] 	# all attributes of selectedPeer from localPeers
		self.peerRights 		= [] 	# contains the rights of this device and selected peer for each other on; routing,local,incoming,fileshare

		if self.meshNetActivated:
			print(f"TabMeshDevices.Init | --current meshDevs = { len( self.meshDevices ) } --> getting meshDevices")
			self.getMeshList() 
			# print(f"TabMeshDevices. got meshDevices { len( self.meshDevices ) }")

		else:
			# Meshnet not activated
			print(f"TabMeshDevices.Init | Meshnet not activated in SETTINGS")
			self.meshNotActiveHdr = tk.Label(
				self,
				text = "Meshnet not activated in SETTINGS",
				font = skin.provideFont("H"),
				bg = skin.myDRed,
				fg = skin.myWhite
			)
			self.meshNotActiveHdr.grid( row = 0, column = 0, columnspan = 3, padx = 2, pady = 2, sticky = 'WENS' )

	#--------------------------------------------------------------------------
	def getMeshList( self ):
		# print(f"TabMeshDevices | getMeshList start")
		# tmpList = meshPort.meshPort( [ "nordvpn", "meshnet", "peer", "list" ] )
		self.meshDevices = meshPort.splitPeerList()
		if len(self.meshDevices)>1:
			self.parsePeerArray( self.meshDevices[1] )
			pub.sendMessage( "thisDeviceUpdate", anyArgs=[ self.meshDevices[0]['Hostname'] ] )

	#--------------------------------------------------------------------------
	def parsePeerArray( self, peerListFull ):
		# To fill the dropdown of peers
		# print(f"TabMeshDevices.parsePeerArray | --peerListFull: { json.dumps( peerListFull, indent = 2 ) }")
		self.peerNames = []

		for p in peerListFull:
			# print(f"parsePeerArray p = { p }")
			self.peerNames.append( p['Hostname'] )

		self.selectedPeerName 	= self.meshDevices[1][self.selectedPeerIdx]['Hostname']
		self.selectedPeerArr 	= self.meshDevices[1][self.selectedPeerIdx]

		#print(f"TabMeshDevices | parsePeerArray - self.peerNames = { json.dumps( self.peerNames, indent = 2 ) }")
		#print(f"TabMeshDevices | parsePeerArray - self.selectedPeerName = { self.selectedPeerName }")
		#print(f"TabMeshDevices | parsePeerArray - self.selectedPeerArr = { json.dumps( self.selectedPeerArr, indent = 2 ) }")
		self.doLayOut()

	#--------------------------------------------------------------------------
	def setPickedPeer( self , event ):
		pickedPeer = self.selectPeer.get() 
		self.selectedPeerIdx 	= self.peerNames.index( pickedPeer )
		self.selectedPeerArr 	= self.meshDevices[1][self.selectedPeerIdx]
		self.selectedPeerName 	= self.selectedPeerArr['Hostname']
		# self.selectedDeviceHdr['text'] = pickedPeer.upper()
		
		#print(f"TabMeshDevices | setPickedPeer-pickedPeer = {pickedPeer}")
		#print(f"TabMeshDevices | setPickedPeer-self.selectPeer.get() = { self.selectPeer.get() }" )
		#print(f"TabMeshDevices | setPickedPeer-self.selectedPeerIdx  = { self.selectedPeerIdx }"  )
		#print(f"TabMeshDevices | setPickedPeer-self.selectedPeerArr  = { json.dumps(self.selectedPeerArr,indent=2)}")
		#print(f"TabMeshDevices | setPickedPeer-self.selectedPeerName = { self.selectedPeerName }" )
		self.peerRights = meshPort.splitMeshRights( self.selectedPeerArr )
		pub.sendMessage( "newPeerSelected", anyArgs=[ self.selectedPeerName, self.selectedPeerArr, self.peerRights ] )
		pub.sendMessage( "newPeerRights", anyArgs=[ self.peerRights, self.selectedPeerName ] )


	#--------------------------------------------------------------------------
	def doLayOut( self ):

		self.thisDeviceHdr = tk.Label(
			self.tabDevices_GridFrm,
			text = "THIS DEVICE:",
			font = skin.provideFont("H"),
			bg = skin.myBlack,
			fg = skin.myDOrange
		)

		self.selectedDeviceHdr = tk.Label(
			self.tabDevices_GridFrm,
			text = "Permissions",
			font = skin.provideFont("B"),
			bg = skin.myBlack,
			fg = skin.myDBlue
		)

		self.comboLabel = tk.Label(
			self.tabDevices_GridFrm,
			text = "CHOOSE PEER",
			font = skin.provideFont("H"),
			bg = skin.myBlack,
			fg = skin.myWhite
		)

		self.selectPeer = ttk.Combobox(
			self.tabDevices_GridFrm,
			state = "readonly",
			values = self.peerNames,
			font = skin.provideFont("B"),
		)
		self.selectPeer.bind('<<ComboboxSelected>>', self.setPickedPeer )

		self.thisDeviceFrm = ThisDevice( 
			self.tabDevices_GridFrm,
			dimensions = [ int( self.dimensions[0] * 0.30 ), int( self.dimensions[1] * 0.60 ) ],
			deviceArr = self.meshDevices[0] 
		)

		self.peerActionsFrame = MeshRightsLabels(
			self.tabDevices_GridFrm, 
			dimensions = [ int( self.dimensions[0] * 0.30 ), int( self.dimensions[1] * 0.60 ) ]
		)

		self.selectedPeerFrame = SelectedPeer(
			self.tabDevices_GridFrm, 
			dimensions=[ int( self.dimensions[0] * 0.30 ), int( self.dimensions[1] * 0.80 ) ]
		)


		self.thisDeviceHdr.grid( 		row = 0, column = 0, rowspan = 2, 	padx = 4, pady = 2, sticky = 'WENS' )
		self.selectedDeviceHdr.grid( 	row = 0, column = 1, rowspan = 2, 	padx = 4, pady = 2, sticky = 'WENS' )

		self.comboLabel.grid( 			row = 0, column = 2, 				padx = 2, pady = 2, sticky = 'WENS' )
		self.selectPeer.grid( 			row = 1, column = 2, 				padx = 2, pady = 2, sticky = 'WENS' )

		self.thisDeviceFrm.grid( 		row = 2, column = 0, 				padx = 2, pady = 2, sticky = 'WENS' )
		self.peerActionsFrame.grid( 	row = 2, column = 1, 				padx = 2, pady = 2, sticky = 'WENS' )
		self.selectedPeerFrame.grid(	row = 2, column = 2, 				padx = 2, pady = 2, sticky = 'WENS' )


		# Finally draw the main Frame of this class
		self.tabDevices_GridFrm.grid( row = 0, column = 0, padx = 2, pady = 2, sticky = 'WENS')
