import socket
import threading
import select
import sys

def connect_to_server(addr):
	server_socket = socket.socket()
	server_socket.connect(addr)
	return server_socket

def listen_to_server(server_socket):
	listening = [server_socket]
	while True:
		active_socket_list,w,e = select.select(listening,[],[])
		if server_socket in active_socket_list:
			try:
				print(server_socket.recv(1024).decode('utf-8'))
			except socket.error as e:
				print(e,' Failed to recieve message from server.')

def send_to_server(server_socket):
	while True:
		try:
			print('>>>',end='')
			msg = input()
			if(msg=='$exit'):
				server_socket.sendall(msg.encode())
		except Exception as e:
			print(e)
		try:
			server_socket.send((msg).encode())
		except Exception as e:
			print(e)

if __name__ == '__main__':
	server_ip = input('Server IP:')
	server_port = int(input('Server Port:'))
	print('\n')
	server_socket = connect_to_server((server_ip,server_port))
	listen_thr = threading.Thread(target=listen_to_server,args=(server_socket,))
	send_thr = threading.Thread(target=send_to_server,args=(server_socket,))
	listen_thr.start()
	send_thr.start()