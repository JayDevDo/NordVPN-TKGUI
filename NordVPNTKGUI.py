#!/usr/bin/env python3

########################################
#### 		NordVPNTKGUI.py 		####
#### 	Version 20250701 	grid	####
########################################

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from pubsub import pub

#import ttkbootstrap as ttk2
import myTheme as skin
import nvpnPort as nvpnT

from PIL import Image
from PIL import ImageTk
iconSize = (32,32)

from cls_Frm_StatusBar import MyStatusBar
from cls_tabFrm_Account import TabAccount
from cls_tabFrm_Connections import TabConnections
from cls_tabFrm_Settings import TabSettings
from cls_tabFrm_Meshnet import TabMeshDevices

global appSize
appSize 	= [ 1100, 850 ]
appWidth 	= appSize[0]
appHeight 	= appSize[1]

# nordVpnVersion is the nordvpn version which was used to build this app. Works 100% on mx-linux debian bookwurm
global nordVpnVersion
nordVpnVersion = "4.0.0"
# 4.0.0 should work with nordvpn-gui 2.0 (official GUI, with limited settings, and NO meshnet )


def iconifyImage( imagePath ):
	imgIcon = Image.open( imagePath )
	imgIcon = imgIcon.resize( iconSize ) # , Image.ANTIALIAS
	return ImageTk.PhotoImage( imgIcon )


# First get the status of nordvpn services/processes. This will set the globals:  --glbl_serviceActive and --glbl_loginStatus
curStatus = nvpnT.nordProcesses()
print(f"NordVPNTKGUI | --nordProcesses: {curStatus}\n--glbl_serviceActive:{ curStatus[0] }\n--glbl_loginStatus: { curStatus[1] }")

# For code folding purpuse to hide all root window settings
if True:	
	root = tk.Tk()
	appGeometry = f'{appWidth}x{appHeight}'
	root.geometry(appGeometry)
	print(f"appSize: { appSize } | appGeometry: {appGeometry} | appWidth: {appWidth} | appHeight: {appHeight} ")

	root.resizable( 1, 1 )
	root.grid_anchor( anchor = 'n' )
	root.configure( bg = skin.myBlack )
	root.title('NordVPN GUI (Tk)')
	root.tk.call(
		"wm", 
		"iconphoto", 
		root._w, tk.PhotoImage( file = skin.icoPath ) 
	)

# Define size of app and tabs
nbDimensions 	= [ int( appWidth * 0.98 ), int( appHeight * 0.90 ) ] 
tabDimensions 	= [ int( appWidth * 0.95 ), int( appHeight * 0.90 ) ]

# For code folding purpuse to hide all styles
if True:	
	frm_NoteBook = ttk.Style()
	
	# frm_NoteBook = ttk2.Style("darkly")
	# frm_NoteBook.theme_use("classic") 
	frm_NoteBook.configure( 
		'Jays.TNotebook', 
		background 	= skin.myBlack,
		foreground 	= skin.myWhite,
		tabposition = "nw",
		font 		= skin.provideFont(18)
	)

	frm_NoteBook.configure( 
		'Jays.TNotebook.TFrame', 
		background 	= skin.myBlack,
		foreground 	= skin.myLBlue,
		font 		= skin.provideFont(18)
	)

	frm_NoteBook.configure( 
		'TFrame', 
		background 	= skin.myBlack,
		foreground 	= skin.myWhite,
		font 		= skin.provideFont(18)
	)

	frm_NoteBook.configure( 
		'Jays.TNotebook.Tab', 
		# background 	= skin.myBlack,
		background 	= skin.myDBlue,
		foreground 	= skin.myWhite,
		lightcolor 	= skin.myLBlue,
		padding 	= ( 5, 5 ), 
		font 		= ( "Arial", 22, "bold" )
	)

	frm_NoteBook.map(
		'Jays.TNotebook.Tab',
		background = [
			( 'active', 	skin.myNYellow 	),
			( 'selected',  	skin.myNGreen 	),
			( 'disabled', 	skin.myDGrey 	)	
		],  
		foreground = [
			( 'active', 	skin.myBlack 	),
			( 'selected', 	skin.myWhite 	),
			( 'disabled', 	skin.myLGrey 	)	# Grey for disabled
		],
		lightcolor = [
			( 'selected', 	skin.myLBlue 	),
			( 'disabled', 	skin.myBlack 	)
		]
	)


