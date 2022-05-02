from concurrent.futures import thread
import socket
import threading
from queue import Queue

def Send(group, send_queue):
    print('Thread Send Start')
    while True:
        try:
            recv = send_queue.get()
            if recv == 'Group Changed':
                print('Group Changed')
                break

            for conn in group:
                msg = 'Client' + str(recv[2]) + ' || ' + str(recv[0])
                if recv[1] != conn:
                    conn.send(bytes(msg.encode()))
                else:
                    pass
        except:
            pass

def Recv(conn, count, send_queue):
    print('Thread Recv' + str(count)+'Start')
    while True:
        data = conn.recv(1024).decode()
        send_queue.put([data, conn, count])


if __name__=='__main__':
    send_queue = Queue()
    HOST = ''
    PORT = 9000
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((HOST, PORT))
    server_sock.listen(10)
    count = 0
    group = []
    while True:
        count = count + 1
        conn, addr = server_sock.accept()
        group.append(conn)
        print('Connected' + str(addr))

        if count > 1:
            send_queue.put('Group Changed')
            thread1 = threading.Thread(target=Send, args=(group, send_queue,))
            thread1.start()
            pass
        else:
            thread1 = threading.Thread(target=Send, args=(group, send_queue,))
            thread1.start()

        thread2 = threading.Thread(target=Recv, args=(conn, count, send_queue,))
        thread2.start()