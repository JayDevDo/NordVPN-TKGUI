#!/usr/bin/env python3

########################################
#### 	cls_Frm_CanvasLabel.py 		####
#### 	Version 20250716 	grid	####
########################################

import tkinter as tk
from tkinter import ttk
import myTheme as skin

# Canvas label with cutom gradient background (2 colors) and custom text

class canvasLblFrm( tk.Frame ):

	def __init__( 	self,
					master 		= None,
					dimensions 	= [ 200, 50 ],
					colors 		= ["#000000", "#FFFFFF"], 
					text 		= "No text provided in arguments" 
	):

		super().__init__( master )

		self.master = master
		self.dimensions = dimensions
		self.lblClrs = colors
		self.lblText = text
		self.configure( background = skin.myBlack )
		self.grid()

		self.endX1 		= self.dimensions[0] * 0.49

		print(f"canvasLblFrm | --dimensions: { self.dimensions } --colors: { self.lblClrs } --text: { self.lblText }")

		self.canvasLblFrmGrid = tk.Frame( 
			self, 
			width = self.dimensions[0], 
			height = self.dimensions[1], 
			bg = skin.myBlack 
		)

		# Define gradient
		canvasLabel = tk.Canvas( 
			self.canvasLblFrmGrid, 
			width 	= self.dimensions[0], 
			height 	= self.dimensions[1] 
		)

		# Iterate through the color and fill the rectangle with colors(r,g,0)
		canvasLabel.create_rectangle( 
			1,
			1,
			self.endX1,
			self.dimensions[1],
			fill = self.lblClrs[0]
		)

		canvasLabel.create_rectangle( 
			self.endX1,
			1,
			self.dimensions[0],
			self.dimensions[1] ,
			fill = self.lblClrs[1]
		)

		canvasLabel.create_text(
			int( self.dimensions[0] * 0.50 ),
			int( self.dimensions[1] * 0.55 ),
			text = self.lblText.upper(), 
			font = skin.provideFont('N'), 
			fill = skin.myDDBlue,
			anchor = 'center'
		)
		"""
		"""

		canvasLabel.grid( row = 0, column = 0, padx = 0, pady = 0, sticky = 'WENS' )
		self.canvasLblFrmGrid.grid( row = 0, column = 0, padx = 0, pady = 0, sticky = 'WENS' )

