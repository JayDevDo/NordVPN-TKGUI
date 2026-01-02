#!/usr/bin/env python3

########################################
#### cls_Frm_Mesh_LocalDevices.py 	####
#### 	Version 20250624 	grid	####
########################################

import tkinter as tk
import json
import myTheme as skin
import meshnet.nvpnMeshPort as meshPort
from pubsub import pub
from idlelib.tooltip import Hovertip


class SelectedPeer( tk.Frame ):

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



	def thisDeviceListener( self, anyArgs ):
		# pub.sendMessage( "thisDeviceUpdate", anyArgs=[ self.meshDevices[0]['Hostname'] ] )
		# print(f"SelectedPeer | thisDeviceListener - { anyArgs }")
		self.thisDeviceName = anyArgs[0]


	def peerSelectionListener( self, anyArgs ):
		# print(f"SelectedPeer | peerSelectionListener - { anyArgs }")
		self.chosenPeerName = anyArgs[0]
		self.chosenPeerArr 	= anyArgs[1]
		self.peerRights = anyArgs[2][1]
		self.doLayOut()


	def getBGColor(self, value):
		# print(f"SelectedPeer | getBGColor --value: {value}")
		if value.lower() == "enabled":
			return skin.myTrue
		else:
			return skin.myFalse 


	def doLayOut( self ):
		self.bFrameUp 	= tk.Frame(	self.selectedPeerGrid, bg = skin.myBlack )

		if len( self.chosenPeerArr ) > 0:
			# print(f"SelectedPeer start of doLayOut")
			
			try:
				self.bFrameUp.grid_info()
				self.bFrameUp.grid_forget()

				# print(f"SelectedPeer | updatePeerInfoFrame - len self.chosenPeerArr = { len(self.chosenPeerArr) }")
				# print(f"SelectedPeer | len self.peerRights  = { len( self.peerRights ) }")

			except Exception as e:
				print(f"SelectedPeer | updatePeerInfoFrame Exception = {e}")

			finally:

				statusLblBG  = skin.myDRed

				if self.chosenPeerArr['Status'].lower() == "connected":
					statusLblBG  = skin.myLGreen


				if len( self.peerRights ) == 4:
					rghtsClmn = 0 
					labelClmn = 2 
					valueClmn = 1
				else:
					rghtsClmn = 2 
					labelClmn = 0 
					valueClmn = 1

				if True:
					# bFrameUp labels:
					statusLbl = tk.Label( 
						self.bFrameUp, 
						text = "STATUS: ", 
						bg = skin.myBlack, 
						fg = skin.myDBlue, 
						font = skin.provideFont('B') 
					)

					statusTxt = tk.Label( 
						self.bFrameUp, 
						text = self.chosenPeerArr['Status'], 
						bg = statusLblBG, 
						fg = skin.myBlack, 
						font = skin.provideFont('B') 
					)

					rightsLbl1 = tk.Label( 
						self.bFrameUp, 
						text = self.peerRights[0][1], 
						bg = self.getBGColor(self.peerRights[0][1]), 
						fg = skin.myDBlue, 
						font = skin.provideFont('B') 
					)

					rightsLbl1.grid( row = 0, column = rghtsClmn, padx = 2, pady = 2, sticky = 'WE' )
					rightsLbl1ToolTip = Hovertip( rightsLbl1, f"On { self.chosenPeerName } \nchange {self.peerRights[0][0]} \nfor { self.thisDeviceName }")
					statusLbl.grid( row = 0, column = labelClmn, padx = 2, pady = 2, sticky = 'WE' )
					statusTxt.grid( row = 0, column = valueClmn, padx = 2, pady = 2, sticky = 'WE' )

					hostNameLbl = tk.Label( 
						self.bFrameUp, 
						text = "HOSTNAME: ", 
						bg = skin.myBlack, 
						fg = skin.myDBlue, 
						font = skin.provideFont('B') 
					)

					hostNameTxt = tk.Label( 
						self.bFrameUp, 
						text = self.chosenPeerArr['Hostname'], 
						bg = skin.myDBlue, 
						fg = skin.myBlack, 
						font = skin.provideFont('B') 
					)

					rightsLbl2 = tk.Label( 
						self.bFrameUp, 
						text = self.peerRights[1][1], 
						bg = self.getBGColor(self.peerRights[1][1]), 
						fg = skin.myDBlue, 
						font = skin.provideFont('B') 
					)

					rightsLbl2ToolTip = Hovertip( rightsLbl2, f"On { self.chosenPeerName } \nchange {self.peerRights[1][0]} \nfor { self.thisDeviceName }")
					rightsLbl2.grid(  row = 1, column = rghtsClmn, padx = 2, pady = 2, sticky = 'WE' )
					hostNameLbl.grid( row = 1, column = labelClmn, padx = 2, pady = 2, sticky = 'WE' )
					hostNameTxt.grid( row = 1, column = valueClmn, padx = 2, pady = 2, sticky = 'WE' )


					nickNameLbl = tk.Label( 
						self.bFrameUp, 
						text = "NICKNAME: ", 
						bg = skin.myBlack, 
						fg = skin.myDBlue, 
						font = skin.provideFont('B') 
					)

					nickNameTxt = tk.Label( 
						self.bFrameUp, 
						text = self.chosenPeerArr['Nickname'], 
						bg = skin.myDBlue, 
						fg = skin.myBlack, 
						font = skin.provideFont('B') 
					)

					rightsLbl3 = tk.Label( 
						self.bFrameUp, 
						text = self.peerRights[2][1], 
						bg = self.getBGColor(self.peerRights[2][1]), 
						fg = skin.myDBlue, 
						font = skin.provideFont('B') 
					)

					rightsLbl3ToolTip = Hovertip( rightsLbl3, f"On { self.chosenPeerName } \nchange {self.peerRights[2][0]} \nfor { self.thisDeviceName }")
					rightsLbl3.grid(  row = 2, column = rghtsClmn, padx = 2, pady = 2, sticky = 'WE' )
					nickNameLbl.grid( row = 2, column = labelClmn, padx = 2, pady = 2, sticky = 'WE' )
					nickNameTxt.grid( row = 2, column = valueClmn, padx = 2, pady = 2, sticky = 'WE' )

					ipLbl = tk.Label( 
						self.bFrameUp, 
						text = "IP: ", 
						bg = skin.myBlack, 
						fg = skin.myDBlue, 
						font = skin.provideFont('B') 
					)
					
					ipTxt = tk.Label( 
						self.bFrameUp, 
						text = self.chosenPeerArr['IP'], 
						bg = skin.myDBlue, 
						fg = skin.myBlack, 
						font = skin.provideFont('B') 
					)

					rightsLbl4 = tk.Label( 
						self.bFrameUp, 
						text = self.peerRights[3][1], 
						bg = self.getBGColor(self.peerRights[3][1]), 
						fg = skin.myDBlue, 
						font = skin.provideFont('B') 
					)

					rightsLbl4ToolTip = Hovertip( rightsLbl4, f"On { self.chosenPeerName } \nchange {self.peerRights[3][0]} \nfor { self.thisDeviceName }")
					rightsLbl4.grid( row = 3, column = rghtsClmn, padx = 2, pady = 2, sticky = 'WE' )
					ipLbl.grid( row = 3, column = labelClmn, padx = 2, pady = 2, sticky = 'WE' )
					ipTxt.grid( row = 3, column = valueClmn, padx = 2, pady = 2, sticky = 'WE' )


					pubKeyLbl = tk.Label( 
						self.bFrameUp, 
						text = "PUBLIC KEY: ", 
						bg = skin.myBlack, 
						fg = skin.myDBlue, 
						font = skin.provideFont('B') 
					)

					pubKeyTxt = tk.Label( 
						self.bFrameUp, 
						text = f"{ self.chosenPeerArr['Public Key'][0:12]} ..." , 
						bg = skin.myDBlue, 
						fg = skin.myBlack, 
						font = skin.provideFont('B') 
					)
					pubKeyLbl.grid( row = 4, column = labelClmn, padx = 2, pady = 2, sticky = 'WE' )
					pubKeyTxt.grid( row = 4, column = valueClmn, padx = 2, pady = 2, sticky = 'WE' )

					osLbl = tk.Label( 
						self.bFrameUp, 
						text = "OS: ", 
						bg = skin.myBlack, 
						fg = skin.myDBlue, 
						font = skin.provideFont('B') 
					)

					osTxt = tk.Label( 
						self.bFrameUp, 
						text = self.chosenPeerArr['OS'], 
						bg = skin.myDBlue, 
						fg = skin.myBlack, 
						font = skin.provideFont('B') 
					)
					osLbl.grid( row = 5, column = labelClmn, padx = 2, pady = 2, sticky = 'WE' )
					osTxt.grid( row = 5, column = valueClmn, padx = 2, pady = 2, sticky = 'WE' )
					

					distriLbl = tk.Label( 
						self.bFrameUp, 
						text = "DISTRIBUTION: ", 
						bg = skin.myBlack, 
						fg = skin.myDBlue, 
						font = skin.provideFont('B') 
					)

					distriTxt = tk.Label( 
						self.bFrameUp, 
						text = self.chosenPeerArr['Distribution'], 
						bg = skin.myDBlue, 
						fg = skin.myBlack, 
						font = skin.provideFont('B') 
					)
					distriLbl.grid( row = 6, column = labelClmn, padx = 2, pady = 2, sticky = 'WE' )
					distriTxt.grid( row = 6, column = valueClmn, padx = 2, pady = 2, sticky = 'WE' )

					self.bFrameUp.grid( row = 0, column = 0, sticky = 'WENS' )


		else:
			print(f"SelectedPeer len self.chosenPeerArr == 0" )

		self.selectedPeerGrid.grid( row = 0, column = 0, padx = 2, pady = 2, sticky = 'WENS' )
