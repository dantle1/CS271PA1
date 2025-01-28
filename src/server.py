import socket
import threading
import json
import hashlib
from blockchain import Blockchain, Transaction

# Server configuration
HOST = '127.0.0.1'
PORT = 65432

# Blockchain and balance table
blockchain = []
balance_table = {"Client1": 10, "Client2": 10, "Client3": 10}
lamport_clock = 0
request_queue = []  # Queue to hold requests in the form of (timestamp, client_id)

# Generate a hash for the block
def hash_block(block):
    block_string = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()

# Create a new block
def create_block(sender, receiver, amount, prev_hash):
    return {
        "sender": sender,
        "receiver": receiver,
        "amount": amount,
        "prev_hash": prev_hash
    }

# Add a transaction to the blockchain
def add_transaction(sender, receiver, amount):
    global blockchain, balance_table, lamport_clock
    if balance_table.get(sender, 0) < amount:
        return f"Transaction failed: {sender} has insufficient funds."

    # Deduct from sender and add to receiver
    balance_table[sender] -= amount
    balance_table[receiver] += amount

    # Add the transaction to the blockchain
    prev_hash = blockchain[-1]["hash"] if blockchain else "0"
    new_block = create_block(sender, receiver, amount, prev_hash)
    new_block["hash"] = hash_block(new_block)
    blockchain.append(new_block)
    return f"Transaction successful: {amount} transferred from {sender} to {receiver}."

# Handle client requests for mutual exclusion
def handle_request(client_socket, client_id, timestamp, request_type, *args):
    global lamport_clock, request_queue

    lamport_clock = max(lamport_clock, timestamp) + 1
    request_queue.append((timestamp, client_id))
    request_queue.sort()  # Sort requests by timestamp and then by client_id

    # Wait until this client's request is at the front of the queue
    while request_queue[0][1] != client_id:
        pass

    if request_type == "TRANSFER":
        sender, receiver, amount = args
        response = add_transaction(sender, receiver, int(amount))
    elif request_type == "BALANCE":
        response = json.dumps(balance_table, indent=2)
    elif request_type == "BLOCKCHAIN":
        response = json.dumps(blockchain, indent=2)
    else:
        response = "Unknown request type."

    # Remove the request from the queue after processing
    request_queue.pop(0)
    client_socket.sendall(response.encode() + b"\n")

# Handle client communication
def handle_client(client_socket, address):
    client_id = f"Client{address[1] % 3 + 1}"  # Map address to client ID
    print(f"Connected to {client_id} ({address})")
    client_socket.sendall(b"Welcome to the server! You can transfer money or check balances.\n")
    client_socket.sendall(b"Commands: BALANCE, TRANSFER <receiver> <amount>, BLOCKCHAIN\n")

    try:
        while True:
            data = client_socket.recv(1024).decode().strip()
            if not data:
                print(f"Connection closed by {client_id}")
                break

            # Extract request type and arguments
            lamport_clock += 1  # Increment Lamport clock for each client message
            if data.upper() == "BALANCE":
                request_type = "BALANCE"
                args = ()
            elif data.upper().startswith("TRANSFER"):
                parts = data.split()
                request_type = "TRANSFER"
                args = (client_id, parts[1], parts[2])
            elif data.upper() == "BLOCKCHAIN":
                request_type = "BLOCKCHAIN"
                args = ()
            else:
                client_socket.sendall(b"Unknown command.\n")
                continue

            # Process the request with Lamport mutual exclusion
            thread = threading.Thread(target=handle_request, args=(client_socket, client_id, lamport_clock, request_type, *args))
            thread.start()

    except Exception as e:
        print(f"Error with {client_id}: {e}")
    finally:
        client_socket.close()

# Main server logic
def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(3)
    print(f"Server running on {HOST}:{PORT}, waiting for clients...")

    try:
        while True:
            client_socket, address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
            client_thread.start()
    except KeyboardInterrupt:
        print("\nServer shutting down.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
