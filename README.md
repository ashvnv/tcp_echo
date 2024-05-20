# tcp_echo

### server.py: 
This program will create a new thread each time a client establishes a connection to the specified port. 
### client.py: 
This program will create specified number of clients and connect to the specified server's port.

### Both the above program can call the following two functions:
  - echo() - The program will reply with the same string.
  - rtt_calc() - The program will send a number of strings to the connected network device and calculate the maximum time it takes to receive the sent message from the connected device.
