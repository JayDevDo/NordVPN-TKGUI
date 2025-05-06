#!/usr/bin/env python3

############################################
#### 		cls_Frm_AccActions.py 		####
#### 		Version 20250506 	grid	####
############################################

import tkinter as tk
from tkinter import messagebox

import myTheme as skin
import nvpnPort as nvpnT

from cls_Dlg_URLWndw import URLDialog as urlMsgBox

import sys 
import os
import time 
import json 
import subprocess
import psutil
import asyncio

""" 
	--------------------
	AccountActionsFrame
	--------------------
	Contains 3 buttons.

		LogIn
		LogOut
		StartServices

	In nvpnPort.getNvpnItem['login'] :
		# Either the user is already logged in. The response will be "You are already logged in." 
		# or ...
		# A html link is returned to be opened in a browser window
		# e.g.: "Continue in the browser: https://api.nordvpn.com/v1/users/oauth/login-redirect?attempt=2e7e88d5-1ee5-4ac4-9a47-3ded0f0307a2"
		# embedded html because of authentication occurs outside this app.
		nvpnTnnlResponse = rawLginResponse
		# "https://api.nordvpn.com/v1/users/oauth/login-redirect?"# 
		# handleResponseStrings( rawLginResponse )

	From 'nvpnPort' we get the result of 'nordvpn login'.
		-> When already logged in the result is "You are already logged in."
		-> If not logged in, the result contains an url that we launch off the cmmand line.
"""

global extAuthStarted
extAuthStarted = False

global curLogInStts
curLogInStts = False

async def startService():
	#  As the service is started with systemctl, the user should be prompted for admin rights automatically 
	stProcessResp = subprocess.run( ["systemctl","start", "nordvpnd"], capture_output = True )
	print(f"AccountActionsFrame.async-startService() start the service response: { stProcessResp }" )
	return stProcessResp


