#!/usr/bin/env python3

########################################
#### 	nvpnSettingsCommands.py 	####
#### 	Version 20250506 	grid	####
########################################

"""
	Because nordvpn displays settings differently from the setting-item being used.
	The 'item' is nordvpn display value
	The 'value' is what we use to change the setting.
"""

nvpnCommandsArray = [
	{ 
		'item':"Threat_Protection_Lite",
		'value': "threatprotectionlite"
	},
	{ 
		'item':"LAN_DISCOVERY",
		'value': "lan-discovery"
	},
	{ 
		'item':"VIRTUAL_LOCATION",
		'value': "virtual-location"
	},
	{ 
		'item':"POST-QUANTUM_VPN",
		'value': "pq"	
	},
	{
		'item':"AUTO-CONNECT",
		'value': "autoconnect"		
	}
]

"""
	With version NordVPN Version 3.20
	=================================
	Technology: NORDLYNX
	Firewall: enabled
	Firewall Mark: 0xe1f1
	Routing: enabled
	Analytics: disabled
	Kill Switch: disabled
	Threat Protection Lite: disabled
	Notify: disabled
	Tray: disabled
	Auto-connect: disabled
	IPv6: disabled
	Meshnet: disabled
	DNS: disabled
	LAN Discovery: disabled
	Virtual Location: enabled
	Post-quantum VPN: disabled
	=================================
"""
