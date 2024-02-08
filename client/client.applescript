-- Pi-radar Utility

-- Main menu
set mainMenuReturn to the button returned of (display alert "Pi-radar" buttons {"Quit", "Manage Databases", "Flash to SD Card"} default button 3)
if mainMenuReturn is "Flash to SD Card" then
	display alert "Not implemented"
	
else if mainMenuReturn is "Manage Databases" then
	set dbMenuReturn to the button returned of (display alert "Manage Databases" buttons {"Download Custom Routes Template", "Load Custom Routes CSV", "Update Databases"} default button 3)
	
	if dbMenuReturn is "Update Databases" then
		display alert "Update Databases" message "Ensure your USB disk is connected to this computer and is visible in Finder, and that you are connected to the Internet." buttons "Continue"
		
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
		set chosenDisk to choose from list filteredDisks with prompt "Select your USB disk" default items {} without multiple selections allowed and empty selection allowed
		
		if chosenDisk is not false then
			set selectedDisk to item 1 of chosenDisk
			
			set diskFS to do shell script ("diskutil info /Volumes/" & quoted form of selectedDisk & " | grep 'File System Personality' | awk '/File System Personality/ {print $4}'")
			set diskParent to do shell script ("diskutil info /Volumes/" & quoted form of selectedDisk & " | grep 'Part of Whole' | awk '/Part of Whole/ {print $4}'")
			
			if diskFS is "MS-DOS" then
				display alert ("Erase & Format Disk") message ("The entirety of the disk, including any other partitions within it, will be erased and formatted. Please remove any important data from " & selectedDisk & " before proceeding. This may take a while, do not close this application, remove the disk or turn off your computer. This action cannot be undone.") buttons {"Cancel", ("Erase & Format " & selectedDisk)} default button 1
				if the button returned of the result is not "Cancel" then
					
					set progress total steps to 6
					set progress description to "Erasing and formatting disk..."
					
					set progress completed steps to 0
					
					set progress additional description to "Downloading callsigns database..."
					set callsignFetcherPath to POSIX path of (path to resource "callsigns.py" in bundle (path to application "Pi-radar")) as string
					do shell script "python3 '" & callsignFetcherPath & "'"
					set progress completed steps to 1
					
					set progress additional description to "Downloading British Airways route database..."
					set routesBAWPath to POSIX path of (path to resource "routesBAW.py" in bundle (path to application "Pi-radar")) as string
					do shell script "python3 '" & routesBAWPath & "'"
					set progress completed steps to 2
					
					set progress additional description to "Downloading airframes database..."
					do shell script "cd ~/Downloads; curl -o /tmp/airframes.csv https://opensky-network.org/datasets/metadata/aircraftDatabase.csv"
					set progress completed steps to 3
					
					set progress additional description to "Formatting USB disk..."
					do shell script "diskutil eraseDisk FAT32 PIRADAR MBRFormat /dev/" & diskParent
					set progress completed steps to 4
					
					set progress additional description to "Transferring files..."
					do shell script "mkdir /Volumes/PIRADAR/.pi-radar; mv /tmp/callsigns.csv /Volumes/PIRADAR/.pi-radar/; mv /tmp/routes*.csv /Volumes/PIRADAR/.pi-radar/; mv /tmp/airframes.csv /Volumes/PIRADAR/.pi-radar/"
					
					do shell script "echo 'Please insert this USB in to the Raspberry Pi running Pi-radar. This file will be deleted once the databases have been successfully transferred.' > /Volumes/PIRADAR/README"
					set progress completed steps to 5
					
					set progress additional description to "Unmounting disk"
					do shell script "diskutil eject /Volumes/PIRADAR"
					set progress completed steps to 6
					
					set progress additional description to "Done"
					delay 1
					
					display alert "USB disk formatted with databases" message "You may now safely remove the USB disk from your Mac and insert it in to the Raspberry Pi running Pi-radar." buttons "OK"
					
				end if
			else
				display alert "Incorrect Format" message (selectedDisk & " is formatted as " & diskFS & ". Please format it as MS-DOS (FAT) using Disk Utility to use it here.") buttons {"Quit", "Open Disk Utility"} default button 2
				if the button returned of the result is not "Quit" then
					tell application "Disk Utility" to activate
				end if
				
			end if -- end if disk is MS-DOS
			
		end if -- end if disk exists
		
	else if dbMenuReturn is "Load Custom Routes CSV" then
		
		set customRoutes to choose file with prompt "Select the custom airline route database you would like to load" of type "csv"
		
		set callsign to the text returned of (display dialog "Enter the three-digit callsign of the airline" default answer "" with icon note buttons "Continue" default button 1)
		
		if callsign is "BAW" then
			display alert "Callsign Error" message "The British Airways routes database is built in to Pi-radar."
		else
			do shell script "cp " & quoted form of (POSIX path of customRoutes) & " /tmp/routes" & callsign & ".csv"
			display alert "Route Database Loaded" message "Your route database has been loaded. Please now update the databases to transfer it to your Raspberry Pi."
		end if
		
	else if dbMenuReturn is "Download Custom Routes Template" then
		open location "https://github.com/yellowcress/pi-radar/raw/main/client/Custom%20route%20database%20template.numbers"
		
		
	end if -- end if dbMenu
	
end if -- end if main menu