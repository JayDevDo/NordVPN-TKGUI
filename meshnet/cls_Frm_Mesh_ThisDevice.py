#!/usr/bin/env python3

########################################
#### 	cls_Frm_Mesh_ThisDevice.py 	####
#### 	Version 20250702 	grid	####
########################################

import tkinter as tk
import myTheme as skin
import json
import nvpnPort as nvpnT

from myTable import TkTable as tableMaker

from idlelib.tooltip import Hovertip

from pubsub import pub


class ThisDevice( tk.Frame ):

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

		# print(f"ThisDevice| --dimensions: { self.dimensions } len deviceArr = { len( self.thisDevice ) }")

		self.thisDeviceGrid = tk.Frame( 
			self, 
			height = self.dimensions[0], 
			width = self.dimensions[1], 
			bg = skin.myBlack 
		)

		pub.subscribe( self.newPeerRightsListener, 'newPeerRights' )		

		self.doLayOut()


	def newPeerRightsListener( self, anyArgs ):
		# print(f"ThisDevice | newPeerRightsListener - { anyArgs }")
		self.peerRights = anyArgs[0]
		self.chosenPeerName = anyArgs[1]
		# print(f"ThisDevice | newPeerRightsListener --self.peerRights: { self.peerRights } --self.chosenPeerName: { self.chosenPeerName }")
		self.doLayOut()



	def createThisDevicePanel( self, parentFrame, thisDevArr ):
		if len( thisDevArr ) > 0:
			tDev = thisDevArr
			# print(f"ThisDevice | createThisDevicePanel. tDev = { json.dumps( tDev, indent=2 ) }")
			rowCounter = 1
			hdrLblBG = skin.myLRed
			pubMsg = ["status: disconnected",""]

			# get device connection status
			self.connStatArray = nvpnT.getNvpnItem( 'status' )
			# print(f"ThisDevice | createThisDevicePanel | { self.connStatArray }")
			if self.connStatArray[0][1].upper() == "CONNECTED":
				hdrLblBG = skin.myLGreen
				pubMsg[0] = "status: connected.\n"

			theHdrLabel = tk.Label( 
				parentFrame, 
				text = self.connStatArray[0][0].upper(), 
				bg = skin.myBlack, 
				fg = skin.myNYellow, 
				font = skin.provideFont('B') 
			)
			theHdrLabel.grid( row = rowCounter, column = 0, padx = 2, pady = 2, sticky = "WE")

			theHdrValue = tk.Label( 
				parentFrame, 
				text = self.connStatArray[0][1].upper(), 
				bg = hdrLblBG, 
				fg = skin.myBlack, 
				font = skin.provideFont('B') 
			)
			theHdrValue.grid( row = rowCounter, column = 1, padx = 2, pady = 2, sticky = "WE")

			rowCounter += 1

			for entry in tDev:
				key = entry
				value = tDev[ entry ]
				# print(f"ThisDevice | createThisDevicePanel - clmn { rowCounter }: key = { key } value = { value }")

				theLabel = tk.Label( 
					parentFrame, 					
					text = key.upper(), 
					bg = skin.myBlack, 
					fg = skin.myNYellow, 
					font = skin.provideFont('B') 
				)
				theLabel.grid( row = rowCounter, column = 0, padx = 2, pady = 2, sticky = "WE" )

				valTxt = value
				if "Key" in key:
					valTxt = f"{ value[0:12] } ..."

				elif "Hostname" in key:
					pubMsg[1] = f"ThisDevice Hostname of this Device: {value}"
					pbmsg = f"{pubMsg[0]}: {pubMsg[1]}"
					pub.sendMessage( "myStatusBarUpdate", anyArgs = pbmsg )

				theValue = tk.Label( 
					parentFrame, 
					text = valTxt, 
					bg = skin.myLBlue, 
					fg = skin.myBlack, 
					font = skin.provideFont('B') 
				)
				theValue.grid( row = rowCounter, column = 1, padx = 2, pady = 2, sticky = "WE" )

				rowCounter += 1


			if rowCounter > 4:

				if len( self.peerRights ) > 0:
					
					rightsCounter = 0
					# print(f"jdon dumps peerRights { json.dumps( self.peerRights, indent = 2) }")

					for r,v in self.peerRights[0] :

						rightsCounter += 1
						bttntxt  = "change to "

						if ( r == "Accept Fileshare Automatically" ):							
							if v == "enabled":
								bttntxt += "disable"
								rightsClr = skin.myLGreen
							elif v == "disabled":
								bttntxt += "enable"
								rightsClr = skin.myLRed
						else:
							if v == "enabled":
								bttntxt += "Deny"
								rightsClr = skin.myLGreen

							elif v == "disabled":
								bttntxt += "Allow"
								rightsClr = skin.myLRed

						# print(f"ThisDevice | createThisDevicePanel self.peerRights r={r} \nv={v} \nbttntxt={bttntxt} \nrightsClr={rightsClr}")
						rghtsLblVal = tk.Label(
							parentFrame, 
							text = bttntxt, 
							bg = rightsClr, 
							fg = skin.myBlack, 
							font = skin.provideFont('B') 
						)
						rghtsLblVal.grid( row = rightsCounter, column = 2, padx = 2, pady = 2, sticky = 'WE')

						rghtsLblValToolTip = Hovertip( rghtsLblVal, f"Click to change the {r} setting\non this device to '{ bttntxt.split(' ')[-1] }'\nfor { self.chosenPeerName }")

						"""
						rghtsLblTxt = tk.Label(
							parentFrame, 
							text = r, 
							bg = rightsClr, 
							fg = skin.myBlack, 
							font = skin.provideFont('N') 
						)
						rghtsLblTxt.grid( row = rightsCounter, column = 3, sticky = 'WE')
						"""



	def doLayOut( self ):

		self.createThisDevicePanel( self.thisDeviceGrid, self.thisDevice )


		# Finally draw the main grid
		self.thisDeviceGrid.grid( row = 0, column = 0, padx = 2, pady = 2, sticky = 'WENS' )

