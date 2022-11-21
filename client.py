# Python program to implement client side of chat room.
import socket
import select
import sys
from utility_func import *
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:
	print ("Correct usage: script, IP address, port number")
	exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.connect((IP_address, Port))
flag = 0 
total_per_client = 10000000

while True:

	# maintains a list of possible input streams
	sockets_list = [sys.stdin, server]
	read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])
	# found_password = ""
	found = False

	for socks in read_sockets:
		# print(socks, server)
		if socks == server:
			
			message = socks.recv(2048)
			message = message.decode()
			
			if flag == 0:
			
				password = message.split(':')[0]
				hash_type = message.split(':')[1]
				flag = 1
			
			elif message == "stop":
				# server.close()
				found = True
				break
			
			else:
				
				if message.isnumeric() == False:
					server.close()
					found = True
					break
				
				interval = []
				interval.append(int(message))
				interval.append(int(message) + total_per_client)
				found_password = funcClient(interval, password, hash_type)
				
				if found_password == "":
					message = "Request:"
				
				else:
					message = "Password found:" + found_password
				
				server.send(message.encode())
		
		else:
			continue
	if found == True:
		break
# print("Break")
server.close()