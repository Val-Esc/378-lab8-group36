import socket

def main():
    # Prompt the user to enter the IP address and port number
    ipaddress = input("Enter the IP address to bind to (e.g., 127.0.0.1 or press Enter for 0.0.0.0): ") or '0.0.0.0'
    port = int(input("Enter the port number to bind to (e.g., 12345): "))

    # Create a server socket
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the specified IP address and port
    serversocket.bind((ipaddress, port))

    # Listen for incoming connections (allow up to 5 clients in the queue)
    serversocket.listen(5)
    print(f"Server is listening on {ipaddress}:{port}...")

    # Accept an incoming connection
    incoming_socket, incoming_address = serversocket.accept()
    print(f"Connection from {incoming_address} has been established.")

    # Loop to handle communication with the client
    try:
        while True:
            # Receive data from the client (up to 1024 bytes)
            data = incoming_socket.recv(1024)

            if not data:
                print("No data received. Closing connection.")
                break

            # Decode and print received data from client
            received_message = data.decode()
            print(f"Received from client: {received_message}")

            # Convert the received message to uppercase
            response = received_message.upper()

            # Respond back to the client with the uppercase message
            incoming_socket.sendall(response.encode('utf-8'))

    except socket.error as e:
        print(f"Socket error: {e}")

    finally:
        # Close the incoming connection and server socket
        incoming_socket.close()
        serversocket.close()
        print("Connection closed.")


main()