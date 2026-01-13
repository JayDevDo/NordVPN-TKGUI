#!/usr/bin/env python3

########################################
#### 	cls_Frm_Mesh_ThisDevice.py 	####
#### 		Version 20260109 		####
########################################

import tkinter as tk
import myTheme as skin
import json
import nvpnPort as nvpnT

from myTable import TkTable as tableMaker

from idlelib.tooltip import Hovertip

from pubsub import pub

#==============================================================================
class ThisDevice( tk.Frame ):

	#--------------------------------------------------------------------------
	def __init__(
			self,
			master = None,
			dimensions = [ 1000, 600 ],
			deviceArr = []
		):

		super().__init__( master )

		self.master = master
		self.configure( background = skin.myBlack )
		self.grid()
		self.dimensions = dimensions
		self.thisDevice = deviceArr
		self.peerRights = []
		self.showAttrs = ["Status","Hostname","Nickname","IP","Public Key","OS","Distribution"]

		# print(f"ThisDevice| --dimensions: { self.dimensions } len deviceArr = { len( self.thisDevice ) }")

		self.thisDeviceGrid = tk.Frame( 
			self, 
			height = self.dimensions[0], 
			width = self.dimensions[1], 
			bg = skin.myBlack 
		)

		pub.subscribe( self.newPeerRightsListener, 'newPeerRights' )		

		self.doLayOut()


	#--------------------------------------------------------------------------
	def newPeerRightsListener( self, anyArgs ):
		# print(f"ThisDevice | newPeerRightsListener - { anyArgs }")
		self.peerRights = anyArgs[0]
		self.chosenPeerName = anyArgs[1]
		self.doLayOut()

	#--------------------------------------------------------------------------
	def clearExistingFrame( self ):
		try:
			if self.td_FrameUp.grid_info():
				self.td_FrameUp.grid_forget()

		except Exception as e:
			print(f"ThisDevice.clearExistingFrame ! Exception: {e}")

	#--------------------------------------------------------------------------
	def doLayOut( self ):
		self.clearExistingFrame()
		self.td_FrameUp = tk.Frame( self.thisDeviceGrid, bg = skin.myBlack )

		try:
			labelClmn = 0 
			valueClmn = 1
			rghtsClmn = 2 
			thisDeviceAttrs = [ pAttr for pAttr in self.thisDevice if pAttr in self.showAttrs ]
			thisDeviceRights = [ tdRight for tdRight in self.peerRights ] #  if 'Allow' in tdRight
			# print(f"ThisDevice.doLayOut | --START --self.peerRights: { json.dumps( self.peerRights, indent = 4 )  }")
			# print(f"ThisDevice.doLayOut | --START --thisDeviceAttrs: { json.dumps( thisDeviceAttrs, indent = 4 )  }")
			# print(f"ThisDevice.doLayOut | --START --thisDeviceRights: { json.dumps( thisDeviceRights, indent = 4 )  }")

			if len( thisDeviceAttrs ) > 0:
				#print(f"ThisDevice.doLayOut | --self.thisDevice: {self.thisDevice}\n")
				statusLblBG = skin.myDRed
				if "Status" in thisDeviceAttrs:
					# print(f"ThisDevice.doLayOut | --Status was present")
					statusLblBG = skin.myLGreen if self.thisDevice['Status'].lower() == "connected" else skin.myDRed
				else:
					# print(f"ThisDevice.doLayOut | --Status NOT present")
					self.thisDevice['Status'] = "disconnected" 
					thisDeviceAttrs = [ pAttr for pAttr in self.thisDevice if pAttr in self.showAttrs ]

				# print(f"ThisDevice.doLayOut | --thisDeviceAttrs: { thisDeviceAttrs }")

				for i,a in enumerate(self.showAttrs):
					#print(f"ThisDevice.doLayOut | --i: {i} --a: {a} --self.thisDevice[a]: { self.thisDevice[a] }")

					attr_lbl = tk.Label( 
						self.td_FrameUp, 
						text = f"{ a.upper() }", 
						bg = skin.myBlack, 
						fg = skin.myDBlue, 
						font = skin.provideFont('B') 
					)

					attr_val_txt = f"{self.thisDevice[a][0:10]}..." if a == "Public Key" else self.thisDevice[a]
					attr_val = tk.Label( 
						self.td_FrameUp, 
						text = f"{ attr_val_txt } ", 
						bg = skin.myDBlue, 
						fg = skin.myBlack, 
						font = skin.provideFont('B') 
					)

					attr_lbl.grid( row = i, column = labelClmn, padx = 2, pady = 2, sticky = 'WE' )
					attr_val.grid( row = i, column = valueClmn, padx = 2, pady = 2, sticky = 'WE' )

			if len( thisDeviceRights ) > 0:

				for i,p in enumerate(self.peerRights[0]):
					# print(f"ThisDevice.doLayOut | --self.peerRights[0][p]: { self.peerRights[0][p] }")

					rights_val_bg = ( skin.myTrue, skin.myBlack ) if self.peerRights[0][p] else ( skin.myFalse, skin.myWhite )
					rights_val = tk.Label( 
						self.td_FrameUp, 
						text = f"{ self.peerRights[0][p] }", 
						bg = rights_val_bg[0], 
						fg = rights_val_bg[1], 
						font = skin.provideFont('B') 
					)
					rights_val.grid( row = i, column = rghtsClmn, padx = 2, pady = 2, sticky = 'WE' )
					# rights_valToolTip = Hovertip( rights_val, f"Click to change the {r} setting\non this device to '{ bttntxt.split(' ')[-1] }'\nfor { self.chosenPeerName }")


		except Exception as e:
			print(f"ThisDevice.doLayOut ! Exception: {e}")

		finally:
			# Finally place td_FrameUp on the grid
			self.td_FrameUp.grid( row = 0, column = 0, sticky = 'WENS' )
			# Finally draw the main grid
			self.thisDeviceGrid.grid( row = 0, column = 0, padx = 2, pady = 2, sticky = 'WENS' )

