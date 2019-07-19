import socket
import select
import sys

hostname = socket.gethostbyname(socket.gethostname())
port = 9995
addr = (hostname, port)
online_socket_list = []
user_name_by_socket = {}


def establish_server():
    server_socket = socket.socket()
    server_socket.bind(addr)
    server_socket.listen(5)
    print("Host name:{0}\nPort:{1}".format(hostname, port))
    return server_socket


def deal_new_client(server_socket):
    welcome_words = 'Welcome to VinceJudge Room({0})'.format(hostname)
    client_socket, client_ip = server_socket.accept()
    print("{0} connect to the server.".format(client_ip[0]))
    try:
        client_socket.sendall(('\n' + welcome_words).encode())
        online_socket_list.append(client_socket)
        user_name_by_socket[client_socket] = client_ip[0]
    except Exception as e:
        print(e)


def run_a_new_server():
    server_socket = establish_server()
    online_socket_list.append(server_socket)
    END_server = False
    while True:
        active_socket_list, w, e = select.select(online_socket_list, [], [])
        for active_socket in active_socket_list:
            if active_socket is server_socket:
                deal_new_client(server_socket)
            else:
                disconnected = False
                try:
                    msg = active_socket.recv(1024).decode('utf-8')
                    if msg == "$exit":
                        msg = '{0} leave the room'.format(user_name_by_socket[active_socket])
                        disconnected = True
                    msg = '{0}: {1}'.format(user_name_by_socket[active_socket], msg)
                except socket.error:
                    msg = '{0} leave the room'.format(user_name_by_socket[active_socket])
                    disconnected = True
                for other_user_socket in online_socket_list:
                    if (other_user_socket is not server_socket) and (other_user_socket is not active_socket):
                        try:
                            other_user_socket.sendall(('\n' + msg).encode())
                        except Exception as e:
                            print(e)
                if disconnected:
                    online_socket_list.remove(active_socket)
                    del user_name_by_socket[active_socket]
                print(msg)
        if END_server:
            break
    return


if __name__ == '__main__':
    run_a_new_server()
