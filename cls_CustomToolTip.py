#!/usr/bin/env python3

########################################
#### 		cls_CustomToolTip.py 	####
#### 		Version 20250714 		####
########################################

import tkinter as tk
from tkinter import ttk

class CustomTooltip:

	def __init__(self, widget, text):
		self.widget = widget
		self.text = text
		self.tooltip_visible = False

		# Bind events to show/hide the tooltip
		widget.bind("<Enter>", self.show_tooltip)
		widget.bind("<Leave>", self.hide_tooltip)

	def show_tooltip(self, event):
		if not self.tooltip_visible:
			x, y, _, _ = self.widget.bbox("insert")
			x += self.widget.winfo_rootx() + 25
			y += self.widget.winfo_rooty() + 25

			self.tooltip_label = tk.Label(
				text 		= 	self.text, 
				background 	= 	"lightyellow", 
				relief 		= 	"solid", 
				borderwidth	=	1
			)
			self.tooltip_label.place(x=x, y=y)
			self.tooltip_visible = True


	def hide_tooltip(self, event):
		if self.tooltip_visible:
			self.tooltip_label.place_forget()
			self.tooltip_visible = False