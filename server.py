import socket
from pymongo.mongo_client import MongoClient
from datetime import datetime, timedelta


def query1(collection):
    moistureSensor_readings = []
    query = {
        #identify kitchen fridge using device ID
        "payload.parent_asset_uid": "yau-1te-5ms-zt3",
        #use data from past 3 hours
        "time": {"$gte": datetime.now() - timedelta(hours=3)}
    }
    projection = {
        #include data from moisture meter sensor only
        "payload.moistureMeter-fridge1": 1,
        "_id": 0
    }
    #run the above query
    readings = collection.find(query, projection)
    #append the sensor readings into an array
    for reading in readings:
        moistureSensor_readings.append(float(reading['payload']['moistureMeter-fridge1']))

    average = 0
    if 0 < len(moistureSensor_readings):
        for i in moistureSensor_readings:
            average = average + i
        average = average / len(moistureSensor_readings)
    else:
        average = 0
    return average

def query2():

def query3():


def main():

    uri = "mongodb+srv://val123:val123@cluster0.pvx8w.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    
    # Create a new client and connect to the server
    client = MongoClient(uri)
    
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB database End-to-End-IoT!")
    except Exception as e:
        print(e)
    
    #access collection
    collection = db.loTFrig_virtual

    
    # Prompt the user to enter the IP address and port number
    ipaddress = input("Enter the IP address to bind to (e.g., 127.0.0.1 or press Enter for 0.0.0.0): ") 
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
            query_choice = data.decode()
            print(f"Received from client: {received_message}")
            
            if query_choice == 1:
                response = query1(collection)
            elif query_choice == 2:
                response = query2(collection)
            elif query_choice == 3:
                response = query3(collection)


            # Respond back to the client with query result
            incoming_socket.sendall(response.encode('utf-8'))

    except socket.error as e:
        print(f"Socket error: {e}")

    finally:
        # Close the incoming connection and server socket
        incoming_socket.close()
        serversocket.close()
        print("Connection closed.")


main()