# create the main window frame
mwFrameGrid = tk.Frame( root, width = appWidth, height = appHeight, bg = skin.myBlack )
mwFrameGrid.grid( row = 0, column = 0, sticky = 'WENS' )

# add the statusBar
appStatusBar = MyStatusBar( mwFrameGrid, dimensions = [ appWidth,  int( appHeight - nbDimensions[1] ) ] )
appStatusBar.grid( row = 8, column = 0, sticky = 'WENS' )

# create a notebook
notebook = ttk.Notebook( 
	mwFrameGrid, 
	width 	= nbDimensions[0], 
	height 	= nbDimensions[1], 
	style 	= 'Jays.TNotebook'
)
notebook.grid( row = 0,	column = 0, pady = 5, padx = 5, sticky = 'N' )


# tab ACCOUNT START 
tabAccountIconPath = skin.iconPath('user_gear')
tabAccountImage = iconifyImage( tabAccountIconPath )
tab_Account = TabAccount( notebook, dimensions = tabDimensions )
notebook.add( tab_Account, text = 'Account', image = tabAccountImage, compound = "left" ) 

# End of tab ACCOUNT

# tab CONNECT START  connectdevelop
tabConnectIconPath = skin.iconPath('vpn-symbol')
tabConnectImage 	=  iconifyImage( tabConnectIconPath )
tab_Connect = TabConnections( notebook, dimensions = tabDimensions )
notebook.add( tab_Connect, text = 'Connection', image = tabConnectImage, compound = "left") 

# End of tab CONNECT


# tab SETTINGS START 'bars'
tabSettingsIconPath = skin.iconPath('gear')
tabSettingsImage 	=  iconifyImage( tabSettingsIconPath )
tab_Settings = TabSettings( notebook , dimensions = tabDimensions )
notebook.add( tab_Settings, text = 'Settings', image = tabSettingsImage, compound = "left" ) 

# End of tab SETTINGS


# tab DEVICES START 
tabDevicesIconPath 	= skin.iconPath('network-wired')
tabDevicesImage 	=  iconifyImage( tabDevicesIconPath )
tab_Devices = TabMeshDevices( notebook, dimensions = tabDimensions )
notebook.add( tab_Devices, text = 'Meshnet', image = tabDevicesImage, compound = "left" ) 

# End of tab DEVICES 

"""
def updateConnStatusEverywhere( anyArgs ):
	print(f"NordVPNTKGUI | updateConnStatusEverywhere: ")
	tab_Account.tabAccActConnFrame.

tab_Account.bind("<Clicked>", 	tabGotFocus( "ACCOUNT", "IN")	)
tab_Account.bind("<FocusOut>", 	tabGotFocus( "ACCOUNT", "OUT")	)

tab_Connect.bind("<FocusIn>", 	tabGotFocus( "CONNECT", "IN")	)
tab_Connect.bind("<FocusOut>", 	tabGotFocus( "CONNECT", "OUT")	)

tab_Settings.bind("<FocusIn>", 	tabGotFocus( "SETTINGS", "IN")	)
tab_Settings.bind("<FocusOut>", 	tabGotFocus( "SETTINGS", "OUT")	)

tab_Devices.bind("<FocusIn>", 	tabGotFocus( "DEVICES", "IN")	)
tab_Devices.bind("<FocusOut>", 	tabGotFocus( "DEVICES", "OUT")	)

"""

def tabGotFocus( event ):
	selectedTab 		= notebook.select()
	selectedTabIndex 	= notebook.index( selectedTab )
	print(f"tabGotFocus | --selectedTab: { selectedTab } --selectedTabIndex: { selectedTabIndex }")

	if selectedTabIndex == 0:
		tab_Account.addConnStatus()

	elif selectedTabIndex == 1:
		tab_Connect.refreshConnStatus()

	elif selectedTabIndex == 2:
		tab_Settings.getLiveSettings()

	elif selectedTabIndex == 3:
		print(f"so far, no refresh needed for meshnet: { selectedTabIndex }")
		# tab_Devices.

	else:
		print(f"unknown tabIndex: { selectedTabIndex }")

	print(f"{'*'*80}\ntabGotFocus END --selectedTabIndex = { selectedTabIndex }")


notebook.bind("<<NotebookTabChanged>>", tabGotFocus )


root.mainloop()
