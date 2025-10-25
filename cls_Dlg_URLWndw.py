#!/usr/bin/env python3

########################################
#### 	cls_Dlg_URLWndw.py 			####
#### 	Version 20250506 	grid	####
########################################

import subprocess
import webbrowser

import tkinter as tk
import myTheme as skin

class URLDialog:

	def __init__(
			self, 
			parent,
			url="https://nordvpn.com/login"
		):

		dlgRoot = self.dlgRoot = tk.Toplevel(parent)

		dlgRoot.geometry("600x250")
		dlgRoot.configure( background = skin.myBlack )

		self.url = url 
		self.result = None

		self.myLabel = tk.Label(
			dlgRoot, 
			text = 'Log in to NordVPN via browser. Then restart the app after you have logged in.',
			font = skin.provideFont(22) ,
			bg = skin.myLbxBG )
		self.myLabel.grid( row = 0, column = 0)

		self.openURLLbl = tk.Label(
			dlgRoot,
			background 		= skin.myBlack,
			foreground 		= skin.myLGreen,
			text 			= self.url,
			font 			= skin.provideFont(12)
			#,textwrap 		= 200
		)
		self.openURLLbl.grid( row = 1, column = 0, sticky = 'wens' )

		self.mySubmitButton = tk.Button( 
			dlgRoot, 
			font= skin.provideFont(20),
			text= 'Submit',
			bg 	= skin.myBlack, 
			fg 	= skin.myNGreen )
		self.mySubmitButton.grid( row = 2, column = 0, sticky = 'wens' )
		self.mySubmitButton.bind('<Button-1>', self.dboxSend )


	def dboxSend( self, event ):
		self.result = webbrowser.open( self.url )
		print(f"dboxSend| self.result: {self.result}")
		self.dlgRoot.destroy()

"""
def onClick():
	inputDialog = ListBoxDialog(root)
	root.wait_window(inputDialog.dlgRoot)
	print('Rated as: ', inputDialog.result)
"""