class AccountActionsFrame( tk.Frame ):

	def __init__( 
			self, 
			master = None, 
			dimensions = [ 400, 400 ]		
		):

		super().__init__( master )

		global extAuthStarted
		global curLogInStts

		self.master = master
		self.configure(background=skin.myBlack)
		self.grid()

		print(f"AccountActionsFrame called with dimensions: { dimensions }")
		self.dimensions = dimensions

		self.frmAccActnsLIArr 	= []
		self.frmAccActnsLIStr 	= ""
		self.frmAccActnsLIUrl 	= ""
		self.aaLblBGClr 		= skin.myLRed

		self.frmAccActnsGrid = tk.Frame(
			self, 
			bg 		= skin.myBlack,
			pady 	= 10,
			padx 	= 10
		)

		self.frmAccActnsStatTitlelLbl = tk.Label( 
			self.frmAccActnsGrid, 
			bg 		= skin.myWhite,
			fg 		= skin.myBlack,
			font 	= skin.provideFont("H"),
			text 	= "Log In Status" 
		)

		self.frmAccActnsLogInStatusLbl = tk.Label(
			self.frmAccActnsGrid,
			text = self.frmAccActnsLIStr,
			bg = self.aaLblBGClr,
			fg = skin.myBlack, 
			padx = 4, 
			pady = 4,
			wraplength = 280 
		)

		self.frmAccActnsAwaitAuthLbl = tk.Label(
			self.frmAccActnsGrid,
			text = "Waiting for external log in",
			bg = skin.myLGreen,
			fg = skin.myDRed,
			padx = 4, 
			pady = 4
		)

		self.frmAccActnsLogInBttn = tk.Button(
			self.frmAccActnsGrid,
			command = self.launchURL,
			text 	= f"LOG IN\n(opens a webbrowser)",
			bg 		= skin.myBlack,
			fg 		= skin.myNYellow
		)

		self.frmAccActnsLogOutBttn = tk.Button(
			self.frmAccActnsGrid,
			command = self.startLogOut,
			text 	= "LOG OUT",
			bg 		= skin.myBlack,
			fg 		= skin.myNYellow
		)

		self.frmAccActnsWidgets = [
			self.frmAccActnsStatTitlelLbl, 	# 0
			self.frmAccActnsLogInStatusLbl,	# 1
			self.frmAccActnsAwaitAuthLbl,	# 2
			self.frmAccActnsLogInBttn,		# 3
			self.frmAccActnsLogOutBttn		# 4
		]

		self.refreshData()
		self.initGrid()


	def showParams( self ):
		global extAuthStarted
		global curLogInStts
		paramObj = {
			'extAuthStarted': extAuthStarted,
			'curLogInStts': curLogInStts,
			'LIString': 	self.frmAccActnsLIStr,
			'URL': 			self.frmAccActnsLIUrl,
			'lblBG': 		self.aaLblBGClr
		}
		# print(f"showParams: {json.dumps(paramObj, indent=4)}")


	def launchStartService( self ):
		#return asyncio.run( startService() );
		self.showParams()


	def launchURL( self ):
		global extAuthStarted
		extAuthStarted = True
		urlPopUp = urlMsgBox(self, url = self.frmAccActnsLIUrl ) # "https://example.com"
		self.wait_window(urlPopUp.dlgRoot)
		print(f"launchURL| --urlPopUp.result: {urlPopUp.result}")
		self.showParams()


	def startLogOut( self ):
		global extAuthStarted
		global curLogInStts
		confMsg = messagebox.askyesno(f"Confirm Log Out", f"Do you really want to log out?")
		print(f"startLogOut| --confMsg: { confMsg }" )
		if confMsg:
			nvpnT.getNvpnItem("logout")
			extAuthStarted 	= False
			curLogInStts 	= False


	def refreshData( self ):
		# Get the login status from nvpnPort, then launch 'doLayOut'
		global extAuthStarted
		global curLogInStts

		self.showParams()

		if not extAuthStarted:
			self.frmAccActnsLIArr = nvpnT.getNvpnItem( 'login' )
			
		self.frmAccActnsLIStr = str( self.frmAccActnsLIArr[0] )

		self.showParams()

		if( "You are already logged in." == self.frmAccActnsLIStr ):
			extAuthStarted = True
			curLogInStts = True
			self.frmAccActnsLIStr = "You are already logged in."
			self.aaLblBGClr = skin.myTrue
			# print(f"finished changing params for logged IN ")
			# skip the rest if logged in, services and extAuth are not needed
			# self.doLayout()

		else:
			curLogInStts = False
			self.aaLblBGClr = skin.myFalse

			if extAuthStarted:
				self.frmAccActnsLIStr = "Awaiting external login (webbrowser)"

			else:

				if( "https://" in self.frmAccActnsLIStr ):
					# ['Continue in the browser: https://api.nordvpn.com/v1/users/oauth/login-redirect?attempt=3d1b4c1f-1326-4d02-8bce-b0f2047df609']
					self.frmAccActnsLIUrl = self.frmAccActnsLIStr[25:]
					self.frmAccActnsLIStr = "You are logged OUT"

		self.showParams()
		self.doLayOut()


	def hideWidget( self, widget ):
		widget.grid_forget()


	def showWidget( self, widget, rw, clmn):
		widget.grid( row = rw, column = clmn )


	def initGrid( self ):
		self.frmAccActnsStatTitlelLbl.grid( row = 0, column = 0, sticky = 'WE' )
		self.frmAccActnsLogInStatusLbl.grid(row = 1, column = 0, sticky = 'WE' )
		self.frmAccActnsAwaitAuthLbl.grid( 	row = 2, column = 0, sticky = 'WE' )
		self.frmAccActnsLogInBttn.grid( 	row = 3, column = 0, sticky = 'WE' )
		self.frmAccActnsLogOutBttn.grid( 	row = 4, column = 0, sticky = 'WE' )
		
		# And finally the grid container Frame	
		self.frmAccActnsGrid.grid( row = 0, column = 0) 
		# , sticky = 'WENS' 
		self.doLayOut()


	def doLayOut( self ):
		global extAuthStarted
		global curLogInStts
		#	self.frmAccActnsStatTitlelLbl, 	# 0
		#	self.frmAccActnsLogInStatusLbl,	# 1
		#	self.frmAccActnsAwaitAuthLbl,	# 2
		#	self.frmAccActnsLogInBttn,		# 3
		#	self.frmAccActnsLogOutBttn		# 4

		#  Always show 0,1
		self.frmAccActnsWidgets[1].configure( text = self.frmAccActnsLIStr )

		if curLogInStts:
			# show 4
			# hide 2,3. Can't log in when already logged in, and no extAuth needed
			# print(f"AccountActionsFrame.doLayout --curLogInStts: {curLogInStts} ")
			self.hideWidget( self.frmAccActnsWidgets[2] )
			self.hideWidget( self.frmAccActnsWidgets[3] )
			self.frmAccActnsWidgets[1].configure( bg = skin.myTrue )

		else:
			# print(f"AccountActionsFrame.doLayout --curLogInStts==False: --extAuthStarted: { extAuthStarted }")
			# hide 4. Can't log out when not logged in
			self.hideWidget( self.frmAccActnsWidgets[4] )
			self.frmAccActnsWidgets[1].configure( bg = skin.myFalse )

			if extAuthStarted:
				# show 2 should show url
				# hide 3 the log in process has started. maybe keep if we dont catch fresh log in status
				# print(f"AccountActionsFrame.doLayout --curLogInStts==False: --extAuthStarted==True")
				self.hideWidget( self.frmAccActnsWidgets[3] )
				self.frmAccActnsWidgets[1].configure( bg = skin.myLYellow )

			else:
				# show 3. Not logged in, 
				# hide 2. extAuth not started
				# print(f"AccountActionsFrame.doLayout --curLogInStts==False: --extAuthStarted==False")
				self.hideWidget( self.frmAccActnsWidgets[2] )
				self.frmAccActnsWidgets[1].configure( bg = skin.myFalse )


