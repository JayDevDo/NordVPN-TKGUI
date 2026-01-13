#!/usr/bin/env python3

########################################
#### 	cls_tabFrm_Account.py 		####
#### 	Version 20250624 	grid	####
########################################

import tkinter as tk
from tkinter import ttk
import myTheme as skin
import nvpnPort as nvpnT

from pubsub import pub

from cls_Frm_AccStatus 	import AccountStatusFrame
from cls_Frm_AccActions import AccountActionsFrame
from cls_Frm_ConnStatus import ConnStatusFrame
from cls_Frm_Services 	import NordVPNServices as NvpnServicesFrm 


class TabAccount( tk.Frame ):

	def __init__( 
			self, 
			master = None, 
			dimensions = [ 900, 750 ]
		):
	
		super().__init__(master)
		print("AA"*40)	
		print(f"TabAccount | --dimensions: {dimensions}")

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


	def addConnStatus( self ):
		print(f"TabAccount | addConnStatus: ")
		try:
			self.tabAccActConnFrame.grid_info()
			self.tabAccActConnFrame.grid_forget()

		except Exception as e:
			print(f"TabAccount | addConnStatus: Exception = { e }")

		finally:
			self.tabAccActConnFrame = ConnStatusFrame( 
				self.tabAccGridFrame,
				dimensions = [  int( self.tabWidth * 0.45 ), int( self.tabHeight * 0.24 ) ]
			)
			self.tabAccActConnFrame.grid( row = 1, column = 0, columnspan = 1, sticky = 'wens' )


	def doLayout( self ):
		# print(f"NordVPNServices -tabAccTnnlDataLen: { self.tabAccTnnlDataLen }")
		# Frames that go into 'tabAccGridFrame' 

		# to display 'tabAccTnnlData'
		self.tabAccDataFrame = AccountStatusFrame( 
			self.tabAccGridFrame,
			accDataArr = self.tabAccTnnlData, 
			dimensions = [ int( self.tabWidth * 0.65 ), int( self.tabHeight * 0.24 )]
		)
		self.tabAccDataFrame.grid( row = 0, column = 0, columnspan = 2, sticky = 'wens' )

		# to display 'Account actions log-in, log-out, start nordvpnd service'
		self.tabAccActionsFrame = AccountActionsFrame( 
			self.tabAccGridFrame, 
			dimensions = [ int( self.tabWidth * 0.33 ), int( self.tabHeight * 0.24 ) ]
		)
		self.tabAccActionsFrame.grid( row = 0, column = 2, columnspan = 1, sticky = 'wens' ) 

		# to display the active connection status
		self.addConnStatus()
		"""
			self.tabAccActConnFrame = ConnStatusFrame( 
				self.tabAccGridFrame,
				dimensions = [  int( self.tabWidth * 0.45 ), int( self.tabHeight * 0.24 ) ]
			)
			self.tabAccActConnFrame.grid( row = 1, column = 0, columnspan = 1, sticky = 'wens' )
		"""

		# to display the active nordvpn services and nordvpn wersion
		self.tabAccSrvcsTblFrm = NvpnServicesFrm( 
			self.tabAccGridFrame,
			dimensions = [ int( self.tabWidth * 0.45 ), int( self.tabHeight * 0.24 )]
		)
		self.tabAccSrvcsTblFrm.grid( row = 1, column = 1, columnspan = 2, sticky = 'wens' )


		# Finally pack the grid-container
		self.tabAccGridFrame.grid( row = 0, column = 0, sticky = 'wens' )
