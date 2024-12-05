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




def query2(collection):
    waterConsum_readings = []
    query = {
        # identify the dishwasher using device ID
        "payload.parent_asset_uid": "47t-206-9t7-va5",
        # use data from past 2 hours to represent cycle
        "time": {"$gte": datetime.now() - timedelta(hours=2)}
    }
    projection = {
        # include data from water consumtion sensor only
        "payload.water-consm": 1,
        "_id": 0
    }
    # run the above query
    readings = collection.find(query, projection)
    # append the sensor readings into an array
    for reading in readings:
        waterConsum_readings.append(float(reading['payload']['water-consm']))
    average = 0
    #make sure values are in array to avoid dividing by 0
    if 0< len(waterConsum_readings):
        for i in waterConsum_readings:
            average += i
        average = average / len(waterConsum_readings)
    else:
        average = 0
    return average




def query3(collection):
    query_fridge1 = {
        # identify kitchen fridge using device ID
        "payload.parent_asset_uid": "yau-1te-5ms-zt3",
        # use data from past 20 minutes
        "time": {"$gte": datetime.now() - timedelta(minutes=20)}
    }
    projection_fridge1 = {
        # include data from ammeter sensor only
        "payload.ammeter-fridge1": 1,
        "_id": 0
    }
    query_fridge2 = {
        # identify the other fridge using device ID
        "payload.parent_asset_uid": "4ba9959b-0ae2-40ec-8888-ffa9bc1db6f6",
        # use data from past 20 minutes
        "time": {"$gte": datetime.now() - timedelta(minutes=20)}
    }
    projection_fridge2 = {
        # include data from ammeter sensor only
        "payload.ammeter-fridge2": 1,
        "_id": 0
    }
    query_washer = {
        # identify the dish washer using device ID
        "payload.parent_asset_uid": "47t-206-9t7-va5",
        # use data from past 20 minutes
        "time": {"$gte": datetime.now() - timedelta(minutes=20)}
    }
    projection_washer = {
        # include data from ammeter sensor only
        "payload.ammeter-wash": 1,
        "_id": 0
    }

    fridge1_readings = collection.find(query_fridge1, projection_fridge1)
    fridge2_readings = collection.find(query_fridge2, projection_fridge2)
    washer_readings = collection.find(query_washer, projection_washer)

    #make 3 arrays with the values of each ammeter
    f1 = []
    f2 = []
    wash = []
    for r in fridge1_readings:
        f1.append(float(r['payload']['ammeter-fridge1']))

    for r in fridge2_readings:
        f2.append(float(r['payload']['ammeter-fridge2']))

    for r in washer_readings:
        wash.append(float(r['payload']['ammeter-wash']))

    #get avearage of each ammeter
    if f1:
        fridge1_avr = sum(f1) / len(f1)
    else:
        fridge1_avr = 0
    if f2:
        fridge2_avr = sum(f2) / len(f2)
    else:
        fridge2_avr = 0
    if wash:
        washer_avr = sum(wash) / len(wash)
    else:
        washer_avr = 0

    #find device with highest power usage
    averages = [fridge1_avr, fridge2_avr, washer_avr]
    most_power = max(averages)
    if most_power == fridge1_avr:
        result = "Kitchen Fridge " + str(fridge1_avr)
        return result
    elif most_power == fridge2_avr:
        result = "Spare Fridge " + str(fridge2_avr)
        return result
    elif most_power == washer_avr:
        result = "Dish Washer " + str(washer_avr)
        return result 
    else:
        return 0
    


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
    
    db = client['test']
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
            query_choice = int.from_bytes(data, byteorder='big')
            print(f"Received from client: {query_choice}")
            
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
