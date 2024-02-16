import hashlib
class Block:
    def _init_(self,creator,parent,transaction,depth):
        self.creator=creator
        self.transactions=transaction
        self.blockID=self.createID(self.transactions)
        self.parent=parent
        self.depth=depth
        
        
    def createID(self):
        transactionString=""+str(self.previous_blockID)
        for txn in self.transactions:
            transactionString+=txn
        sha=hashlib.sha256(transactionString.encode())
        return sha.hexdigest()
    
    def getblockID(self):
        return self.blockID