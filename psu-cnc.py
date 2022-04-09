#!/usr/bin/env python3
'''
Standard python3 shebang

Import Python Libraries:
    socket  for server interactiosn
    threading
    os
    time
    sys
    base64      aliased as b64
    random

Global configurations:
    shutdown    flag to shutdown server
    count       as counter of bots that executed cnc command
    dead        as counter of offline bots (didn't respond to socket)
    socketList  as list of open sockets () representing each client connection
    key         as an xor key (Look up XOR cipher)

ReadSocket Function: uses socket and length of of message
    data = empty string
    while it is empty,
        socket receives message from client
            decodes while ignoring errors
                strips padding (A fix)
        data += that message
    returns data

ReadLine Function: uses socket and length of message
	Unused by program

SentCmd Function: data to send, socket, and the thread lock
    will use global variables: socketList, count, and dead
    rlock tells this thread lock the following resources from access
        To prevent Race Condition
    try:
        sets maximum time to run socket function as 1 second.
        send bit encoded data as utf-8
        counter incremented for each successfull sent command
    except:
        On failure to send to specific bot
        close that socket
        remove socket from list
        dead incremented for each offline bot
    release rlock to allow for next thread to use resources

SendCmd function: cmd as string
        

How it Runs:
	Duneder Check:
		if there are more or less than 2 arguments, it will provide error feedback
		try:
			saving the port number as an integar into variable b.
		except:
			error feedback if the second argument cannot be saved as an integer
		
		rlock make a thread lock
		sendout a thread to call main with rlock argument as a daemon
			daeomon will continue outside this below loop as a separate thread.
		while 1:
			try:
				checks every 0.1 second to see if the shutdown command is received
					if it has it will exit
			except:
				Ctrl C or X will also break the running script.

	main(rlock):
		Make a daemon thread for listen_scan()
		s = socket with IPv4 and TCP
			reuseaddr option
			keepalive option
		bind to 0.0.0.0 on port b (argv[1])
		listen for any connection to current IP
		while 1:
				socket, addr = accept new socket connections
				Make daemon thread to Verify() if it's a bot.

	Verify:
		data = ReadSocket(): Read data
		print data
		Check if it is recognized code (1337)
			if socket is not in my socket list
				lock up resources to other threads from changing it
				append socket onto socketList
				release thread lock
				handle_bot(socket, socketlist, rlock)
		else:
			telnet server side
			commander(socket, rlock)
	
	handle_bot(socket, socketlist, rlock):
		while True:
			try:
				set max timeout to try socket function to 1 second
				send ping out to bot
				set max timeout to try socket function is 2 seconds
				receive msg from bot
				if msg == pong:
					try again in 15 seconds
				else:
					try:
						close socket
						lock thread resources
						remove socket from socketlist
						release lock
					except:
						break out of loop.
			except pass

	Commander(socket, rlock): A psuedo Telent server
		try:
			check for username
			check for password
		except:
			return to main() thread and eventually close
		grab login credentials from login.txt
		correct number flag
		for each line in text file:
			split line into username and pass
			if both name and pass mathc:
				correct login
		if correct counter isn't 1:
			close socket
			return to Verify(), which returns to Main() to accept the next socket connection.

		"setting up server" as a fancy ascii graphic.
			sends to commander on socket connection
		
		make daemonized thread for ShowBot

		while True:
			Psuedo-shell: name @ Aoyama
			cmd_str = ReadSocket(	Commander.socket,	1024 bytes).lower() if you are careless
			if len(cmd_str) isn't 0:
				if command starts with !:
					SendCmd(cmd_str, sock, rlock)
				if scan:		Active scan for extra devices
					scan_device(rlock,) < trailing comma common code practice in python. dunno why
				if help:
					give out help screen
						should give out cmd list with proper args
						!stop
						!kill
						bots
						scan
						clear
						exit
						shutdown
				if bots:
					send length of socketlist
				if clear:
					sends clear screen string	"\033[2J
					moves cursor to top			"\033[1H"
					sends fancy AOYAMA ascii graphic
				if exit:
					closes commander socket connection, not the server
				if shutdown:
					closes commander socket connection
					use global shutdown flag
					set shutdown to true
						closes all daemonized threads
					sys.exit()
				back to begining of loop

	ShowBot(socket):
		while True:
			try:
				sets Terminal window name update on len of socketlist
			except:
				return

	scan_device()
		will ping update all sockets in socketlist
			if they do not respond
				updates socketlist
				increment dead counter
	
	SendCmd(cmd, socket, rlock):
		use global count and dead
		XOR encodeds cmd
		set count to 0
		set dead to 0
		th_list		as	List of Threads
		for each client in socketList:
			th	=	thread for SentCmd with the client socket
			start that thread
			append onto th_list
		for each thread in th_list
			wait until all threads terminate (task completion or otherwise)
		prints out who died to terminal
		prints out who lived to terminal
		sends to Commander the number of bots who executed the command
		scan_device(rlock) to check bot status
	
	SentCmd(data, sock, rlock):
		use global variables: socketList, count, dead
		thread lock resources
		try:
			max timeout for socket attempt at 1 sec
			send data to client
			count incremented
		except:
			close that client socket
			remove that client from the socketList
			dead incremented
		release thread locked resources

'''
