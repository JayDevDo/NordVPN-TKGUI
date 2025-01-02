#!/usr/bin/env python3

############################################
#### 		NordVPNTKGUI.py 			####
#### 		Version 241228_2000 grid	####
############################################

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import myTheme as skin
import nvpnPort as nvpnT

global appSize
appSize 	= [ 900, 750 ]
appWidth 	= appSize[0]
appHeight 	= appSize[1]

# nordVpnVersion is the nordvpn version which was used to build this app. Works 100% on mx-linux debian bookwurm
global nordVpnVersion
nordVpnVersion = "3.19.2"
# Is nordvpn present on the system?
nvpnVersionCurrent = nvpnT.getNvpnItem('version')
print(f"NordVPNTKGUI | --nvpnVersionCurrent: { nvpnVersionCurrent  }")

if ( len( nvpnVersionCurrent ) == 2 ) and ( len( nvpnVersionCurrent[1] ) > 0 ):

	print(f"NordVPNTKGUI | comparing versions: { nvpnVersionCurrent[1] } - { nordVpnVersion }")

	if( nordVpnVersion ==  nvpnVersionCurrent[1].split(' ')[-1] ):
		print(f"NordVPNTKGUI | comparing versions: SAME ")

	elif( nordVpnVersion[0:-2] in nvpnVersionCurrent[1] ):
		
		msgInfoTxt = f"NordVPNTKGUI | comparing versions: SAME-ISH {nordVpnVersion[0:-2]}"

		if nvpnVersionCurrent[1].split(' ')[-1] > nordVpnVersion:
			msgInfoTxt = f"NordVPNTKGUI | comparing versions: SAME-ISH\nRunning: {nvpnVersionCurrent[1].split(' ')[-1] }\nNeeded: {nordVpnVersion}.\nIt might work !"
		else:
			msgInfoTxt = f"NordVPNTKGUI | comparing versions: SAME-ISH\nRunning: {nvpnVersionCurrent[1].split(' ')[-1] }\nNeeded: {nordVpnVersion}.\nIt might work !"

		print(f"{msgInfoTxt}")
		messagebox.showinfo(msgInfoTxt.split('|')[0],msgInfoTxt.split('|')[1][1:])


else:
	print(f"NordVPNTKGUI | nvpnVersionCurrent len not 2 or no info in nvpnVersionCurrent[1]")
	cannotWorkWithoutNordvpn = messagebox.showerror( "NordVPN GUI (Tk)", f"This app needs nordvpn to be installed with at least version {nordVpnVersion}")
	if cannotWorkWithoutNordvpn:
		exit(1)


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

nbDimensions = [ int( appWidth * 0.98 ), int( appHeight * 0.925 ) ] 

# For code folding purpuse to hide all styles
if True:	
	frm_NoteBook = ttk.Style()
	# frm_NoteBook.theme_use("classic") 

	frm_NoteBook.configure( 
		'Jays.TNotebook', 
		background 	= skin.myBlack,
		foreground 	= skin.myWhite,
		tabposition = "nw",
		font 		= ( "Arial", 18, "normal" )
	)

	frm_NoteBook.configure( 
		'Jays.TNotebook.TFrame', 
		background 	= skin.myBlack,
		foreground 	= skin.myLBlue,
		font 		= ( "Arial", 18, "normal" )
	)

	frm_NoteBook.configure( 
		'TFrame', 
		background 	= skin.myBlack,
		foreground 	= skin.myWhite,
		font 		= ( "Arial", 18, "normal" )
	)

	frm_NoteBook.configure( 
		'Jays.TNotebook.Tab', 
		background 	= skin.myBlack,
		foreground 	= skin.myDGreen,
		lightcolor 	= skin.myLBlue,
		padding 	= ( 10, 5 ), 
		font 		= ( "Arial", 22, "bold" )
	)

	frm_NoteBook.map(
		'Jays.TNotebook.Tab',
		background = [
			( 'active', 	"#FFDD44"),	# Golden for active tab
			( 'selected', 	"#BB00BB")	# Purple for selected
		],  
		foreground = [
			( 'selected', 	"#FFFFFF" )
		]
	)



# create the main window frame
mwFrameGrid = tk.Frame(root,width=appWidth,height=appHeight,bg=skin.myBlack)
mwFrameGrid.grid(row=0, column=0)

# create a notebook
notebook = ttk.Notebook( 
	mwFrameGrid, 
	width 	= nbDimensions[0], 
	height 	= nbDimensions[1], 
	style 	= 'Jays.TNotebook')
notebook.grid(
	row 	= 0,
	column 	= 0, 
	pady 	= 5, 
	padx 	= 5,
	sticky  = 'WENS'
)

tabDimensions 	= [ int( appWidth * 0.90 ), int( appHeight * 0.80 ) ]

# tab ACCOUNT START
from cls_tabFrm_Account import TabAccount
tab_Account = TabAccount( notebook, dimensions = tabDimensions )
# tab_Account.grid( row = 0, column = 0, sticky = 'WENS' )
notebook.add( tab_Account, text = 'Account' )
# End of tab ACCOUNT


# tab CONNECT START
from cls_tabFrm_Connections import TabConnections
tab_Connect = TabConnections( notebook, dimensions = tabDimensions )
# tab_Connect.grid( row = 0, column = 0 )
# , sticky = 'WENS' 
notebook.add( tab_Connect, text = 'Connection' )
# End of tab CONNECT


# tab SETTINGS START
from cls_tabFrm_Settings import TabSettings
tab_Settings = TabSettings( notebook , dimensions = tabDimensions )
tab_Settings.grid( row = 0, column = 0, sticky = 'N' )
# , sticky = 'WENS' 
notebook.add( tab_Settings, text = 'Settings')
# End of tab SETTINGS
"""
"""

root.mainloop()
