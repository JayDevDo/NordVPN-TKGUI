#!/usr/bin/env python3

########################################
#### 	cls_Frm_StatusBar.py 		####
#### 	Version 20250628 	grid	####
########################################

import tkinter as tk
from datetime import datetime
from pubsub import pub
import myTheme as skin

class MyStatusBar( tk.Frame ):

	def __init__( 
			self, 
			master = None, 
			dimensions = [ 1000, 120 ] 
		):
	
		super().__init__( master )
	
		# print(f"MyStatusBar called with dimensions: { dimensions }")

		self.master = master
		self.configure( background = skin.myBlack )
		self.grid()
		self.dimensions = dimensions

		self.stBarMainGrid = tk.Frame( 
			self, 
			width = self.dimensions[0], 
			height = self.dimensions[1], 
			padx = 1, 
			pady = 1, 
			bg = skin.myBlack 
		)

		self.stBarText = [ "statusBar time", "statusBar text"]

		self.stHdr = tk.Label( 
			self.stBarMainGrid, 
			text = self.stBarText[0].upper(),
			bg = skin.myWhite, 
			fg = skin.myBlack, 
			font = skin.provideFont('N')
		)

		self.stTxt = tk.Label( 
			self.stBarMainGrid, 
			text = self.stBarText[1],
			bg = skin.myBlack, 
			fg = skin.myWhite, 
			font = skin.provideFont('N')
		)

		self.stHdr.grid( row = 0, column = 0, sticky = 'WE' )
		self.stTxt.grid( row = 0, column = 1, sticky = 'WE' )

		pub.subscribe( self.stBarListener, 'myStatusBarUpdate' )
		self.doLayOut()


	def stBarListener( self, anyArgs="MystatusBar update default text" ):
		print(f"MyStatusBar stBarListener: anyArgs: { anyArgs } self.dimensions={self.dimensions}")
		dt = datetime.now()
		self.stBarText[0] = str(dt).split('.')[0] 
		self.stBarText[1] = ":\t" + anyArgs
		self.doLayOut()



	def doLayOut(self):
		self.stHdr.config( text = self.stBarText[0] )
		self.stTxt.config( text = self.stBarText[1] )
		self.stBarMainGrid.grid( row = 0, column = 0, sticky = 'WES' )
