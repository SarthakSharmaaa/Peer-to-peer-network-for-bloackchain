from datetime import datetime
import hashlib
import json

class Block:
    def __init__(self,blockID,previous_block_hash,transactions):
        self.blockID=blockID
        self.previous_block_hash=previous_block_hash
        self.timestamp=datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
        self.transactions=transactions
        
    def __str__(self):
        return f"Block ID: {self.block_id}\nPrevious Block ID: {self.prev_block_id}\nTimestamp: {self.timestamp}\nTransactions: {self.transactions}"
def hash_creater(block):
    block_string = json.dumps(block.__str__(), sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()

def transaction_validator_and_node_updater(transaction,sender, receiver):
    if sender.balance >= transaction.amount:
        sender.balance -= transaction.amount
        receiver.balance += transaction.amount
        return True 
    else:
        return False
    


genesis_block = Block(0, None, [])

