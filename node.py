import random 
import time
import queue
import threading


class Node:
    def __init__(self,number, speed, cpu):
        self.number=number
        if speed==1:
            self.speed = "slow"
        else:
            self.speed = "fast"
        
        if cpu==1:
            self.cpu = "low"
        else:
            self.cpu = "high"

        self.coins=random.randint(1000,2000)

        self.transaction_list=[]

        self.transaction_queue=queue.Queue()

        self.t = threading.Thread(target=self.start_check_queue)

        self.mutex = threading.Lock()

        self.t.start()



        self.flag=1

    def gen_time(self):
        return 2

    def start_check_queue(self):
        print("Thread for " + str(self.number) + " started")
        while True:
            if self.transaction_queue.empty()==False and self.flag==1:
                front_of_queue=self.transaction_queue.get()
                to_node=front_of_queue.split()[1]
                amount=front_of_queue.split()[2]
                self.transaction(int(to_node),int(amount))
                print("Added to transaction, sleeping for 2 seconds")
                time.sleep(self.gen_time())
                print("sleep done")
        
    def stop_check_queue(self):
        print("Thread for " + str(self.number) + " stopped")
        if self.t.is_alive():
            print("alive")
        else:
            print("Dead")
        self.t.join(timeout=1)
    

    def gen_time(self):
        print(str(self.number)+" sleeping")
        return 1



    def thread_handler(self,to_node,amount):
        print("thread handler for "+ str(self.number))
        str_to_queue=str(self.number) + " " + str(to_node) + " " + str(amount)
        self.transaction_queue.put(str_to_queue)


    
    def transaction(self,to_node,amount): 
        
        if self.coins-amount >=0 :
            self.coins-=amount
            transaction_string=str(self.number)+" pays "+str(to_node)+" "+str(amount)+" coins"
            self.transaction_list.append(transaction_string)
            print("Transaction successful")
        else:
            print("only have ",self.coins," but you trying to spend ",amount)
    
    


def CreateNodes(n,z0,z1):
    node_list=[]

    z0=int(z0)
    z1=int(z1)
    n=int(n)

    slow=int((z0/100)*n)
    fast=n-slow

    low=int((z1/100)*n)
    high=n-low

    for i in range(int(n)):
        speed = 0
        cpu = 0

        gen1=random.randint(1,2)
        gen2=random.randint(1,2)

        if gen1==1:
            if slow>0:
                speed=1
                slow-=1
            else:
                speed=2
                fast-=1
        else:
            if fast>0:
                speed=2
                fast-=1
            else:
                speed=1
                slow-=1

        if gen2==1:
            if low>0:
                cpu=1
                low-=1
            else:
                cpu=2
                high-=1
        else:
            if high>0:
                cpu=2
                high-=1
            else:
                cpu=1
                low-=1



        node_list.append(Node(i+1,speed,cpu))


    return node_list

def StopNodes(nodes_list):
    print("initiated stop threads")
    for i in nodes_list:
        i.flag=0
        i.stop_check_queue()