#!/usr/bin/env python3

############################################
#### 		cls_tabFrm_Account.py 		####
#### 		Version 241228_2000 grid	####
############################################


import tkinter as tk
from tkinter import ttk

import myTheme as skin
import nvpnPort as nvpnT

class TabAccount( tk.Frame ):

	def __init__( 
			self, 
			master = None, 
			dimensions = [ 900, 750 ]
		):
	
		super().__init__(master)

		print("AA"*40)	
		print(f"cls_tabFrm_Account.TabAccount: --dimensions: {dimensions}")

		self.master = master
		self.configure( background = skin.myBlack )
		self.configure( width = dimensions[0], height = dimensions[1] )
		self.grid()

		self.dimensions = dimensions

		self.tabWidth  = int( self.dimensions[0] * 0.975 )
		self.tabHeight = int( self.dimensions[1] * 0.975 )

		self.tabAccTnnlData 	= nvpnT.getNvpnItem( 'account' )
		self.tabAccTnnlDataLen 	= len( self.tabAccTnnlData ) 

		self.tabAccDataGrid = []
		self.tabAccBttnGrid = []

		# The Frame that will act as a grid-sizer of 'TabAccount'
		self.tabAccGridFrame = tk.Frame( 
			self, 
			bg 		= skin.myBlack, 
			pady 	= 10, 
			padx 	= 10,
			width 	= self.tabWidth,
			height 	= self.tabHeight
		)

		self.doLayout()


	def doLayout( self ):

		# print(f"NordVPNServices -tabAccTnnlDataLen: { self.tabAccTnnlDataLen }")

		# Frames that go into 'tabAccGridFrame' 

		# to display 'tabAccTnnlData'
		from cls_Frm_AccStatus import AccountStatusFrame
		self.tabAccDataFrame = AccountStatusFrame( 
			self.tabAccGridFrame,
			accDataArr = self.tabAccTnnlData, 
			dimensions = [ int( self.tabWidth * 0.95 ), int( self.tabHeight * 0.32 )]
		)
		self.tabAccDataFrame.grid( row = 0, column = 0, sticky = 'nw' )


		# to display 'Account actions log-in, log-out, start nordvpnd service'
		from cls_Frm_AccActions import AccountActionsFrame
		self.tabAccActionsFrame = AccountActionsFrame( 
			self.tabAccGridFrame, 
			dimensions = [ int( self.tabWidth * 0.45 ), int( self.tabHeight * 0.25 ) ]
		)
		self.tabAccActionsFrame.grid( row = 0, column = 1, sticky = 'ne' ) 
		#, sticky = 'WENS'


		# to display the active nordvpn services and nordvpn wersion
		from cls_Frm_Services import NordVPNServices as NvpnServicesFrm 
		self.tabAccSrvcsTblFrm = NvpnServicesFrm( 
			self.tabAccGridFrame,
			dimensions = [ int( self.tabWidth * 0.45 ), int( self.tabHeight * 0.33 )]
		)
		self.tabAccSrvcsTblFrm.grid( row = 2, column = 1, sticky = 'n' )
		# , sticky = 'WE'

		# to display the active connection status
		from cls_Frm_ConnStatus import ConnStatusFrame
		self.tabAccActConnFrame = ConnStatusFrame( 
			self.tabAccGridFrame,
			dimensions = [  int( self.tabWidth * 0.45 ), int( self.tabHeight * 0.25 ) ]
		)
		self.tabAccActConnFrame.grid( row = 2, column = 0, sticky = 'sw' )
		# , sticky = 'WENS'


		# Finally pack the grid-container
		self.tabAccGridFrame.grid( row = 0, column = 0 )
