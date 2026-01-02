#!/usr/bin/env python3

########################################
#### cls_Frm_Mesh_Rightslabels.py 	####
#### 	Version 20250712 	grid	####
########################################

import tkinter as tk
from tkinter import ttk
import myTheme as skin
from pubsub import pub 
from meshnet.cls_Frm_CanvasLabel import canvasLblFrm as clrLabel


class MeshRightsLabels( tk.Frame ):

	def __init__(
			self,
			master = None ,
			dimensions = [ 1000, 600 ]
		):

		super().__init__( master )

		self.master = master
		self.dimensions = dimensions

		self.configure( background = skin.myBlack )
		self.grid()

		self.chosenPeerName = "select peer"
		self.allPeerRights 	= []


		self.meshActionsGrid = tk.Frame( 
			self, 
			height = self.dimensions[0], 
			width = self.dimensions[1], 
			bg = skin.myBlack 
		)

		self.meshActions = [
			"incoming", 	# 0
			"routing",		# 1
			"local",		# 2
			"fileshare",	# 3
			"auto-accept"	# 4
		]

		pub.subscribe( self.chosenPeerListener, 'newPeerSelected' )	

		self.doLayOut()


	def chosenPeerListener( self, anyArgs ):
		print(f"MeshRightsLabels | chosenPeerListener - { anyArgs }")
		self.chosenPeerName = anyArgs[0]
		# Don't need anyArgs[1] here
		self.allPeerRights = anyArgs[2]
		self.doLayOut()

	
	def getRightsTuple( self, rightCommand ):
		# print(f"MeshRightsLabels | getRightsTuple --rightCommand: { rightCommand }")
		permIndex = self.meshActions.index(rightCommand)
		# print(f"MeshRightsLabels | getRightsTuple --permIndex: { permIndex }")

		retValArr = [ 
			[ 'disabled', skin.myFalse ], 
			[ 'disabled', skin.myFalse ] 
		]

		if len(self.allPeerRights) == 2:

			if permIndex == 4: 
				retValArr[0][0] = self.allPeerRights[0][permIndex][1]
				retValArr[1][0] = self.allPeerRights[1][permIndex-1][1]

			else:
				retValArr[0][0] = self.allPeerRights[0][permIndex][1]
				retValArr[1][0] = self.allPeerRights[1][permIndex][1]

		else:
			print(f"MeshRightsLabels | len(self.allPeerRights) NOT 2")

		# print(f"MeshRightsLabels | --retValTuple = { retValTuple }")

		if retValArr[0][0] == "enabled":
			retValArr[0][1] = skin.myLGreen

		if retValArr[1][0] == "enabled":
			retValArr[1][1] = skin.myLGreen

		return retValArr



	def doLayOut( self ):
		"""
			Meshnet actions buttons has 2 columns
			Actions are always relative to the chosen peer
			column 0 Always shown contains the labels of the actions
			column 1 (if peer selected) contains the 4 rights that the selected peer has for this device (display only)
		"""
		# Create grid with rights labels in column 0
		rightsLabelRow = 0
		for rightObj in self.meshActions:
			"""
			tdRightsLabel = tk.Label(
				self.meshActionsGrid,
				text 	= rightObj.upper(),
				font  	= skin.provideFont("B"),
				fg 		= skin.myBlack,
				bg 		= skin.myWhite
			)
			"""
			rObjPerms = self.getRightsTuple( rightObj )
			print(f"MeshRightsLabels | calling getRightsTuple('{rightObj}') result: { rObjPerms }")
			tdRightsLabel = clrLabel(
				self.meshActionsGrid,
				dimensions 	= [ 160, 25 ],
				colors 		= [ rObjPerms[0][1], rObjPerms[1][1] ], 
				text 		= rightObj.upper()
			)

			tdRightsLabel.grid( row = rightsLabelRow, column = 0 , pady = 1, padx = 2, sticky = 'WENS' )
			rightsLabelRow +=1


		"""

		self.colorlabel1 = clrLabel(
			self.meshActionsGrid,
			dimensions 	= [ 150, 20 ],
			colors 		= [ skin.myTrue, skin.myFalse ], 
			text 		= "incoming" 
		)
		self.colorlabel1.grid(  row = rightsLabelRow, column = 0, sticky = 'WENS' )
		"""

		# Finally draw the main grid
		self.meshActionsGrid.grid( row = 0, column = 0, sticky = 'WENS' )
		