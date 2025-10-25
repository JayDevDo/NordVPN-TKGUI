#!/usr/bin/env python3

########################################
#### 	cls_Frm_ConnStatus.py 		####
#### 	Version 20250506 	grid	####
########################################

import tkinter as tk
from tkinter import ttk
import myTheme as skin
import nvpnPort as nvpnT
from myTable import TkTable as connStatusTbl
from pubsub import pub

class ConnStatusFrame( tk.Frame ):

	def __init__( 
			self, 
			master = None, 
			dimensions = [ 400, 400 ] 
		):
	
		super().__init__(master)
	
		self.master = master
		self.configure( background = skin.myBlack )
		self.grid()
		self.dimensions = dimensions
		print(f"ConnStatusFrame called with dimensions: { dimensions }")

		self.connStatArray 	= []
		self.connStatArrSize = 0 
		self.csLblBGClr = skin.myBlack
				
		self.tabConnStatGridFrame = tk.Frame(
			self, 
			bg = skin.myBlack,
			width 	= int( self.dimensions[0] * 0.975 ),
			height 	= int( self.dimensions[1] * 0.975 ), 
			padx = 2, 
			pady = 2
		)

		self.refreshData()


	def refreshData( self ):
		self.connStatArray 		= nvpnT.getNvpnItem( 'status' )
		self.connStatArrSize 	= len( self.connStatArray ) 
		print(f"ConnStatusFrame.refreshData -connStatArrSize: { self.connStatArrSize }\n\t{ str( self.connStatArray ) }")
		if nvpnT.getConnStatus():
			pubMsg = f"{ self.connStatArray[0][1] } - { self.connStatArray[1][1] } - { self.connStatArray[-1][1] }"  
			pub.sendMessage( "myStatusBarUpdate", anyArgs=f"Connection status: { pubMsg }" )
		else:
			print(f"nvpnT.getRatingResult() = {nvpnT.getRatingResult()}")
			pubMsg = f"{ self.connStatArray[0][1] }" + f"{ nvpnT.getRatingResult() }"

		self.doLayout()


	def doLayout( self ):
		pubMsg = ""
		if nvpnT.getConnStatus():
			self.csLblBGClr = skin.myTrue
		else:
			self.csLblBGClr = skin.myFalse

		self.connStatHeader = tk.Label( 
			self.tabConnStatGridFrame, 
			text = "Connection Status", 
			bg = self.csLblBGClr,
			fg = skin.myBlack,
			font = skin.provideFont(20)
		)

		self.frmConnStatTbl = connStatusTbl(
			self.tabConnStatGridFrame,
			title 		= "", 
			colHeaders 	= [], 
			data 		= self.connStatArray, 
			dimensions 	= [ self.dimensions[0] , self.dimensions[1] ]
		)

		self.refreshImage = skin.provideImage('refresh')
		self.btn_Refresh = tk.Button(
			self.tabConnStatGridFrame,
			text = "Refresh status", 
			command = self.refreshData,
			font = skin.provideFont("B"), 
			background = skin.myBttnBG, 
			fg = skin.myBttnFG, 
			padx = 10,
			pady = 10,
			image = self.refreshImage,
			compound = 'left'
		)

		self.connStatHeader.grid( row = 0, 	column = 0, sticky = 'WENS' )
		self.frmConnStatTbl.grid( row = 1, 	column = 0, sticky = 'WENS'	)	
		self.btn_Refresh.grid( 	row = 2, 	column = 0, sticky = 'WENS'	)	

		self.tabConnStatGridFrame.grid( row = 0, column = 0)
