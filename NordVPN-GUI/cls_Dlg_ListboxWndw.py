#!/usr/bin/env python3

########################################
#### 	cls_Dlg_ListboxWndw.py 		####
#### 	Version 20250506 	grid	####
########################################

import tkinter as tk
import myTheme as skin

class ListBoxDialog:

	def __init__(self, parent):

		top = self.top = tk.Toplevel(parent)

		top.geometry("350x250")
		top.configure( background = skin.myBlack )
		self.ratingArray = [ "*****", "****", "***", "**", "*" ]
		self.ratingArrayStrVar = tk.StringVar()
		self.ratingArrayStrVar.set(self.ratingArray)

		self.myLabel = tk.Label(
			top, 
			text = 'Rate the last connection',
			font = skin.provideFont(22) ,
			bg = skin.myLbxBG )
		self.myLabel.grid( row = 0, column = 0, columnspan = 2 )

		self.ratingLB = tk.Listbox(
			top,
			selectbackground= skin.myLBlue,
			background 		= skin.myBlack,
			foreground 		= skin.myLGreen,
			selectmode  	= 'single',
			height 			= 6,
			width 			= 5,
			listvariable 	= self.ratingArrayStrVar,
			font 			= skin.provideFont(20)
		)
		self.ratingLB.configure( exportselection = False )
		self.ratingLB.bind( "<<ListboxSelect>>", self.lbUpdate )
		self.ratingLB.grid( row = 1, column = 0 )

		self.mySubmitButton = tk.Button( 
			top, 
			font= skin.provideFont(20),
			text= 'Submit',
			bg 	= skin.myBlack, 
			fg 	= skin.myNGreen )
		self.mySubmitButton.grid(row=1,column=1,sticky='wens')
		self.mySubmitButton.bind('<Button-1>', self.dboxSend )


	def lbUpdate( self, event ):
		pickedItem = self.ratingArray[0]
		if ( len( self.ratingLB.curselection() ) > 0 ):
			pickedItem = event.widget.get( self.ratingLB.curselection()[0] )
			print(f"lbUpdate| --pickedItem: {pickedItem}")
			self.mySubmitButton.configure( text = f"Rate as\n{ len(pickedItem) }", bg=skin.myNGreen, fg = skin.myBlack )			
			# Adjust accordingly
			self.result = str( len(pickedItem) )


	def dboxSend( self, event ):
		print(f"dboxSend| self.result: {self.result}")
		self.top.destroy()

"""
def onClick():
	inputDialog = ListBoxDialog(root)
	root.wait_window(inputDialog.top)
	print('Rated as: ', inputDialog.result)
"""
