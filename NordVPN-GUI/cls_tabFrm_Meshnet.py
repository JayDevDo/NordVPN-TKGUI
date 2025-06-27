#!/usr/bin/env python3

########################################
#### 	cls_tabFrm_Meshnet.py 		####
#### 	Version 20250624 	grid	####
########################################

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json

import myTheme as skin
import nvpnMeshPort as meshPort

from myTable import TkTable as tableMaker

class TabMeshDevices( tk.Frame ):

	def __init__( 
			self, 
			master = None , 
			dimensions = [ 900, 750 ] 
		):
	
		super().__init__(master)
	
		self.master = master
		self.configure( background = skin.myBlack )
		self.grid()
		print(f"TabMeshDevices| --dimensions: {dimensions}")
		self.dimensions = dimensions

		self.tabDevices_Refresh_bttn = tk.Button(
			self,
			text = "Refresh Peer List", 
			command = self.getMeshList,
			bg = "#000000",
			fg = "#00FF00",
			font = skin.provideFont("B")
		)		

		self.tabDevices_GridFrm = tk.LabelFrame(
			self, 
			labelwidget = self.tabDevices_Refresh_bttn, 
			bg = skin.myBlack,
			width 	= self.dimensions[0],
			height 	= self.dimensions[1], 
			labelanchor = 'n'
		)

		self.meshDevices = []

		print(f"TabMeshDevices. current meshDevs = { len( self.meshDevices ) } --> getting meshDevices")
		self.getMeshList() 
		print(f"TabMeshDevices. got meshDevices { len( self.meshDevices ) }")

		self.doLayOut()


	def getMeshList( self ):
		print(f"TabMeshDevices.getMeshList start")
		tmpList = meshPort.meshPort( [ "nordvpn", "meshnet", "peer", "list" ] )
		self.meshDevices = meshPort.parseMeshPeerList(tmpList)
		self.doLayOut()


	def createThisDevicePanel(self,  parentFrame ):
		if len( self.meshDevices[0] ) > 0:
			tDev = self.meshDevices[0]
			print(f"createThisDevicePanel. tDev = { json.dumps( tDev, indent=2 ) }")
			clmnCounter = 0

			for entry in tDev:
				key = entry
				value = self.meshDevices[0][ entry ]
				print(f"createThisDevicePanel - clmn { clmnCounter }: key = { key } value = { value }")

				theLabel = tk.Label( parentFrame, text = key, bg = skin.myLGreen, fg = skin.myBlack, font = skin.provideFont('B') )
				theLabel.grid( row = 0, column = clmnCounter, padx = 2, pady = 2, sticky = "N")

				valTxt = value
				if "Key" in key:
					valTxt = f"{ value[0:12] } ..."

				theValue = tk.Label( parentFrame, text = valTxt, bg = skin.myBlack, fg = skin.myNYellow, font = skin.provideFont('B') )
				theValue.grid( row = 1, column = clmnCounter, padx = 2, pady = 2, sticky = "S")

				clmnCounter += 1


	def doLayOut( self ):
		# 2 Frames. This device info and Peer list
		# peer list has 2 frames, local and external

		self.tabDevices_ThisDeviceFrm = tk.LabelFrame(
			self.tabDevices_GridFrm, 
			# labelwidget = self.tabDevices_Refresh_bttn, 
			text = "This machine",
			bg = skin.myBlack,
			fg = skin.myDRed,
			font = skin.provideFont(18),
			labelanchor = 'n'
		)

		self.createThisDevicePanel( self.tabDevices_ThisDeviceFrm )
		self.tabDevices_ThisDeviceFrm.grid( row = 0, column = 0, padx = 2, pady = 2, sticky = 'WENS' )


		from cls_Frm_Mesh_LocalDevices import PeerList

		self.localPeerFrame = PeerList(
			self.tabDevices_GridFrm, 
			dimensions=[ int( self.dimensions[0] * 0.95 ), int( self.dimensions[1] * 0.80 ) ],
			peerArray = self.meshDevices[1]
		)
		self.localPeerFrame.grid( row = 1, column = 0, padx = 2, pady = 2, sticky = 'WENS' )

		# Finally draw the main Frame of this class
		self.tabDevices_GridFrm.grid( row = 0, column = 0, padx = 2, pady = 2, sticky = 'WENS')



