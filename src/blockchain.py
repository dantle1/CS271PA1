import hashlib
import datetime
import json

'''
Genesis Block
{
    index: 0,
    timestamp: current time,
    data: Transaction 1,
    previous_hash: "0"
} -> hash() -> 2343aaa

{
    index: 1,
    timestamp: current time,
    data: Transaction 2, 
    previous_hash: 2343aaa
} -> hash() -> 98723ffe

{
    index: 2,
    timestamp: current time,
    data: Transaction 3, 
    previous_hash: 98723ffe
}
'''

class Transaction:
    def __init__(self, sender, receiver, amount, logic_clock):
        self.sender_id : int = sender # id of sender client
        self.receiver_id : int = receiver # id of receiver client
        self.amount : float = amount # amount transferred
        self.logic_clock : int = logic_clock  # lamport logic clock
        self.timestamp : str = None 
        self.status : str = "Pending" # Pending, success, abort
    
    def to_tuple(self):
        return self.sender_id, self.receiver_id, self.amount


class Block:
    def __init__(self, transaction: Transaction, previous_hash=None):
        self.transaction : Transaction = transaction
        self.previous_hash : str = previous_hash if previous_hash else hashlib.sha256(''.encode()).hexdigest()
        self.next_block = None
    
    # hash the blockchain
    def hash(self):
        return hashlib.sha256(str(self).encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.bchain = [] # return 

    # turn transaction into block
    def create_block(self, transaction: Transaction, previous_hash=None):
        block = Block(transaction)
        return block

    # add transaction to blockchain
    def add_transaction(self, transaction):
        block = self.create_block(transaction)
        self.bchain.append(block)
        # recompute hash of blocks in blockchain
        self.chain.sort

        

