#!/usr/bin/env python3

########################################
#### cls_Frm_Mesh_Rightslabels.py 	####
#### 	Version 20250712 	grid	####
########################################

import os, json, time
import tkinter as tk
from tkinter import ttk
import myTheme as skin
from pubsub import pub 
from meshnet.cls_Frm_CanvasLabel import canvasLblFrm as clrLabel
import meshnet.nvpnMeshPort as meshPort

#==============================================================================
class MeshRightsLabels( tk.Frame ):

	#--------------------------------------------------------------------------
	def __init__(
			self,
			master = None ,
			dimensions = [ 1000, 600 ]
		):

		super().__init__( master )

		self.master = master
		self.dimensions = dimensions

		self.configure( background = skin.myBlack )
		self.grid()

		self.chosenPeerName = "select peer"
		self.allPeerRights 	= [ {}, {} ]

		self.meshActionsGrid = tk.Frame( 
			self, 
			height = self.dimensions[0], 
			width = self.dimensions[1], 
			bg = skin.myBlack 
		)

		self.meshActions = [
			"incoming", 	# 0
			"routing",		# 1
			"local",		# 2
			"sending",		# 3
			"auto-accept"	# 4
		] # These are used in peer rights

		self.meshCommands = [
			"incoming", 	# 0
			"routing",		# 1
			"local",		# 2
			"fileshare",	# 3
			"auto-accept"	# 4
		] # These are used on commandline


		pub.subscribe( self.chosenPeerListener, 'newPeerSelected' )		
		self.doLayOut()


	#--------------------------------------------------------------------------
	def chosenPeerListener( self, anyArgs ):
		"""
			pub.sendMessage( 
				"newPeerSelected", 
				anyArgs = [ 
					self.selectedPeerName, 
					self.selectedPeerArr, 
					self.peerRights 
				] 
			)
		"""
		# print(f"MeshRightsLabels | chosenPeerListener - { json.dumps( anyArgs, indent = 4 ) }")
		self.chosenPeerName = anyArgs[0]
		# Don't need full device array (anyArgs[1]) here
		self.allPeerRights = anyArgs[2]		
		self.doLayOut()
	
	#--------------------------------------------------------------------------
	def permissionChangeClicked( self , event, args ):
		# print(f"MeshRightsLabels.permissionChangeClicked | TRY --args: { args }")
		cmmndRetVal = meshPort.meshCmndRouter("peer", args )
		print(f"MeshRightsLabels.permissionChangeClicked | --cmmndRetVal: {cmmndRetVal}")

	#--------------------------------------------------------------------------
	def makePrmssnLabel( self, parentFrame, action ):
		""" returns a clickable tk Label, and commandlineString to change the setting """
		# Label will be blank unless allPeerRights is filled.
		permssnStr = "deny"
		commandStr = ""
		tmp_lbl_Bln = False
		tmp_lbl_Text = ""
		tmp_lbl_clrT = ( skin.myDRed, skin.myWhite )
		tmp_lbl_clrF = ( skin.myLGreen, skin.myBlack )
		clrTuple = tmp_lbl_clrF

		try:
			# print(f"MeshRightsLabels.makePrmssnBttn | TRY --action: { action }")

			if self.allPeerRights[0]:
				# print(f"MeshRightsLabels.makePrmssnBttn | --self.allPeerRights[0]: { self.allPeerRights[0] }")
				for rghtPerm in self.allPeerRights[0]:
					# print(f"MeshRightsLabels.makePrmssnBttn | --rghtPerm: { rghtPerm }")
					
					if action == "auto-accept":
						# print(f"MeshRightsLabels.makePrmssnBttn | --action == auto-accept value: { self.allPeerRights[0]["Accept Fileshare Automatically"] }")
						tmp_lbl_Bln = self.allPeerRights[0]["Accept Fileshare Automatically"]
						permssnStr = "disable" if tmp_lbl_Bln else "enable"

					else:
						# print(f"MeshRightsLabels.makePrmssnBttn | --action in rghtPerm: { action in rghtPerm.lower() }")
						if action in rghtPerm.lower() :
							tmp_lbl_Bln = self.allPeerRights[0][rghtPerm]
							permssnStr = "deny" if tmp_lbl_Bln else "allow"

					tmp_lbl_Text = f"Change to '{ permssnStr }'" 
					commandStr = f"{ action.replace('sending','fileshare') } {permssnStr} { self.chosenPeerName }"

			else:
				# print(f"MeshRightsLabels.makePrmssnBttn ! --self.allPeerRights == empty")
				tmp_lbl_Bln = False
				tmp_lbl_Text = "Select a peer"

			clrTuple = tmp_lbl_clrT if tmp_lbl_Bln else tmp_lbl_clrF
			# print(f"MeshRightsLabels.makePrmssnBttn | --tmp_lbl_Bln: {tmp_lbl_Bln} --tmp_lbl_Text: {tmp_lbl_Text} --clrTuple: { clrTuple }")


		except Exception as e:
			print(f"MeshRightsLabels.makePrmssnBttn ! Exception: {e}")

		finally:
			# print(f"MeshRightsLabels.makePrmssnBttn | Finally --action: { action }")
			tmpRet_lbl = tk.Label(
				parentFrame,
				text = f"{ tmp_lbl_Text }",
				font = skin.provideFont("B"),
				bg = clrTuple[0],
				fg = clrTuple[1]
			)

			# print(f"MeshRightsLabels.makePrmssnBttn | Finally --action: { action } --commandStr: {commandStr}")
			return ( tmpRet_lbl, commandStr )



	#--------------------------------------------------------------------------
	def doLayOut( self ):
		"""
			Meshnet actions buttons has 2 columns
			Col 1: Buttons to change permissions (only if peer has been selected)
			Col 2: Name of the permission
			Actions are always relative to the chosen peer
		"""
		# print(f"MeshRightsLabels.doLayOut | START --self.meshActions: { json.dumps( self.meshActions, indent = 4) }")

		if len( self.meshActions ) > 0:

			for i, p in enumerate( self.meshActions ):
				# print(f"MeshRightsLabels.doLayOut | --i: {i} --p: {p}")
				meshActions_lbl = tk.Label(
					self.meshActionsGrid,
					text = f"{ p.upper() }",
					font = skin.provideFont("B"),
					fg = skin.myBlack,
					bg = skin.myWhite
				)
				meshActions_lbl.grid( row = i, column = 1 , pady = 2, padx = 2, sticky = 'WE' )

				perm_lbl, perm_cmd  = self.makePrmssnLabel( self.meshActionsGrid, p )
				# print(f"MeshRightsLabels.doLayOut | -- perm_cmd: { perm_cmd }")
				perm_lbl.grid( row = i, column = 0 , pady = 2, padx = 2, sticky = 'WE' )

				perm_lbl.bind(
					"<ButtonPress-1>", 
					lambda event, arg=perm_cmd.split(' '): self.permissionChangeClicked( event, arg )
				)


		else:
			print(f"MeshRightsLabels.doLayOut | START --self.meshActions NOT > 0")

		# Finally draw the main grid
		self.meshActionsGrid.grid( row = 0, column = 0, sticky = 'WENS' )


		"""

            "Allow Incoming Traffic": true,
			nordvpn meshnet peer incoming allow <device> 	/ nordvpn meshnet peer incoming deny <device>

            "Allow Routing": false,
			nordvpn meshnet peer routing allow <device> 	/ nordvpn meshnet peer routing deny <device>

            "Allow Local Network Access": false,
			nordvpn meshnet peer local allow <device> 		/ nordvpn meshnet peer local deny <device>

            "Allow Sending Files": true,
			nordvpn meshnet peer fileshare allow <device> 	/ nordvpn meshnet peer fileshare deny <device>

            "Accept Fileshare Automatically": false
			nordvpn meshnet peer auto-accept enable <device> / nordvpn meshnet peer auto-accept disable <device>


			nordvpn meshnet peer nickname set <device> <nickname> /  nordvpn meshnet peer nickname remove <device>
			nordvpn meshnet peer refresh

		"""