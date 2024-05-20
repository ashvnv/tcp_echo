#   ASHWIN VALLABAN
#   20 MAY 2024
#   THIS PROGRAM CAN BE USED TO ANALYZE THE CLIENT'S SOCKET PERFORMANCE.

import socket
import threading
import timeit
import time

#ECHO THE MESSAGE BACK TO THE SERVER
def echo(socket):
    while(1):
        #ECHO THE MESSAGE
        socket.sendall(socket.recv(1024))


#THIS FUNCTION WILL CALCULATE THE RTT
def rtt_calc(client_socket, addr, msg_head):

    rtt_max = 0 #MAXIMUM RTT

    try:
        
        #TOTAL PACKETS TO BE SENT TO SERVER
        for i in range(100):

            start_time = timeit.default_timer()

            #msg_head: LOOP <i>\r\n
            client_socket.sendall(f"{msg_head}: LOOP {i} \r\n".encode("utf-8"))

            #WAIT FOR RECEIVING THE MESSAGE
            client_socket.recv(1024).decode("utf-8")

            #CALCULATE THE ROUND-TRIP TIME
            rtt = (timeit.default_timer() - start_time) * 1000 #IN MS
            
            #ONLY PRINT THE MAXIMUM DELAY
            if rtt > rtt_max:
                rtt_max = rtt
                print(f"{msg_head}: RTT MAX: {rtt_max}")

            #time.sleep(1)  

        print(f"{msg_head}: EXECUTION COMPLETE")

    except Exception as e:
        print(f"Error when hanlding client: {e}")
    finally:
        client_socket.close()
        print(f"Connection to client ({addr[0]}:{addr[1]}) closed")


#THIS FUNCTION WILL KEEP RUNNING AND CREATE A NEW THREAD WHEN NEW CONNECTION IS ACCEPTED
def run_server():
    server_ip = "192.168.92.9"  # server hostname or IP address
    port = 8080  # server port number

    client_conn = 0; #TO IDENTIFY CLIENTS

    # create a socket object
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to the host and port
        server.bind((server_ip, port))
        # listen for incoming connections
        server.listen()
        print(f"Listening on {server_ip}:{port}")

        while True:
            # accept a client connection
            client_socket, addr = server.accept()
            print(f"Accepted connection from {addr[0]}:{addr[1]}")
            # start a new thread to handle the client
            
            #UNCOMMENT THE BELOW LINES TO ENABLE RTT CALCULATION
            #thread = threading.Thread(target=rtt_calc, args=(client_socket, addr, "THREAD " + str(client_conn)))
            #client_conn += 1 #INCREMENT CLIENT CONN BY 1

            #UNCOMMENT THE BELOW LINE TO ENABLE ECHO FUNCTION
            thread = threading.Thread(target=echo, args=(client_socket,))

            thread.start()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.close()


run_server()