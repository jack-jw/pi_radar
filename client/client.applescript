-- Pi-radar client app

on flashSD()
	display alert "Not implemented"
end flashSD

on flashUSB()
	try
		set loaded to do shell script "ls /tmp/routes*.csv"
		set loaded to do shell script "echo " & quoted form of loaded & " | sed 's/.csv//g' "
		set loaded to do shell script "echo " & quoted form of loaded & " | sed 's/\\/tmp\\/routes//g' "
	on error
		display alert "No Route Databases Loaded" message "You must load at least one route database before flashing them to a USB disk."
		return
	end try
	display alert "Update Databases" message "Loaded route databases: " & return & loaded & return & return & "Ensure your USB disk is connected to this computer and is visible in Finder, and that you are connected to the Internet." buttons "Continue"
	
	-- Get disks
	set diskList to paragraphs of (do shell script "ls /Volumes/")
	
	-- Remove Time Machine disks
	set filteredDisks to {}
	repeat with disk in diskList
		if disk does not contain "Backups of " then
			set end of filteredDisks to disk
		end if
	end repeat
	
	-- Prompt user to select their USB disk
	set chosenDisk to choose from list filteredDisks with prompt "Select your USB disk" & return & "This all existing content on this disk will be removed. Please make a backup before continuing." default items {} without multiple selections allowed
	
	if chosenDisk is not false then
		set selectedDisk to item 1 of chosenDisk
		
		set diskFS to do shell script ("diskutil info /Volumes/" & quoted form of selectedDisk & " | grep 'File System Personality' | awk '/File System Personality/ {print $4}'")
		set diskParent to do shell script ("diskutil info /Volumes/" & quoted form of selectedDisk & " | grep 'Part of Whole' | awk '/Part of Whole/ {print $4}'")
		
		if diskFS is "MS-DOS" then
			set progress description to "Flashing to " & selectedDisk
			set progress additional description to "Formatting USB disk..."
			set progress total steps to 4
			set progress completed steps to 1
			
			set progress completed steps to 2
			do shell script "diskutil eraseDisk FAT32 PI-RADAR MBRFormat /dev/" & diskParent
			
			do shell script "mkdir /Volumes/PI-RADAR/.pi-radar; mv /tmp/routes*.csv /Volumes/PI-RADAR/.pi-radar/"
			set progress additional description to "Transferring your databases..."
			do shell script "echo 'Please insert this USB in to the Raspberry Pi running Pi-radar. This file will be deleted once your databases have been successfully transferred.' > /Volumes/PI-RADAR/README"
			set progress completed steps to 3
			
			do shell script "diskutil eject /Volumes/PI-RADAR"
			set progress additional description to "Unmounting disk..."
			set progress completed steps to 4
			
			set progress additional description to "Done"
			delay 1
			
			display alert "USB disk formatted with your databases" message "You may now safely remove the USB disk from your Mac and insert it in to the Raspberry Pi running Pi-radar." buttons "OK"
			
		else
			display alert "Incorrect Format" message (selectedDisk & " is formatted as " & diskFS & ". Please format it as MS-DOS (FAT) using Disk Utility to use it here.") buttons {"Quit", "Use Another Disk", "Open Disk Utility"} default button 2
			if the button returned of the result is "Open Disk Utility" then
				tell application "Disk Utility" to activate
			else if the button returned of the result is "Use Another Disk" then
				flashUSB()
			end if
		end if
	end if -- end if disk is MS-DOS
end flashUSB

on loadCustomRoutes()
	set customRoutes to choose file with prompt "Select the airline route database you would like to load" of type "csv"
	
	repeat
		try
			set callsign to the text returned of (display dialog "Enter the three-digit callsign of the airline" default answer "" with icon note buttons "Continue" default button 1)
			set callsign to do shell script "echo " & quoted form of callsign & " | tr '[:lower:]' '[:upper:]'"
			set maxLength to 20
			set callsign to text 1 thru 3 of callsign
			exit repeat
		on error
			display alert "Enter a three-character airline callsign"
		end try
	end repeat
	
	if callsign is "BAW" then
		display alert "Callsign Error" message "The British Airways route database is built in to Pi-radar." buttons {"Quit", "Add Another Airline"} default button 2
		return the button returned of the result
	else
		do shell script "cp " & quoted form of (POSIX path of customRoutes) & " /tmp/routes" & callsign & ".csv"
		display alert "Route Database Loaded" message "Your route database has been loaded. Please now flash it to a USB disk to transfer it to your Raspberry Pi." buttons {"Quit", "Add Another Airline", "Flash to USB Disk"} default button 3
		return the button returned of the result
	end if
end loadCustomRoutes

-- Main menu
set mainMenuReturn to the button returned of (display alert "Pi-radar" buttons {"Quit", "Add Route Databases", "Flash to SD Card"} default button 3)
if mainMenuReturn is "Flash to SD Card" then
	flashSD()
	
else if mainMenuReturn is "Add Route Databases" then
	set dbMenuReturn to the button returned of (display alert "Route Databases" message "Add route databases for any airline to see route information in Pi-radar." buttons {"Download Custom Routes Template", "Load Custom Routes", "Flash to USB Disk"} default button 3)
	
	if dbMenuReturn is "Flash to USB Disk" then
		flashUSB()
		
	else if dbMenuReturn is "Load Custom Routes" then
		set loop to "Add Another Airline"
		repeat while loop is "Add Another Airline"
			set loop to loadCustomRoutes()
		end repeat
		if loop is "Flash to USB Disk" then
			flashUSB()
		end if
	else if dbMenuReturn is "Download Custom Routes Template" then
		open location "https://github.com/yellowcress/pi-radar/raw/main/client/Route%20database%20template.numbers"
	end if -- end if dbMenu
	
end if -- end if mainMenu