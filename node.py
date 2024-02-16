import random 
import time
import queue
import threading
import numpy as np
import asyncio
from block import Block


global_unique_transaction_id=1


class Node:
    def __init__(self,number, speed, cpu,n):
        self.total_peers=n
        self.number=number
        if speed==1:
            self.speed = "slow"
        else:
            self.speed = "fast"
        
        if cpu==1:
            self.cpu = "low"
        else:
            self.cpu = "high"

        self.coins=random.randint(5000,7000)

        self.transaction_list=[]

        self.transaction_queue=queue.Queue()

        self.t = threading.Thread(target=self.start_check_queue)

        self.transaction_thread = threading.Thread(target=self.create_transactions)

        self.th = None

        self.thread_handler_mutex = threading.Lock()

        self.transaction_mutex = threading.Lock()

        self.transaction_spread_lock = threading.Lock()

        self.creation_mutex = threading.Lock()
        
        self.transaction_tracker=0
        
        self.flag=0

        self.loop_tracker=0

        self.to_node=0

        self.amount=0

        self.genesis = Block("start","initial",[],0)

        self.finalised_blocks=set(self.genesis)

        self.block_chain_dict={}
        
        self.block_chain_dict[self.genesis.blockID]=self.genesis.depth

        self.finalised_transactions = set()

        self.t.start()


    def create_block(self):
        max_depth_blockID = max(self.block_chain_dict, key=self.block_chain_dict.get)
        max_depth_value = self.block_chain_dict[max_depth_blockID]
        block_transactions=[]
        for txn in self.transaction_list:
            if txn in self.finalised_transactions:
                continue
            else:
                block_transactions.append(txn)

        b=Block(creator=self.number,parent=self.max_depth_blockID,transactions=block_transactions,depth=max_depth_value+1)
        for x in block_transactions:
            self.finalized_transaction.add(x)
        self.finalised_blocks[b.getblockID()]=max_depth_value+1


    def create_transactions(self):
        for self.loop_tracker in range(20):
            while True:
                self.to_node=random.randint(0,self.total_peers-1)  #transaction recieving node
                if self.to_node==self.number:
                    continue
                else:
                    break
            
            self.amount=random.randint(500,600) #amount spent

            self.thread_handler(self.to_node,self.amount)

    def random_time(self,t):
        exponential_dist = np.random.exponential(scale=t, size=100)
        exponential_dist = np.round(exponential_dist, decimals=1) #randomly generating transaction time
        gen=random.randint(0,99)
        return exponential_dist[gen]
    
    async def thread_sleep(self,t):
        t/=1000
        print("sleeping for " , t)
        await asyncio.sleep(t) 

    async def thread_sleep_transaction(self,t):
        t/=1000
        print("sleeping for " , t)
        await asyncio.sleep(t) 

    def simulate_thread_sleeping(self,neighbor,time_to_sleep,d):
        asyncio.run(self.thread_sleep(1)) 

        self.transaction_spread_lock.acquire()
        try:
            neighbor.transaction_list.append(d)
        finally:
            self.transaction_spread_lock.release()
            


    def simulate_latency(self,neighbor,d):
        #ρij + |m|/cij + dij

        p=5
        m=10
        c=0
        if self.speed == "fast" and neighbor.speed=="fast":
            c=100
        else:
            c=5
        val=96/c
        dij=self.random_time(val)
        time_to_sleep=p+(m/c)+dij

        self.th = threading.Thread(target=self.simulate_thread_sleeping, args=(neighbor,time_to_sleep,d))

        self.th.start()

        self.th.join()
        print("thread ",self.number ," stopped after transaction")

    

    def gen_time(self):
        exponential_dist = np.random.exponential(scale=2, size=100)
        exponential_dist = np.round(exponential_dist, decimals=1) #randomly generating transaction time
        gen=random.randint(0,99)
        return exponential_dist[gen]

    def start_check_queue(self):
        print("Thread for " + str(self.number) + " started")

        self.transaction_thread.start()
        self.transaction_thread.join()

        while True and (self.flag==0 or self.transaction_queue.empty()==False):
            if self.transaction_queue.empty()==False:
                front_of_queue=self.transaction_queue.get()
                to_node=front_of_queue.split()[1]
                amount=front_of_queue.split()[2]
                self.transaction(int(to_node),int(amount))
                print("Added to transaction, sleeping ")
                asyncio.run(self.thread_sleep_transaction(self.gen_time())) 
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
                if self.coins-amount >=0 :
                    self.coins-=amount
                    transaction_string=str(global_unique_transaction_id)+"_"+str(self.number)+" "+str(self.number)+" pays "+str(to_node)+" "+str(amount)+" coins"
                    global_unique_transaction_id+=1
                    self.transaction_list.append(transaction_string)
                    print("Transaction successful")
                else:
                    print("only have ",self.coins," but you trying to spend ",amount)
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



        node_list.append(Node(i+1,speed,cpu,n))


    return node_list

def StopNodes(nodes_list):
    print("initiated stop threads")
    for i in nodes_list:
        i.flag=1
        i.stop_check_queue()