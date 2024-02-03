from datetime import datetime

def transaction_generator(sender, receiver, amount):
    transactionID = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
    return transactionID+": "+str(sender)+" pays "+str(receiver)+" "+str(amount)+" coins"

# print(transaction_generator(2020, 2021, 5))
# print(transaction_generator(2022,2023,8))


# “TxnID: IDx pays IDy C coins”
    
    