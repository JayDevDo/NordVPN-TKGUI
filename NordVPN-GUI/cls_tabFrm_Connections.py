#!/usr/bin/env python3

########################################
#### 	cls_tabFrm_Connections.py 	####
#### 	Version 20250510 	grid	####
########################################

import tkinter as tk
from tkinter import messagebox

import myTheme as skin
import nvpnPort as nvpnT
import json
import time

from pubsub import pub

from cls_Dlg_ListboxWndw import ListBoxDialog as dlgRating
from cls_Frm_ConnStatus import ConnStatusFrame

class TabConnections( tk.Frame ):

	def __init__( 
			self, 
			master = None, 
			dimensions = [ 1000, 750 ] 
		):
	
		super().__init__( master )
	
		print(f"TabConnections called with dimensions: {dimensions}")

		self.master = master
		self.configure(background=skin.myBlack)
		self.grid()
		self.dimensions = dimensions

		nvpnT.groupListManager("set")
		nvpnT.countryListManager("set")
		nvpnT.loadAllConns()

		# self.connectionConfig['selected']['cntry']
		self.connectionConfig = {
			'selected': {
				'grp': 	nvpnT.chosenGroupManager('get'),
				'cntry':nvpnT.chosenCountryManager('get'),
				'cty':	nvpnT.chosenCityManager('get'),
				'cnnctnStr': "",
				'curConnStatus': "disconnected",
				'cnnctnRate': "5"
			},
			'lists':{
				'grp': 	nvpnT.groupListManager("get"),
				'cntry':nvpnT.countryListManager("get"),
				'cty':	nvpnT.cityListManager("get")
			}
		}

		self.connLB_GrpVar 	= tk.StringVar()
		self.connLB_CntrVar = tk.StringVar()
		self.connLB_CtyVar 	= tk.StringVar()
		self.connLB_ConnsVar = tk.StringVar()

		# Define variable to hold the value of the filter Entry
		self.connFltrStrVar = tk.StringVar()
		self.connFltrStrVar.trace( 'w', self.liveCntrFilter )

		self.activeConnStatus()

		##################################################
		# The frame that holds all connection-tab widgets
		##################################################
		self.tabConnGridFrame = tk.Frame( 
			self, 
			bg 		= skin.myBlack, 
			highlightcolor = skin.myLBlue # ,width 	= self.dimensions[0],height	= self.dimensions[1]
		)

		#================================================================
		# Things that go in the tabConnGroupFrm (group selection widgets)
		# tabConnGridFrame( row = 0, column = 0 )
		#################################################################
		if True:
			self.tabConnGroupFrm = tk.LabelFrame(
				self.tabConnGridFrame,
				text = "GROUP",
				bg 	= skin.myDBlue, 
				fg 	= skin.myBlack,
				labelanchor = 'n',
				font = skin.provideFont(24) )
			self.tabConnGroupFrm.grid( row = 0, column = 0, sticky = 'n' , padx = 12, pady = 10)


			self.selectServerGroupLb = tk.Listbox(
				self.tabConnGroupFrm,
				selectbackground= skin.myNGreen,
				background 		= skin.myBlack,
				foreground 		= skin.myLbxFG,
				width 			= 30,
				height 			= 9,
				selectmode  	= 'single',
				listvariable 	= self.connLB_GrpVar,
				font 			= skin.provideFont(14) )
			self.selectServerGroupLb.configure( exportselection = False )
			self.selectServerGroupLb.bind( "<<ListboxSelect>>", self.updateSelectedGroup )
			self.selectServerGroupLb.grid( row = 0, column = 0, columnspan = 1, sticky = 'n' )

			self.tabConnGroupClearBtn = tk.Button(
				self.tabConnGroupFrm,
				font  	= skin.provideFont("B"),
				bg 		= skin.myBlack,
				fg 		= skin.myLGreen,
				text 	= "Reset group",
				command = self.clearSelectedGroup)
			self.tabConnGroupClearBtn.grid( row = 1, column = 0, padx = 2 )


		#====================================================================
		# Things that go in the tabConnCountryFrm (country selection widgets)
		# tabConnGridFrame( row = 0, column = 1 )
		#####################################################################
		if True:
			self.tabConnCountryFrm = tk.LabelFrame(
				self.tabConnGridFrame,
				text = "COUNTRY",
				bg 	= skin.myNBlue, 
				fg 	= skin.myBlack,
				labelanchor = 'n',
				font = skin.provideFont(24)	)
			self.tabConnCountryFrm.grid( row = 0, column = 1, sticky = 'n', padx = 5, pady = 10)

			self.selectServerCountryLb = tk.Listbox(
				self.tabConnCountryFrm,
				selectbackground= skin.myNGreen,
				background 		= skin.myBlack,
				foreground 		= skin.myLbxFG,
				width 			= 24,
				height 			= 8,
				selectmode  	= 'single',
				listvariable 	= self.connLB_CntrVar,
				font 			= skin.provideFont(14) )
			self.selectServerCountryLb.configure( exportselection = False )			
			self.selectServerCountryLb.bind( "<<ListboxSelect>>", self.updateSelectedCountry )
			self.selectServerCountryLb.grid( row = 0, column = 0, padx = 1, sticky = 'n')

			self.tabConnCountryClearBtn = tk.Button(
				self.tabConnCountryFrm,
				font  	= skin.provideFont("B"),
				bg 		= skin.myBlack,
				fg 		= skin.myLGreen,
				text 	= "Reset country (+filter)",
				command = self.clearSelectedCountry )
			self.tabConnCountryClearBtn.grid( row = 1, column = 0 )

			self.tabConnFltrCnt = tk.Frame( 
				self.tabConnCountryFrm, 
				bg = skin.myBlack )
			self.tabConnFltrCnt.grid( row = 2, column = 0 )

			self.connCntrFltrLbl = tk.Label(
				self.tabConnFltrCnt,
				text 	= "Filter:",
				bg 		= skin.myBlack,
				fg 		= skin.myLGrey,
				font 	= skin.provideFont("B") )
			self.connCntrFltrLbl.grid( row = 0, column = 0 )

			self.connCntrFilterTxt = tk.Entry(
				self.tabConnFltrCnt,
				bg 		= skin.myBlack,
				fg 		= skin.myLGrey,
				width 	= 10,
				font 	= skin.provideFont("B"),
				textvariable = self.connFltrStrVar )
			self.connCntrFilterTxt.grid( row = 0, column = 1 )


		#==============================================================
		# Things that go in the tabConnCityFrm (city selection widgets)
		# tabConnGridFrame( row = 0, column = 2 )
		###############################################################
		if True:
			self.tabConnCityFrm = tk.LabelFrame(
				self.tabConnGridFrame,
				text = "CITY",
				bg 	= skin.myLBlue, 
				fg 	= skin.myBlack,
				labelanchor = 'n',
				font = skin.provideFont(24) )
			self.tabConnCityFrm.grid( row = 0, column = 2, sticky = 'n', padx = 5, pady = 10 )

			self.selectServerCityLb = tk.Listbox(
				self.tabConnCityFrm,
				selectbackground= skin.myNGreen,
				background 		= skin.myBlack,
				foreground 		= skin.myLbxFG,
				width 			= 25,
				height 			= 9,
				selectmode  	= 'single',
				listvariable 	= self.connLB_CtyVar,
				font 			= skin.provideFont(14) )
			self.selectServerCityLb.configure( exportselection = False )			
			self.selectServerCityLb.bind( "<<ListboxSelect>>", self.updateSelectedCity )
			self.selectServerCityLb.grid( row = 0, column = 0, sticky = 'n' )

			self.tabConnCityClearBtn = tk.Button(
				self.tabConnCityFrm,
				font  	= skin.provideFont("B"),
				bg 		= skin.myBlack,
				fg 		= skin.myLGreen,
				text 	= "Reset city",				
				command = self.clearSelectedCity )
			self.tabConnCityClearBtn.grid( row = 1, column = 0 )


		############################################################################
		# Things that go in the self.tabConnActionsFrm (all selected values widgets)
		# tabConnGridFrame( row = 1, column = 0 )
		############################################################################

		if True:
			self.tabConnActionsFrm = tk.LabelFrame(
				self.tabConnGridFrame,
				text = "CONNECT",
				bg 	= skin.myBlack, 
				fg 	= skin.myNGreen,
				labelanchor = 'n',
				font = skin.provideFont(24) 
			)
			self.tabConnActionsFrm.grid( row = 1, column = 0, sticky = 'wens' )


			##########################################
			# Things that go in the tabConnActionsFrm
			# tabConnActionsFrm( row = 0, column = 0 )
			##########################################
			
			#===============================================================================
			# row 0: last connections listBox
			self.tabConnLastConnsFrm = tk.LabelFrame(
				self.tabConnActionsFrm,
				text = "Last 3 Connections",
				bg 	= skin.myBlack, 
				fg 	= skin.myNGreen,
				labelanchor = 'n',
				borderwidth = 5,				
				font = skin.provideFont(24) 
			)
			self.tabConnLastConnsFrm.grid( row = 0, column = 0, sticky = 'wens' )
			
			self.selectLastConnLb = tk.Listbox(
				self.tabConnLastConnsFrm,
				selectbackground= skin.myNGreen,
				background 		= skin.myBlack,
				foreground 		= skin.myLbxFG,
				width 			= 32,
				height 			= 4,
				selectmode  	= 'single',
				listvariable 	= self.connLB_ConnsVar,
				font 			= skin.provideFont(14) )
			self.selectLastConnLb.configure( exportselection = False )
			self.selectLastConnLb.bind( "<<ListboxSelect>>", self.updateSelectedLastConn )
			self.selectLastConnLb.grid( row = 0, column = 0, padx = 1, sticky = 'wens')

			#===============================================================================
			# row 1: selected connection values ( [group] country [city] )
			self.tabConnActnsRw1 = tk.LabelFrame(
				self.tabConnActionsFrm,
				text = "SELECTED:",
				bg 	= skin.myBlack, 
				fg 	= skin.myNBlue,
				labelanchor = 'n',
				borderwidth = 5,
				font = skin.provideFont(24) 
			)
			self.tabConnActnsRw1.grid( row = 1, column = 0, rowspan = 2, sticky = 'wens' )

			self.tabConnSelGrpLbl = tk.Label(
				self.tabConnActnsRw1,
				font = skin.provideFont(16),
				fg 	= skin.myLYellow,
				bg 	= skin.myBlack,
				text= nvpnT.chosenGroupManager('get') 
			)
			self.tabConnSelGrpLbl.grid( row = 0, column = 0 )

			self.tabConnSelCntryLbl = tk.Label(
				self.tabConnActnsRw1,
				font = skin.provideFont(16),
				fg 	= skin.myLYellow,
				bg 	= skin.myBlack,
				text = nvpnT.chosenCountryManager('get') 
			)
			self.tabConnSelCntryLbl.grid( row = 0, column = 1 )

			self.tabConnSelCtyLbl = tk.Label(
				self.tabConnActnsRw1,
				font = skin.provideFont(16),
				fg 	= skin.myLYellow,
				bg 	= skin.myBlack,
				text = nvpnT.chosenCityManager('get')
			)
			self.tabConnSelCtyLbl.grid( row = 0, column = 2 )

			#===============================================================================
			# row 3: Connect/disconnect buttons
			self.tabConnActnsRw0 = tk.LabelFrame(
				self.tabConnActionsFrm,
				text = "ACTIONS:",
				bg 	= skin.myBlack, 
				fg 	= skin.myNBlue,
				labelanchor = 'n',
				borderwidth = 5,
				font = skin.provideFont(24) 
			)
			self.tabConnActnsRw0.grid( row = 3, column = 0, sticky = 'wens' )

			self.tabConnDisConnectBtn = tk.Button(
				self.tabConnActnsRw0,
				font = skin.provideFont(18),
				bg 	= skin.myFalse, 
				fg 	= skin.myWhite,
				command = self.disConnect,
				text = "Disconnect" 
			)
			self.tabConnDisConnectBtn.grid( row = 0, column = 0, sticky = 'nw' )

			self.tabConnSelectionsConnStrBtn = tk.Button(
				self.tabConnActnsRw0,
				bg 	= skin.myWhite, 
				fg 	= skin.myBlack,
				command = self.makeConnection,
				font = skin.provideFont(15),
				text = "nordvpn connect" 
			)
			self.tabConnSelectionsConnStrBtn.grid( row = 0, column = 1, sticky = 'ne' )



		self.doLayOut()



	def refreshConnStatus(self):
		########################################################################
		# Thing that goes in the active connection status display 
		# tabConnGridFrame( row = 1, column = 1 )
		########################################################################
		try:
			self.tabConnActSttsFrm.grid_info()
			self.tabConnActSttsFrm.grid_forget()

		except Exception as e:
			print(f"Exception on self.tabConnActSttsFrm.grid_info() = {e}")

		finally:
			self.tabConnActSttsFrm = ConnStatusFrame( 
				self.tabConnGridFrame, 
				dimensions = [ 
					int( self.dimensions[0] * 0.40 ), 
					int( self.dimensions[1] * 0.40 )
				] 
			)
			self.tabConnActSttsFrm.grid( row = 1, column = 1, columnspan = 2, sticky = 'e' )



	def buildConStr(self):
		useFollowingFlags = True
		startStr = ""
		grp 	= nvpnT.chosenGroupManager('get')
		cntry 	= nvpnT.chosenCountryManager('get')
		cty 	= nvpnT.chosenCityManager('get')
		if len( grp ) > 0:
			startStr += f" -g { grp.lower() }"
			if grp.lower() in ['onion_over_vpn']:
				useFollowingFlags = False

		if ( useFollowingFlags ) and ( len( cntry ) > 0 ):
			startStr += f" { cntry.lower() }"

		if ( useFollowingFlags ) and ( len(grp) == 0 ) and ( len(cntry) > 0 ):
			startStr += f" { cty.lower() }"

		print(f"buildConStr: {startStr.strip()}")
		self.connectionConfig['selected']['cnnctnStr'] = startStr.strip()
		self.tabConnSelectionsConnStrBtn.configure( text = f"nordvpn connect\n{startStr}" )


	def continueMsg( self, strConnParams = "--<group> <country> <city>"):
		result = messagebox.askyesno(f"Confirm connection", f"Connect with:\n{strConnParams} ?")
		if result:
			print(f"continueMsg chose YES {result}")
			nvpnT.addToConns(strConnParams)
			return True
		else: 
			print(f"continueMsg chose NO {result}")
			return False


	def makeConnection( self ):
		# conStr isthe full command, we only need the parameters. Ignoring 'nordvpn connect ' using everything after
		conStr = self.connectionConfig['selected']['cnnctnStr']
		print(f"conStr from connectionConfig = {conStr}")
		if self.continueMsg(conStr):
			connectArr = [ value for value in conStr.split(' ') if value not in [ None, "", "\t", {}, [] ] ]
			print(f"makeConnection| --connectArr: { connectArr }")
			cnnRespArr = nvpnT.getNvpnItem("connect", connectArr )
			print(f"makeConnection| --cnnRespArr: {cnnRespArr}")
			time.sleep(0.5)
			nvpnT.addToConns( conStr )
			self.doLayOut()
		else:
			print(f"User cancelled connection")


	def disConnect( self ):
		sttsAtStart = nvpnT.getConnStatus()
		dCnnRespArr = nvpnT.getNvpnItem( 'disconnect' )
		print(f"disConnect: response |-> nordvpn disconnect =: { dCnnRespArr }<-|")
		inputDialog = dlgRating(self)
		self.wait_window(inputDialog.top)
		print(f"disConnect| --inputDialog.result: {inputDialog.result}")
		nvpnReply = nvpnT.getNvpnItem("rate",inputDialog.result)
		print(f"disConnect| --nvpnReply: {nvpnReply}")
		time.sleep(0.5)
		self.doLayOut()


	def updateSelectedGroup( self, event ):
		pickedGrp = ""
		if ( len( self.selectServerGroupLb.curselection() ) > 0 ):
			pickedGrp = event.widget.get( self.selectServerGroupLb.curselection()[0] )
			self.tabConnCityFrm.grid_forget()
			#self.connLB_CtyVar.set([])
			self.clearSelectedCity()
		else:
			self.tabConnCityFrm.grid( row = 0, column = 2, sticky = 'n', padx = 5, pady = 10 )

		print(f"pickedGrp: { pickedGrp}")
		nvpnT.chosenGroupManager( 'set', pickedGrp )
		self.tabConnSelGrpLbl.configure( text = pickedGrp )
		self.buildConStr()


	def updateSelectedCountry( self , event):
		pickedCntry = "" 
		if ( len( self.selectServerCountryLb.curselection() ) > 0 ):
			pickedCntry = event.widget.get( self.selectServerCountryLb.curselection()[0] )
		print(f"updateSelectedCountry.pickedCntry: { pickedCntry}")
		nvpnT.chosenCountryManager( 'set', pickedCntry )
		self.tabConnSelCntryLbl.configure( text = pickedCntry )
		self.connLB_CtyVar.set( nvpnT.cityListManager('get'))
		self.buildConStr()


	def updateSelectedLastConn(self, event ):
		pickedCntry = "" 
		if ( len( self.selectLastConnLb.curselection() ) > 0 ):
			pickedCntry = event.widget.get( self.selectLastConnLb.curselection()[0] )
		print(f"updateSelectedLastConn.pickedCntry: { pickedCntry}")
		nvpnT.chosenCountryManager( 'set', pickedCntry )
		self.tabConnSelCntryLbl.configure( text = pickedCntry )
		self.connLB_CtyVar.set( nvpnT.cityListManager('get'))
		self.buildConStr()


	def updateSelectedCity( self, event ):
		print(f"updateSelectedCity: called by { event.widget }")
		pickedCity = ""
		if ( len( self.selectServerCityLb.curselection() ) > 0 ):
			pickedCity = event.widget.get( self.selectServerCityLb.curselection()[0] )
		print(f"pickedCity: { pickedCity }")
		self.tabConnSelCtyLbl.configure( text = pickedCity )
		nvpnT.chosenCityManager( 'set', pickedCity )
		self.buildConStr()


	def clearSelectedGroup( self ):
		print(f"clearSelectedGroup: clicked")
		self.selectServerGroupLb.selection_clear(0, 'end')
		self.tabConnSelGrpLbl.configure(text="")
		nvpnT.chosenGroupManager( 'clear' )
		self.buildConStr()
		print(f"self.tabConnCityFrm.winfo_viewable(): { self.tabConnCityFrm.winfo_viewable() }")
		if not self.tabConnCityFrm.winfo_viewable():
			self.tabConnCityFrm.grid( row = 0, column = 2, sticky = 'n', padx = 5, pady = 10 )


	def clearSelectedCountry( self ):
		print(f"clearSelectedCountry: clicked")
		self.selectServerCountryLb.selection_clear(0, 'end')
		self.connCntrFilterTxt.delete(0, 'end')		
		self.tabConnSelCntryLbl.configure(text="")
		nvpnT.chosenCountryManager( 'clear' )
		self.connLB_CtyVar.set( nvpnT.cityListManager('get'))
		self.buildConStr()


	def clearSelectedCity( self ):
		print(f"clearSelectedCity: clicked")
		self.tabConnSelCtyLbl.configure( text = "" )
		self.selectServerCityLb.selection_clear(0, 'end')
		nvpnT.chosenCityManager( 'clear' )
		self.buildConStr()


	def activeConnStatus(self):
		self.connectionConfig['selected']['curConnStatus'] = nvpnT.getConnStatus()
		print(f"activeConnStatus| --curConnStatus: {self.connectionConfig['selected']['curConnStatus']}")
		return self.connectionConfig['selected']['curConnStatus']


	def liveCntrFilter( self, event, widget, somethingElse ):
		""" Catches the trace-bind of self.connFltrStrVar when called it receives 4 args none of them useful for me."""
		fltrText 	= self.connFltrStrVar.get()
		cntrArr 	= self.connectionConfig['lists']['cntry'].copy()
		cntrArrLen 	= len( cntrArr )
		self.connCntrFltrStr = fltrText
		print(f"liveCntrFilter fltrText: { fltrText } full cntrArr has { cntrArrLen } items.")

		if ( len( fltrText ) > 0 ):	
			fltrText = fltrText.lower()
			resCntr  = 0
			self.selectServerCountryLb.delete( 0, 'end' )

			for c in cntrArr :
				if fltrText in c.lower():
					resCntr += 1
					self.selectServerCountryLb.insert( 'end', c )

			print(f"liveCntrFilter returns listBox of { resCntr } of {cntrArrLen} hidden: { cntrArrLen-resCntr }")
			self.connCntrFltrLbl.configure( text = f"Filter ({ resCntr }):" )

		else:
			self.connLB_CntrVar.set( self.connectionConfig['lists']['cntry'] )
			self.connCntrFltrLbl.configure( text = f"Filter ({ cntrArrLen }):" )


	def doLayOut(self):
		## Check connectionConfig
		print(f"connectionConfig[0] selected: { self.connectionConfig['selected'] }")

		# Groups
		print(f"connectionConfig[1][0]  grps: { len(self.connectionConfig['lists']['grp']) }")
		if len(self.connectionConfig['lists']['grp']) > 0:
			self.connLB_GrpVar.set(self.connectionConfig['lists']['grp'])
		else:
			self.connLB_GrpVar.set([])


		# Countries
		print(f"connectionConfig[1][1] cntry: { len(self.connectionConfig['lists']['cntry']) }")
		if len(self.connectionConfig['lists']['cntry']) > 0:
			self.connLB_CntrVar.set(self.connectionConfig['lists']['cntry'])
		else:
			self.connLB_CntrVar.set([])

		# Cities
		print(f"connectionConfig[1][2]   cty: { len(self.connectionConfig['lists']['cty']) }")
		if len(self.connectionConfig['lists']['cty']) > 0:
			self.connLB_CtyVar.set(self.connectionConfig['lists']['cty'])
		else:
			self.connLB_CtyVar.set([])

		# Last Connections
		print(f"lastConnections: { len( nvpnT.allConsArr) }")
		if len( nvpnT.allConsArr) == 0:
			self.connLB_ConnsVar.set([])
		else:
			if len( nvpnT.allConsArr) >= 3:
				self.connLB_ConnsVar.set( nvpnT.allConsArr[0:3] )
			else:
				self.connLB_ConnsVar.set( nvpnT.allConsArr )


		self.tabConnDisConnectBtn.grid(row = 0, column = 0, columnspan = 1 )
		self.tabConnSelectionsConnStrBtn.grid( row = 0, column = 1, columnspan = 1 )

		self.refreshConnStatus()

		# Finalle draw the class grid frame
		self.tabConnGridFrame.grid( row = 0, column = 0 ) # , sticky = 'WENS' 

		print(f"TabConnections End of doLayOut")
