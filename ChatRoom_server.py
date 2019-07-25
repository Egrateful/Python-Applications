#Server of Chatroom
from socket import *
import sys
import os
import signal

def do_login(s,users,name,addr):
	for i in users:
		if i == name or name == '管理員':
			s.sendto(b'FAIL',addr)
			return
	s.sendto(b'OK',addr)	
	#通知所有人有人登入
	msg = '\n welcome %s take part in the chat room'%name
	for i in users:
		s.sendto(msg.encode(),users[i])
	
	#將用户插入字典
	users[name] = addr	
	return	

def do_chat(s,users,tmp):
	msg ='\n%-4s: %s'%(tmp[1],' '.join(tmp[2:]))

	#轉發聊天內容給其它用戶, 除了發送者
	for i in users:
		if i != tmp[1]:
			s.sendto(msg.encode(),users[i])
	return

def do_quit(s,users,name):
	#將該用户從字典中刪除
	del users[name]
	msg = '\n' + name + " has left the chat room"
	
	#告知其它用戶哪一位用戶退出聊天室
	for i in users:
		s.sendto(msg.encode(),users[i])
	return

#receiving requests and process them
def do_child_task(s):
	#users directory {name:ADDR}
	users = {}
   
	while True:
		msg,addr = s.recvfrom(1024)
		msgList = msg.decode().split(' ')

		#determine the request types and process them
		if msgList[0] == 'L':
			do_login(s,users,msgList[1],addr)
		elif msgList[0] == 'C':
			do_chat(s,users,msgList)
		elif msgList[0] == 'Q':
			do_quit(s,users,msgList[1])


#sending system messages
def do_parent_task(s,addr):
	while True:
		msg = input("管理員消息:")
		msg = "C 管理員 " + msg 
		s.sendto(msg.encode(),addr)
	s.close()
	sys.exit()

def main():
	if len(sys.argv) != 3:
		print("argv error !")
		return
	
	HOST = sys.argv[1]
	PORT = int(sys.argv[2])

	#create the datagram socket
	s = socket(AF_INET,SOCK_DGRAM)
	s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
	ADDR = (HOST,PORT)
	s.bind(ADDR)

	#avoiding zombie child process 
	signal.signal(signal.SIGCHLD,signal.SIG_IGN)

	#create process
	pid = os.fork()
	if pid < 0:
		sys.exit("process creation failed !")
		
	elif pid == 0:
		do_child_task(s)		

	else:
		do_parent_task(s,ADDR)		

if __name__ == '__main__':
	main()