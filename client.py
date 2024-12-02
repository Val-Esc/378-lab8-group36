import socket

def query_options():
  print("1. What is the average moisture inside my kitchen fridge in the past three hours?")
  print("2. What is the average water consumption per cycle in my smart dishwasher?")
  print("3. Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?")
  print()
  query = int(input("Please select a query number: "))

  while query not in {1,2,3}:
    print("Sorry, this query cannot be processed. Please try one of the following:")
    print()
    print("1. What is the average moisture inside my kitchen fridge in the past three hours?")
    print("2. What is the average water consumption per cycle in my smart dishwasher?")
    print("3. Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?")
    print()
    query = int(input("Please select a query number: "))
  return query

#try to establish connection to server with TCP socket
success = 'n'
while success == 'n':
  try:
    serverIP = input("Enter server IP address: ").strip()  # prompt user for server IP address
    serverPort = int(input("Enter server port number: ")).strip()  # prompt user for server port number

    myTCPSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # establish TCP socket
    myTCPSocket.connect((serverIP, serverPort)) #attempt to connect TCP socket with server Ip address and port number
    success = 'y'
  except:
    print("IP address or port number entered incorrectly") #error message if connection failed
    success = 'n'


continue_Client = 'y'
  
while continue_Client == 'y':
  query = query_options() #get the user's query pick (1,2,or 3)
  myTCPSocket.send(query.to_bytes(1, byteorder='big')) #send pick as an integer to server

  serverResponse = myTCPSocket.recv(1024).decode('utf-8') #recieve server response as letters
  print("Server response: ", serverResponse) #display server capital message response

  continue_Client = input("Would you like to process another query? (y/n):") #ask to continue with another query
  if continue_Client == 'y':
    query = query_options()
  
myTCPSocket.close()

