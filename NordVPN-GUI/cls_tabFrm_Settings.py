#!/usr/bin/env python3

########################################
#### 	cls_tabFrm_Settings.py 		####
#### 	Version 20250506 	grid	####
########################################

import tkinter as tk
from tkinter import messagebox
import json
import os

import myTheme as skin
import nvpnPort as nvpnT

from myTable import TkTable as myTkTable
from nvpnSettingCommands import nvpnCommandsArray


def loadSettingCommandsArr():
	return nvpnCommandsArray

# print(f"tabFrmSettings| --")


class TabSettings( tk.Frame ):

	def __init__( 
			self, 
			master = None , 
			dimensions = [ 900, 750 ] 
		):
	
		super().__init__(master)
	
		self.master = master
		self.configure(background=skin.myBlack)
		self.grid()
		print(f"tabFrmSettings| --dimensions: {dimensions}")
		self.dimensions = dimensions
		
		self.tabSttngs_Refresh_bttn = tk.Button(
			self,
			text = "Refresh Settings", 
			command = self.getLiveSettings,
			bg = "#000000",
			fg = "#00FF00",
			font = skin.provideFont("B")
		)		

		self.tabSttngs_GridFrm = tk.LabelFrame(
			self, 
			labelwidget = self.tabSttngs_Refresh_bttn, 
			bg = skin.myBlack,
			width 	= 100, # self.dimensions[0],
			height 	= 100, # self.dimensions[1], 
			labelanchor = 's'
		)

		self.tabSttngs_Data = []
		self.getLiveSettings()


	def getLiveSettings( self ):
		settingsWithControls = []
		tempSttngs_Data = nvpnT.getNvpnItem("settings")
		# print(f"tabFrmSettings| getLiveSettings: --len(tempSttngs_Data): { len(tempSttngs_Data)}\n{ json.dumps( tempSttngs_Data, indent = 2 ) }\n")
		for i,s in enumerate( tempSttngs_Data ):
			#print(f"--i={i} --s={s[0]} --v={s[1]} type-v={ type(s[1]) }")
			settingsWithControls.append( [ s[0], s[1], type(s[1]) ] )

		self.tabSttngs_Data = settingsWithControls
		self.doLayOut()


	def sttngChangeClicked( self , event, args ):
		# print("#"*60)
		print(f"sttngChangeClicked| --args: { args }")
		lclCmnArr = loadSettingCommandsArr() 
		# print(f"tabFrmSettings| sttngChangeClicked: --lclCmnArr: { len(lclCmnArr)}\n{ json.dumps( lclCmnArr, indent = 2 ) }\n" )

		for adjSttng in lclCmnArr:
			"""
				print("="*60)
				print(f"tabFrmSettings| sttngChangeClicked: --lclCmnArr:\t{ adjSttng }" )
				print(f"tabFrmSettings| sttngChangeClicked: --args[0]:\t{ args[0] }" )
				print(f"tabFrmSettings| sttngChangeClicked: --same?:\t{ args[0].lower() == adjSttng['item'].lower() }" )
			"""

			if( args[0].lower() == adjSttng['item'].lower() ):
				args[0] = adjSttng['value']
				print(f"sttngChangeClicked| --adjusted args[0]: {args}")

		nvpnRespArr = nvpnT.getNvpnItem( 'set', args )
		print(f"sttngChangeClicked| --nvpnRespArr: { json.dumps( nvpnRespArr, indent = 4 ) }")
		messagebox.showinfo( "Information", f"{ nvpnRespArr[0] }\n{ nvpnRespArr[1] }")
		self.getLiveSettings()


	def doLayOut( self ):
		# Add widgets via grid

		self.tabSttngs_HeaderFrm = tk.Frame( self.tabSttngs_GridFrm, bg=skin.myBlack, width = self.dimensions[0] )
		self.tabSttngs_HeaderFrm.grid( row = 0, column = 0, sticky = 'we' )
		hdrArray 		= ["SETTING", "VALUE", "CHANGE"]
		hdrArrayWdths 	= [ 20,10,10]
		for hi, h in enumerate(hdrArray):
			hdrLbl = tk.Label( 
				self.tabSttngs_HeaderFrm, 
				width 	= hdrArrayWdths[hi],
				bg 		= skin.myBlack, 
				fg 		= skin.myDBlue, 
				text 	= h, 
				font 	= skin.provideFont("H") )
			hdrLbl.grid( row = 0, column = hi, sticky = 'n' )

		self.tabSttngs_SettingsFrm = tk.Frame( self.tabSttngs_GridFrm, bg=skin.myBlack)
		self.tabSttngs_SettingsFrm.grid( row = 1, column = 0, sticky = 'wens' )

		for i,s in enumerate(self.tabSttngs_Data):

			# print(f"tabFrmSettings| --doLayOut: Adding row {i+1} for { s[2] }-{ s[0] } with a button to change the value from = {s[1]} ")

			# container for this row
			sttngRow = tk.Frame( self.tabSttngs_SettingsFrm , bg = skin.myBlack , width = self.dimensions[0]  )
			sttngRow.grid( row = i, column = 0 , padx = 1 , sticky = 'we')

			# Adding setting items to row 
			sttngTitle = tk.Label( 
				sttngRow, 
				text 	= s[0], 
				font 	= skin.provideFont(14),
				highlightbackground = skin.myBlack,
				highlightthickness = 1,
				width 	= 30 )
			sttngTitle.grid( row = 0, column = 0 , sticky = 'e' )

			sttngVal = tk.Label( 
				sttngRow, 
				text = str(s[1]), 
				font = skin.provideFont(14),
				highlightbackground = skin.myBlack,
				highlightthickness = 1,
				width = 15  )
			sttngVal.grid( row = 0, column = 1  )

			sttngType 	= type(s[1])

			if sttngType == type(True) :
				# print(f"it's a bool, make a button")
				sttngChange = tk.Button(
					sttngRow, 
					text = f'change to { not s[1] }', 
					highlightbackground = skin.myBlack,
					highlightthickness = 3,
					font = skin.provideFont(12) )
				sttngChange.grid( row = 0, column = 2, ipadx = 1, sticky = 'we', columnspan=2 )
				sttngChange.bind(
					"<ButtonPress-1>", 
					lambda event, arg=[ s[0].lower(), (not s[1]) ]: self.sttngChangeClicked( event, arg )
				)

				if s[1]:
					sttngTitle.configure( bg = skin.myTrue, fg = skin.myBlack )
					sttngVal.configure( bg = skin.myTrue, fg = skin.myBlack )

					sttngChange.configure( bg = skin.myFalse, fg = skin.myWhite )

				else:
					sttngTitle.configure( bg = skin.myFalse, fg = skin.myWhite )
					sttngVal.configure( bg = skin.myFalse, fg = skin.myWhite )

					sttngChange.configure( bg = skin.myTrue, fg = skin.myBlack )


			elif sttngType == type("string") :

				if 'firewall' in s[0].lower():
					# print(f"it's a string --> firewall")
					sttngChange = tk.Label(
						sttngRow, 
						text = 'Firewall Mark is fixed',
						font = skin.provideFont(13)
					)
					sttngChange.grid( row = 0, column = 2, sticky = 'e' )

				elif 'technology' in s[0].lower():
					# print(f"it's a string --> technology")
					valNordlynx = tk.Button(sttngRow, text = 'Nordlynx' , font = skin.provideFont(13) )
					valNordlynx.grid( row = 0, column = 2, sticky = 'e')
					valOpenVPN 	= tk.Button(sttngRow, text = 'OpenVPN' , font = skin.provideFont(13) )
					valOpenVPN.grid( row = 0, column = 3, sticky = 'e')
					if s[1] == 'NORDLYNX':
						valOpenVPN.config(state=tk.NORMAL)
						valNordlynx.config(state=tk.DISABLED)
					elif s[1] == 'OPENVPN':
						valNordlynx.config(state=tk.NORMAL)
						valOpenVPN.config(state=tk.DISABLED)

					sttngTitle.configure( bg = skin.myNBlue, fg = skin.myWhite )
					sttngVal.configure( bg = skin.myNBlue, fg = skin.myWhite )

			else:
				print(f"it's something else, stick it in a label")


		# Finally draw the main Frame of this class
		self.tabSttngs_GridFrm.grid( row = 0, column = 0, padx = 2, pady = 2, sticky = 'WENS')

		
