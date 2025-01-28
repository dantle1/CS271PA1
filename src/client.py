import fastapi   # uses http & tcp by default
import grequests # async http requests
import socket
import threading 
import uvicorn
import os
import logging
import re
from blockchain import Blockchain, Transaction

# Delay for simulating time needed for message passing and demoing concurrent events
MESSAGE_DELAY = 3

class Client:
    
    def __init__(self, id, ipv4, port, server_address):
        self.id = id
        self.port = port
        self.ipv4 = ipv4
        self.server_address = server_address  # address of main bank server
        self.lamport_clock = 0  # lamport clock protocol
        self.bchain = Blockchain()  # each client keeps local log of transactions
        self.sending_queue : list[Transaction]= []  # queue of sent messages
        self.message_queue: list[Transaction] = [] # queue of processed messages

    '''
    Balance Transaction: 
    - return requesting client's balance
    - no mutex
    - No new node added to the blockchain
    '''

    def balance(self, transfer=False):
        # only update lamport clock if it is an isolated balance transaction
        if not transfer:
            self.lamport_clock += 1
        


    '''
    Transfer Transaction:
    - Lamport's Distributed Mutual Exclusion Protocol
    - once client gets mutex, verify balance is enough to issue transfer
        using local balance table
    - Case 1: Not enough money
        - abort transaction and release mutex
    - Case 2: Enough money 
        - insert transaction block at head of blockchain
        - send that block to all other clients
        - insert that block at head of blockchain of other clients
        - update local copy of balance table after inserting
        - release mutex
    '''
    def transfer_transaction(self):
        return

    def up(self):
        threading.Thread(target=uvicorn.run, args={
            'app' : app, 
            'ipv4' : self.ipv4,
            'port' : self.port}).start()
        

    '''
    User Interface:
    1. issue transfer/balance transactions to individual client
    2. Print "SUCCESS" or "FAILED" for transfer interactions
    3. Print balance returned from server for balance interactions
    4. Print client's blockchain w details of each block
    5. Print balance table containing balances of all clients

    '''
    def talk(self):
        self.command_list()
        while True:
            cmd = input('>>>').strip().lower()
            if re.match(, cmd):
                print('Exiting the client...')
                os._exit(0)
    
    def command_list(self):
        print('Hi, this is the blockchain client!')
        print('Commands:')
        print(' 1. transfer/t <recipient> <amount>: send <amount> to user with <recipient> id')
        print(' 2. balance/b: get current balance of account')
        print(' 3. blockchain/c: print contents of local blockchain')
        print(' 4. allinfo/a: print detailed info of client')
        print(' 5. messages/m: print message queues')
        print(' 6. exit/e')
        print(' 7. help/h')
        print('Enter one of the above commands: ')


if __name__ == '__main__':
    client = Client()