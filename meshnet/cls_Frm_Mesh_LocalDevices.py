#!/usr/bin/env python3

########################################
#### cls_Frm_Mesh_LocalDevices.py 	####
#### 		Version 20260110		####
########################################

import os, json
import tkinter as tk
import myTheme as skin
import meshnet.nvpnMeshPort as meshPort
from pubsub import pub
from idlelib.tooltip import Hovertip

class SelectedPeer( tk.Frame ):

	#--------------------------------------------------------------------------
	def __init__(
			self,
			master = None ,
			dimensions = [ 1000, 600 ]
		):

		super().__init__( master )

		self.master = master
		self.configure( background = skin.myBlack )
		self.grid()
		self.dimensions = dimensions
		self.showAttrs = ["Status","Hostname","Nickname","IP","Public Key","OS","Distribution"]
		# print(f"SelectedPeer| --dimensions: { self.dimensions }")

		self.selectedPeerGrid = tk.Frame( 
			self, 
			height 	= self.dimensions[0], 
			width 	= self.dimensions[1], 
			bg 		= skin.myBlack 
		)

		self.chosenPeerName = ""
		self.thisDeviceName = ""
		self.chosenPeerArr 	= []
		self.peerRights 	= []

		pub.subscribe( self.peerSelectionListener, 	'newPeerSelected' )	
		pub.subscribe( self.thisDeviceListener, 	'thisDeviceUpdate' )	

		self.doLayOut()

	#--------------------------------------------------------------------------
	def thisDeviceListener( self, anyArgs ):
		# pub.sendMessage( "thisDeviceUpdate", anyArgs=[ self.meshDevices[0]['Hostname'] ] )
		# print(f"SelectedPeer | thisDeviceListener - { anyArgs }")
		self.thisDeviceName = anyArgs[0]

	#--------------------------------------------------------------------------
	def peerSelectionListener( self, anyArgs ):
		# print(f"SelectedPeer | peerSelectionListener - { json.dumps( anyArgs, indent = 4 ) }")
		self.chosenPeerName = anyArgs[0]
		self.chosenPeerArr 	= anyArgs[1]
		self.peerRights 	= anyArgs[2][1]
		# print(f"SelectedPeer.peerSelectionListener | --self.peerRights: { self.peerRights }")
		self.doLayOut()

	#--------------------------------------------------------------------------
	def doLayOut( self ):
		"""
			Each row consists of rightsIndecator, DeviceAtrr, DeviceAtrrValue
			Data for permissions are taken from self.peerRights 
			Data for DeviceAtrr and DeviceAtrrValue are taken from self.chosenPeerArr
		"""
		self.bFrameUp = tk.Frame( self.selectedPeerGrid, bg = skin.myBlack )
		# Filter attributes of self.chosenPeerArr
		#  [ myPic for myPic in tmpImgList if myPic.split('.')[-1] in self.allowedExtensions ]
		chosenPeerAttrs = [ pAttr for pAttr in self.chosenPeerArr if pAttr in self.showAttrs ]

		if len( chosenPeerAttrs ) > 0:
			# print(f"SelectedPeer.doLayOut | START --chosenPeerAttrs: { json.dumps( chosenPeerAttrs, indent=4 ) }")
			
			try:
				if self.bFrameUp.grid_info():
					self.bFrameUp.grid_forget()

			except Exception as e:
				print(f"SelectedPeer | updatePeerInfoFrame Exception = {e}")

			finally:
				# First add localPeer Attrs (currently 7 out of 18 total )
				# Second add localPeer permissions (4)
				rghtsClmn = 0 
				valueClmn = 1
				labelClmn = 2 

				statusLblBG = skin.myLGreen if self.chosenPeerArr['Status'].lower() == "connected" else skin.myDRed
				for i,a in enumerate(self.showAttrs):
					# print(f"SelectedPeer.doLayOut | --i: {i} --a: {a} --self.chosenPeerArr[a]: { self.chosenPeerArr[a] }")
	
					attr_lbl = tk.Label( 
						self.bFrameUp, 
						text = f"{ a.upper() }", 
						bg = skin.myBlack, 
						fg = skin.myDBlue, 
						font = skin.provideFont('B') 
					)

					attr_val_txt = f"{self.chosenPeerArr[a][0:10]}..." if a == "Public Key" else self.chosenPeerArr[a]
					attr_val = tk.Label( 
						self.bFrameUp, 
						text = f"{ attr_val_txt } ", 
						bg = skin.myDBlue, 
						fg = skin.myBlack, 
						font = skin.provideFont('B') 
					)

					attr_lbl.grid( row = i, column = labelClmn, padx = 2, pady = 2, sticky = 'WE' )
					attr_val.grid( row = i, column = valueClmn, padx = 2, pady = 2, sticky = 'WE' )

				for i,p in enumerate(self.peerRights):
					# print(f"SelectedPeer.doLayOut | --i: {i} --p: {p} --self.peerRights[p]: { self.peerRights[p] }")
					rights_val_bg = skin.myTrue if self.peerRights[p] else skin.myFalse
						
					rights_val_bg = ( skin.myTrue, skin.myBlack ) if self.peerRights[p] else ( skin.myFalse, skin.myWhite )		
					rights_val = tk.Label( 
						self.bFrameUp, 
						text = f"{ self.peerRights[p] }", 
						bg = rights_val_bg[0], 
						fg = rights_val_bg[1], 
						font = skin.provideFont('B') 
					)
					rights_val.grid( row = i, column = rghtsClmn, padx = 2, pady = 2, sticky = 'WE' )

				# Finally place bFrameUp on the grid
				self.bFrameUp.grid( row = 0, column = 0, sticky = 'WENS' )

		else:
			print(f"SelectedPeer len self.chosenPeerArr == 0" )

		self.selectedPeerGrid.grid( row = 0, column = 0, padx = 2, pady = 2, sticky = 'WENS' )
