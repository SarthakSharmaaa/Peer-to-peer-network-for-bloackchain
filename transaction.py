from datetime import datetime

class Transaction:
    def __init__(self, sender, receiver, coins):
        self.transaction_id = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
        self.sender= sender
        self.receiver= receiver
        self.amount = amount

    def __str__(self):
        return transactionID+": "+str(sender)+" pays "+str(receiver)+" "+str(amount)+" coins"
    
class CoinBaseTransaction:
    def __init__(self,receiver, coins):
        self.transaction_id = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
        self.receiver= receiver
        self.amount = amount

    def __str__(self):
        return transactionID+":"+str(receiver)+" mines "+str(amount)+" coins"


    
    