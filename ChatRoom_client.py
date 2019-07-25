#Client of Chatroom
from socket import *
import sys
import os
import signal

#send requests and messages
def sending_task(s,addr,name):
	while True:
		text = input("Your message:")
		if text == 'quit':
			#用户欲退出聊天室
			msg = 'Q ' + name
			s.sendto(msg.encode(),addr)
			#stop the parent process
			os.kill(os.getppid(),signal.SIGKILL)
			sys.exit(0)
		#chatting in normal situation 
		else:
			msg = 'C %s %s'%(name,text)
			s.sendto(msg.encode(),addr)

#receive requests and messages
def receving_task(s):
	while True:
		msg,addr = s.recvfrom(1024)
		print(msg.decode() + "\nYour message: ",end="")	


def main():
	if len(sys.argv) != 3:
		print("argv error !")
		return
	HOST = sys.argv[1]
	PORT= int(sys.argv[2])
	ADDR = (HOST,PORT)	

	#create the datagram socket
	s = socket(AF_INET,SOCK_DGRAM)
	s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)

	while True:
		name = input("please enter name:")
		msg ='L '+ name
		s.sendto(msg.encode(),ADDR)
		data,addr = s.recvfrom(1024)
		if data.decode() == 'OK':
			break
		else:
			print("This user has existed already!")	


	#avoiding zombie child process 
	signal.signal(signal.SIGCHLD,signal.SIG_IGN)

	#create process
	pid = os.fork()
	if pid < 0:
		print("process creation failed !")
		return

	elif pid == 0:
		sending_task(s,ADDR,name)

	else:
		receving_task(s)		

if __name__ == '__main__':
	main()