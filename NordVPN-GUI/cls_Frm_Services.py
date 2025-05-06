#!/usr/bin/env python3

########################################
#### 	cls_Frm_Services.py 		####
#### 	Version 20250506 	grid	####
########################################

import tkinter as tk
import os
import psutil
import json 

import myTheme as skin
import nvpnPort as nvpnT

from myTable import TkTable as myTableFrm 

def nordServicesArr():
	tmp_prgInfoArr = []
	for p in psutil.process_iter( [ "pid", "name", "cmdline", "status" ] ):
		prcsNm = p.info["name"]

		if prcsNm.lower() == "nordvpnd":
			print(f"cls_Frm_Services.nordServicesArr| found NORDVPND { p.info['status'] } as { p.info['pid'] }-{ p.info['cmdline'] } " )
			tmp_prgInfoArr.append( [ str(p.pid), prcsNm, True ] )

		elif prcsNm.lower() == "norduserd":
			print(f"cls_Frm_Services.nordServicesArr| found NORDUSERD { p.info['status'] } as { p.info['pid'] }-{ p.info['cmdline'] } " )
			tmp_prgInfoArr.append( [ str(p.pid), prcsNm, True ] )

		elif ( "nord" in prcsNm.lower() ):
			tmp_prgInfoArr.append( [ str(p.pid), prcsNm, False ] )

	# End of: for p in psutil.process_iter:
	return tmp_prgInfoArr



class NordVPNServices( tk.Frame ):

	def __init__( 
			self, 
			master = None , 
			dimensions = [ 200, 200 ]
		):
	
		super().__init__( master )
	
		self.master = master
		self.grid()
		self.configure( background = skin.myBlack )

		print("SERVICES\t"*8)	
		print(f"cls_Frm_Services.NordVPNServices| --dimensions: { dimensions }")
		self.nvpnVersion = nvpnT.getNvpnItem('version')[1].split(':')[1].strip()

		print(f"NordVPNServices| --self.nvpnVersion: { json.dumps( self.nvpnVersion, indent = 4 ) }" )

		self.nvpnSrvcsFrmGrid = tk.Frame( 
			self, 
			bg = skin.myBlack, 
			width  = int( dimensions[0]*0.95), 
			height = int( dimensions[1]*0.95)
		)

		self.nvpnSrvcsTable = myTableFrm(
			self.nvpnSrvcsFrmGrid,
			title 		= "NVPN Services", 
			colHeaders 	= ["pid","name","user"],
			data 		= nordServicesArr() ,
			dimensions 	= [ int( dimensions[0]*0.95), int( dimensions[1]*0.95) ] )
		self.nvpnSrvcsTable.grid( row = 0, column = 0, sticky = 'wens' )

		appDirStr = str(os.path.dirname(__file__)) 

		self.nvpnVersionLbl = tk.Label(
			self.nvpnSrvcsFrmGrid,
			text = f"{self.nvpnVersion}\nApp dir: '{appDirStr}'", 
			bg = skin.myBlack,
			fg = skin.myLYellow,
			font = skin.provideFont("B"),
			wraplength= int( dimensions[0]*0.9)
		)
		self.nvpnVersionLbl.grid( row = 1, column = 0, sticky = 'wens')

		# Finally the class grid frame
		self.nvpnSrvcsFrmGrid.grid( row = 0, column = 0, sticky = 'wens' )
