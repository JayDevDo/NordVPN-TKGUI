#!/usr/bin/env python3

############################################
#### 		cls_Frm_MyTable.py 			####
#### 		Version 20250506 	grid	####
############################################

import tkinter as tk
import myTheme as skin

class TkTable( tk.Frame ):

	def __init__(	
			self, 
			master = None, 
			title = "", 
			colHeaders = [], 
			data = [] , 
			dimensions = [ 400, 400 ]
		):

		super().__init__(master)
	
		self.master = master
		self.grid()
		self.configure( background = skin.myBlack )
		self.title = title
		self.dimensions = dimensions

		self.hasTitle = ( len( self.title ) > 2 )

		self.colHeaders 	= colHeaders
		self.colHeadersLen 	= len( self.colHeaders ) 
		self.colSpan 		= max( 2, self.colHeadersLen )

		self.colWidths = [ int( self.dimensions[0] / 2.66 ), int( self.dimensions[0] / 1.6 ),100,100,100,100,100,100 ]
		self.colSticky = [ "e", "w" ,"e", "e", "e", "e" ]

		self.tkTableData = data
		self.tkTableDataLen = len( self.tkTableData ) 

		self.firstDataRow = 0

		# Main container frame 
		self.tkTable = tk.Frame( 
			self, 
			bg 		= skin.myBlack, 
			width 	= int( self.dimensions[0] * 0.975 ),
			height 	= int( self.dimensions[1] * 0.975 )
		)

		"""
		print(
			f"myTkTable called with dimensions: { dimensions }\n" + 
			f"title: { self.hasTitle } ({self.title})\n" +
			f"headers: {self.colHeadersLen }\n" +
			f"self.tkTableDataLen: {self.tkTableDataLen}"
		)
		"""

		self.doLayout()


	def doLayout( self ):

		# Row 0 Title
		if self.hasTitle:
			self.lbl_title = tk.Label( 
				self.tkTable, 
				text = self.title, 
				bg = skin.myWhite,
				fg = skin.myBlack,
				font = skin.provideFont(20)
			)
			self.lbl_title.grid( 
				row = 0, 
				column = 0, 
				columnspan = self.colSpan,
				sticky = 'WE'
			)
			self.firstDataRow = 1
			# print(f"self.firstDataRow After Tilte = {self.firstDataRow}")

		# Row 1 Column labels if provided
		if ( len( self.colHeaders ) > 0 ):

			# print(f"Adding colHeaders: { str( self.colHeaders ) }")

			for h, hdrText in enumerate( self.colHeaders ):
				hdr = tk.Label(
					self.tkTable,
					text= str( self.colHeaders[h] ),
					bg 	= skin.myBlack,
					fg 	= skin.myNBlue,
					borderwidth = 1,
					# width = self.colWidths[h],
					font = skin.provideFont("H")
				)
				hdr.grid( row = self.firstDataRow, column = h )

			self.firstDataRow += 1 
			# print(f"self.firstDataRow After colHeaders = { self.firstDataRow }")

		# Table data
		if self.tkTableDataLen > 0 :
			# print(f"self.tkTableData:{self.tkTableData} | self.tkTableData[0]:{ self.tkTableData[0] }")
			if self.tkTableData[0] == "No data":
				print("Empty table")
			else:
				for r, dataRow in enumerate( self.tkTableData ):
					# print(f"This data row {r} has { len(dataRow) } items")
					curFrmRow = r + self.firstDataRow
					# print(f"DATA curRow = {curFrmRow} | r={r} | firstDataRow: { self.firstDataRow }")
					for c, rowItem in enumerate( dataRow ):
						# print(f"In row[{r}] the rowItem {c} has value { rowItem }")
						cell = tk.Label(
							self.tkTable,
							text 	= str( self.tkTableData[r][c] ),
							bg 		= skin.myBlack,
							fg 		= skin.myWhite,
							font 	= skin.provideFont("N"),
							borderwidth = 2
							#,padx 	= 5,pady 	= 5
						)
						cell.grid( row = curFrmRow,	column = c, sticky = self.colSticky[c] )

		# Finally draw the Table
		self.tkTable.grid( row = 0, column = 0) 
		#,columnspan = self.colSpan,rowspan = 1, sticky = 'WENS'
