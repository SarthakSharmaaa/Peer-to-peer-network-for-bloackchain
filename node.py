import random 
import time
import queue
import threading
import numpy as np

global_unique_transaction_id=1
failed=0

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

        self.thread_handler_mutex = threading.Lock()

        self.transaction_mutex = threading.Lock()
        
        self.flag=0

        self.t.start()

        

    def gen_time(self):
        exponential_dist = np.random.exponential(scale=2, size=100)
        exponential_dist = np.round(exponential_dist, decimals=1) #randomly generating transaction time
        gen=random.randint(0,99)
        return exponential_dist[gen]

    def start_check_queue(self):
        print("Thread for " + str(self.number) + " started")
        while True and self.flag==0:
            if self.transaction_queue.empty()==False:
                front_of_queue=self.transaction_queue.get()
                to_node=front_of_queue.split()[1]
                amount=front_of_queue.split()[2]
                self.transaction(int(to_node),int(amount))
                print("Added to transaction, sleeping ")
                time.sleep(self.gen_time())
                print("sleep done")
        print("thread " , self.number , " out")
        
    def stop_check_queue(self):
        print("Thread for " + str(self.number) + " stopped")
        if self.t.is_alive():
            print("alive")
        else:
            print("Dead")
        self.t.join(timeout=1)



    def thread_handler(self,to_node,amount):
        print("thread handler for "+ str(self.number))

        self.thread_handler_mutex.acquire()
        try:
            str_to_queue=str(self.number) + " " + str(to_node) + " " + str(amount)
            self.transaction_queue.put(str_to_queue)
        finally:
            self.thread_handler_mutex.release()
    
    def transaction(self,to_node,amount): 
            
            self.transaction_mutex.acquire()
            try:
                global global_unique_transaction_id
                global failed
                if self.coins-amount >=0 :
                    self.coins-=amount
                    transaction_string=str(global_unique_transaction_id)+" "+str(self.number)+" pays "+str(to_node)+" "+str(amount)+" coins"
                    global_unique_transaction_id+=1
                    self.transaction_list.append(transaction_string)
                    print("Transaction successful")
                else:
                    print("only have ",self.coins," but you trying to spend ",amount)
                    failed+=1
            finally:
                self.transaction_mutex.release()
    
    


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
        i.flag=1
        i.stop_check_queue()