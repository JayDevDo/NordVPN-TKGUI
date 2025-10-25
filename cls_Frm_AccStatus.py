#!/usr/bin/env python3

############################################
#### 		cls_Frm_AccStatus.py 		####
#### 		Version 20250506 	grid	####
############################################

import tkinter as tk
import json

import myTheme as skin
from myTable import TkTable as AccStatTbl

class AccountStatusFrame( tk.Frame ):

	def __init__( 
			self, 
			master = None, 
			accDataArr = [ ( "AccountInfo", ) ], 
			dimensions = [ 600, 400 ] 	
		):

		super().__init__( master )

		self.master = master
		self.configure( background = skin.myBlack )
		self.grid()
		
		# print(f"AccountStatusFrame called with\n--dimensions: { dimensions }\n--accDataArr: { json.dumps( accDataArr, indent=4) }")
		self.accStatTnnlData = accDataArr

		self.accStatFrmGrid = tk.Frame(
			self,
			bg 		= skin.myBlack,
			padx 	= 10,
			pady 	= 10,
			width 	= int(dimensions[0] * 0.95 )
		)

		passOnData = []
		if ( len( self.accStatTnnlData ) == 1 ):
			passOnData = self.accStatTnnlData
		elif( len( self.accStatTnnlData ) == 0 ):
			passOnData = ["No data"]
		else:
			passOnData = self.accStatTnnlData[1:]

		# to display 'tabAccTnnlData'
		self.tabAccStatusFrm = AccStatTbl(
			self.accStatFrmGrid,
			title 		= "Nord VPN Account",
			colHeaders 	= [],
			data 		= passOnData,
			dimensions 	= [ max( dimensions[0], 600 ), min( dimensions[0], 400 ) ]		
		)

		self.tabAccStatusFrm.grid( row = 0, column = 0 )
		self.accStatFrmGrid.grid(  row = 0, column = 0 )

