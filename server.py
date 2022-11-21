# Python program to implement server side of chat room. 
import socket 
import select 
import sys 
import _thread
import time
import progressbar
from _thread import *


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

if len(sys.argv) != 3: 
    print ("Correct usage: script, IP address, port number")
    exit() 
 
IP_address = str(sys.argv[1]) 
Port = int(sys.argv[2]) 
  
server.bind((IP_address, Port))

with open('cracker.log','w') as f:
    print('Binded server to address :',IP_address,'and port :',Port, file=f)

server.listen() 

password_hash = input("hash of password is: ")
hash_type = input("Choose hash type: ")

if hash_type not in ['md5','sha']:
    print('Choose between md5 or sha')
    exit()

max_poss_time_client = 250

with open('cracker.log','a') as f:
    print('Hash of password is',password_hash,'of hash type',hash_type, file=f)

list_of_clients = dict()
faulty = []
start = 1
num_per_client = 10000000
found = False

def clientthread(conn, addr):
    global found
    global max_poss_time_client
    global faulty

    message = list_of_clients[conn]  
    message = str(message).encode()
    conn.send(message)
    count = 0
    
    while found == False:
            
            if count > 5 * max_poss_time_client:
                
                faulty.append(list_of_clients[conn])
                conn.close()
                list_of_clients.pop(conn)
                
                with open('cracker.log','a') as f:
                    print('Closed',conn,'because was taking more than threshold time', file=f)
                break

            try:
                conn.settimeout(0.1)
                message = conn.recv(2048) 
                
                if message: 
                    message = message.decode()
                    
                    if message.split(':')[0] == "Password found":
                        password = message.split(':')[1]

                        # if check(Password) == False:
                        #     faulty.append(list_of_clients[conn])
                        #     conn.close()
                        #     list_of_clients.pop(conn)
                
                        #     with open('cracker.log','a') as f:
                        #         print('Closed',conn,'because gave wrong password')
                        #     break

                        with open('cracker.log','a') as f:
                            print(conn,'said password is',password, file=f)
                        
                        print('\n\nFinal password :',password)
                        found = True
                        stop()
                        
                        server1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        server1.connect((IP_address, Port))
                        server1.close()
                        
                        break

                    elif found == False:
                        global start
                        
                        count = 0
                        
                        if len(faulty) == 0:
                            list_of_clients[conn] = start 
                            start += num_per_client
                        
                        else:
                            list_of_clients[conn] = faulty[0]
                            del faulty[0]                         

                        with open('cracker.log','a') as f:
                            print('Sending',conn,'start value',list_of_clients[conn], file=f)
                        
                        message = list_of_clients[conn] 
                        message = str(message).encode()
                        conn.send(message)
                    
                    else:
                        break
  
                else: 
                    count+=1
                    print('here')
                    pass 

            except Exception as e:

                pass
            
            count+=1
    
    exit()
    
  

def stop(): 
    
    message = 'stop'
    
    with open('cracker.log','a') as f:
        print('Stopping all clients', file=f)
    
    for clients in list_of_clients: 
        
        try: 
            message = message.encode()
            clients.send(message) 
        
        except: 
            clients.close() 

# def check(password): 
    
#     with open('cracker.log','a') as f:
#         print('Checking password',password,'with other clients')
    
#     for clients in list_of_clients: 
        
#         try: 
#             message = ("check:"password).encode()
#             clients.send(message)    
        
#         except: 
#             clients.close() 


def show_percentage():
    global start
    
    max_pass_length = 4
    No_of_possibilities = (93 ** (max_pass_length + 1) - 93)/92
    bar = progressbar.ProgressBar(maxval=No_of_possibilities, \
            widgets=[progressbar.Bar('*'), '', progressbar.Percentage()])
    bar.start()
    while(found == False):
        if start < No_of_possibilities:
            bar.update(start)
            time.sleep(1)
    bar.finish()

start_new_thread(show_percentage,())

while found == False: 
    conn, addr = server.accept()

    if(found == True):
        with open('cracker.log','a') as f:
            print ("Closing server", file=f)
        break
    
    conn.send((password_hash+':'+hash_type).encode())
    
    
    
    if len(faulty) == 0:
        list_of_clients[conn] = start 
        start = start + num_per_client
    
    else:
        list_of_clients[conn] = faulty[0]
        faulty.pop(index=0)
    
    with open('cracker.log','a') as f:
        print (conn,"connected with start value", list_of_clients[conn], file=f)
        
    start_new_thread(clientthread,(conn,addr))     

conn.close()
server.close() 
