#!/usr/bin/env python3
''' Standard shebang

Importing various libraries:
	socket
	ssl			unused for the purposes of this
	sys
	os
	time
	random	
	threading	handles actual functions
	base64		aliased as b64

configureable values:
	cnc				=>	IP of your CNC server
	cport				=>	port that your CNC server listens on
	scan_ip				=>	IP
	scan_port			=>	port 
	sport				=>	port to scan nearby IP's
	single_instance_port=>	Mirai specific function (need to research)
	strings				=>	a string for randomized http requests
	stop				=>	Flag used for thread controls and prevent simultaneous attacks from one bot
	scan				=>	Flag to allow scanner function to run on connection

send_back Function:	ip to send info to (cnc)
	

scanner Function:	Based on Mirai's scanner
	While indefinitely
		generated IP  (gip not used in this)
		try:
			make a socket for (hostname or IPv4 and TCP connections)
			Set socket options at TCP level to REUSEADDR
			set max timeout to 1 second
			socket connect to (ip, port to scan)
			close that socket conneciton

handle(sock):	a Command List that sends out threads to individual tasks.
	global stop will be used
	attack counter = 0
	send CNC server a 1337 msg
		This is to Verify the bot to the CNC server. Consider change login code for specific settings
	while True:
		read CNC message
		if empty return to the begining of the loop
		XOR decode the message
		if msg starts with !:
			try:
				Split the command into it's arguments:
					0 is the command
					1+ is the arguments
				if command is the predefined XOR encoded string command:
					check if there are attacks in the attack counter:
						set stop flag to True, which stops lingering attack threads
						attack counter reset to 0
					stop flag set to False for next threads
					for however many theads you want to dedicate to this attack:
						make a thread using your attacking function and start it
						attack counter incremented.
				elif for however many comamnds you want

				elif msg is STOP
					set stop to True
					attack counter reset
				elif msg is kill
					close CNC server socket connection
					return kill command to conn()
			except:
				pass: This is used to fill up the except block space
				
		Respond to CNC beacon request: get ping, send pong.
		back to top of loop

How it Runs:
	Dunder Check:
		Initialize and Conn()
	
	Conn():
		if NOT Windows
			Dameonize the Thread
				make child thread and exit parent thread
				change to root directory
				change permissions to 000, which means only world readable writable for file creation and opening as user
				make child thread and exit parent thread
				clears stdin, stdout buffer
				closes stdin, stdout, stderr

		global kill flag will be used
		set kill to False

		Make scan_th number of threads:
			Run Scanner() for each Thread
		Make a single_instance thread: Mirai Specific checks

		while True:
			try:
				socket IPv4 and TCP
					can reuseaddr
				socket connect to CNC server
				send socket to handle()
					This will stay inside handle until a return statement happens
						return happens on kill command or error in reading CNC msgs
				if a kill command was sent,
					resets stdin
					resets stdout
					resets stderr
					kill to true for any remaining threads that are open
					exit the loop and end program.
			except:
				wait for 1-60 seconds before trying again

	handle(sock):	a Command List that sends out threads to individual tasks.
		global stop will be used
		attack counter = 0
		send CNC server a 1337 msg
			This is to Verify the bot to the CNC server. Consider change login code for specific settings
		while True:
			read CNC message:
			if empty return to the begining of the loop
			XOR decode the message
			if msg starts with !:
				try:
					Split the command into it's arguments:
						0 is the command
						1+ is the arguments
					if command is the predefined XOR encoded string command:
						check if there are attacks in the attack counter:
							set stop flag to True, which stops lingering attack threads
							attack counter reset to 0
						stop flag set to False for next threads
						for however many theads you want to dedicate to this attack:
							make a thread using your attacking function and start it
						attack counter incremented.
					elif for however many comamnds you want

					elif msg is STOP
						set stop to True
						attack counter reset
					elif msg is kill
						close CNC server socket connection
						return kill command to conn()
				except:
					pass: This is used to fill up the except block space
				
				Respond to CNC beacon request: get ping, send pong.

'''
