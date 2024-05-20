#   ASHWIN VALLABAN
#   20 MAY 2024
#   THIS PROGRAM CAN BE USED TO ANALYZE THE SERVERS'S SOCKET PERFORMANCE.

import socket
import threading
import timeit

#ECHO THE MESSAGE BACK TO THE SERVER
def echo(socket):
    while(1):
        #ECHO THE MESSAGE
        socket.sendall(socket.recv(1024))
    

#THIS FUNCTION WILL CALCULATE THE RTT
def rtt_calc(socket, msg_head):

    rtt_max = 0 #MAXIMUM RTT
        
    #TOTAL PACKETS TO BE SENT TO SERVER
    for i in range(100):

        start_time = timeit.default_timer()

        #msg_head: LOOP <i>\r\n
        socket.sendall(f"{msg_head}: LOOP {i} \r\n".encode("utf-8"))

        #WAIT FOR RECEIVING THE MESSAGE
        socket.recv(1024).decode("utf-8")

        #CALCULATE THE ROUND-TRIP TIME
        rtt = (timeit.default_timer() - start_time) * 1000 #IN MS

        #ONLY PRINT THE MAXIMUM DELAY
        if rtt > rtt_max:
            rtt_max = rtt
            print(f"{msg_head}: RTT MAX: {rtt_max}")

        #time.sleep(1)  

    print(f"{msg_head}: EXECUTION COMPLETE")

#THIS FUNCTION WILL CREATE THREADS EACH TIME IT IS CALLED
def client_thread(server_ip, server_port, msg_head):
    # create a socket object
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_ip, server_port))

        #UNCOMMENT THE BELOW LINE TO ENABLE RTT CALCULATION
        rtt_calc(client_socket, msg_head);
    
        #UNCOMMENT THE BELOW LINE TO ENABLE ECHO FUNCTION
        #echo(client_socket)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

#CALL THIS TO RUN THE CLIENT PROGRAM
def run_client():

    server_ip = "192.168.92.9"  # replace with the server's IP address
    server_port = 8080  # replace with the server's port number

    #NUMBER OF CLIENTS TO BE MADE
    for i in range(10):
        # start a new thread to handle the client
        thread = threading.Thread(target=client_thread, args=(server_ip, server_port, "THREAD " + str(i)))
        thread.start()
        #server_port += 1


run_client()

#WAIT FOR THE THREADS TO COMPLETE EXECUTION
while(1):
    pass