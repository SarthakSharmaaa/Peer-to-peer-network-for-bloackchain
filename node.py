import random 
import time
import queue
import threading
import numpy as np
import asyncio
from block import Block
from datetime import datetime



global_unique_transaction_id=1


class Node:
    def __init__(self,number, speed, cpu,n, z0,z1,pij):

        #Parameters used to initialize a node consisting of various data structures and variables


        self.pij=pij

        self.z0=z0
        self.z1=z1

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

        self.block_thread = threading.Thread(target=self.create_block)

        self.block_simulation = None

        self.th = None

        self.the= None

        self.thread_handler_mutex = threading.Lock()

        self.transaction_mutex = threading.Lock()

        self.transaction_spread_lock = threading.Lock()

        self.transaction_block_spread_lock = threading.Lock()
        
        self.block_attach_mutex = threading.Lock()

        self.creation_mutex = threading.Lock()
        
        self.flag=0

        self.loop_tracker=0

        self.to_node=0

        self.amount=0

        self.genesis = Block(creator="start",parent="initial",transactions=["genesis"],create_time_stamp=0)

        self.block_chain = {self.genesis.blockID:self.genesis}

        self.longest_chain = self.genesis.blockID

        self.longest_chain_depth = 1 

        self.add_block_list = []

        self.semaphore=0

        self.flag_block = 0 

        self.flag_block_simulation = 0

        self.t.start()


    def simulate_latency_block_list(self):

        # BLocks from the add block list are correctly added to the correct parent if current parent doesnt exist then the block waits infinitely untill the parent node is received

        while True and self.flag_block_simulation==0 and len(self.add_block_list)>0:
            for i in self.add_block_list:
                if i.parent in list(self.block_chain.keys()):
                    self.block_chain[i.blockID]=i
                    self.set_longest_path(i)
                    
                    self.add_block_list.remove(i)




    def interarrival_blocks(self,z1,blockInterval):

        # THis function is used to calculate the interarrival time between 2 blocks of a node if it is a low cpu or a high cpu using hashing power 
        fast=int(z1*self.total_peers/100)
        slow=self.total_peers-fast

        slowInterarrival=blockInterval*(9*fast+slow)
        fastInterarrival=blockInterval*(9*fast+slow)/10
        if self.cpu == "high":
            return int(fastInterarrival)
        else:
            return int(slowInterarrival)

    async def inter_block_sleep(self,z1,tx):


        t=self.interarrival_blocks(z1,tx)
        t/=1000
        await asyncio.sleep(t)


    def trigger_block_creation(self):

        # this triggers the block creation thread to start creating the threads
        self.block_thread.start()
        self.block_thread.join()

    def attach_block(self,node,block):

        # When a node gets the broadcasted block it add the block to the node's local blockchain in the proper order to maintain consistency

        self.simulate_latency_block(node,block)


        node.block_simulation = threading.Thread(target=self.simulate_latency_block_list)

        node.block_simulation.start()


        node.block_simulation.join()
        

        
    def set_longest_path(self,block):

        # It is used to calculate the longest chain depth in the local blockchain
        
        count=1

        id=block.blockID

        while id!=self.genesis.blockID:
            count+=1
            id=self.block_chain[id].parent

        if self.longest_chain_depth<count:
            self.longest_chain_depth=count
            self.longest_chain=block.blockID
            
        

    def create_block(self):
        
        #This function is used to create the block by a node when it has to create between the interarrival time.
        while True and self.flag_block==0:
            
            self.semaphore=1
            check_transaction_list=[]
            id=self.longest_chain
            while id!=self.genesis.blockID:
                check_transaction_list.extend(self.block_chain[id].transactions)
                id=self.block_chain[self.block_chain[id].parent].blockID

            transaction_to_append=[]
            count=0

            for i in self.transaction_list:
                if i not in check_transaction_list:
                    count+=1
                    transaction_to_append.append(i)
                    if(count==(len(self.transaction_list)/2)):
                        break
            
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

            new_block = Block(self.number,self.longest_chain,transaction_to_append,current_time)

            self.longest_chain = new_block.blockID

            self.longest_chain_depth+=1

            self.block_chain[new_block.blockID]=new_block
            

            self.semaphore = 0 

            asyncio.run(self.inter_block_sleep(self.z1,2) )

            if len(self.transaction_list)==len(check_transaction_list):
                break


    def create_transactions(self):

        #It will create the transaction by the node.
        for self.loop_tracker in range(100):
            while True:
                self.to_node=random.randint(0,self.total_peers-1)  #transaction recieving node
                if self.to_node==self.number:
                    continue
                else:
                    break
            
            self.amount=random.randint(500,600) #amount spent

            self.thread_handler(self.to_node,self.amount)

    def random_time(self,t):

        # This function is used to get the exponential and unifor time distribution to simulate latencies between 2 nodes i and j

        exponential_dist = np.random.exponential(scale=t, size=100)
        exponential_dist = np.round(exponential_dist, decimals=1) #randomly generating transaction time
        gen=random.randint(0,99)
        return exponential_dist[gen]
    
    async def thread_sleep(self,t):
        t/=1000
        await asyncio.sleep(t) 

    async def thread_sleep_transaction(self,t):
        t/=1000
        await asyncio.sleep(t) 

    async def block_sleep(self,t):
        t/=1000
        await asyncio.sleep(t) 

    


    def simulate_thread_sleeping_block(self,neighbor,time_to_sleep,block):

        # IT is used to simulate block waiting period of a block
        asyncio.run(self.block_sleep(time_to_sleep)) 

        self.transaction_block_spread_lock.acquire()
        try:
            neighbor.add_block_list.append(block)
        finally:
            self.transaction_block_spread_lock.release()
            


    def simulate_latency_block(self,neighbor,block):
        #ρij + |m|/cij + dij

        # it is used to simulate latency in the block

        m=1024*8
        c=0
        if self.speed == "fast" and neighbor.speed=="fast":
            c=10000000
        else:
            c=500000
        val=96000/c
        dij=self.random_time(val)
        time_to_sleep=self.pij+(m/c)+dij

        self.the = threading.Thread(target=self.simulate_thread_sleeping_block, args=(neighbor,time_to_sleep,block))

        self.the.start()

        self.the.join()


    def simulate_thread_sleeping(self,neighbor,time_to_sleep,d):

        # it is used to simulate transactions between 2 nodes
        asyncio.run(self.thread_sleep(time_to_sleep))

        self.transaction_spread_lock.acquire()
        try:
            neighbor.transaction_list.append(d)
        finally:
            self.transaction_spread_lock.release()
            


    def simulate_latency(self,neighbor,d):
        #ρij + |m|/cij + dij
        # it is used to simulate latency in the transaction

        m=1024*8
        if self.speed == "fast" and neighbor.speed=="fast":
            c=10000000
        else:
            c=500000
        val=96000/c

        dij=self.random_time(val)
        time_to_sleep=self.pij+(m/c)+dij

        self.th = threading.Thread(target=self.simulate_thread_sleeping, args=(neighbor,time_to_sleep,d))

        self.th.start()

        self.th.join()

    

    def gen_time(self):

        # THis is used to create exponential distribution between blocks and transactions
        exponential_dist = np.random.exponential(scale=2, size=100)
        exponential_dist = np.round(exponential_dist, decimals=1) #randomly generating transaction time
        gen=random.randint(0,99)
        return exponential_dist[gen]

    def start_check_queue(self):

        #It is used to check wether any transaction has been received by the node so it can be added to the transaction pool
        self.transaction_thread.start()
        self.transaction_thread.join()

        while True and (self.flag==0 or self.transaction_queue.empty()==False):
            if self.transaction_queue.empty()==False:
                front_of_queue=self.transaction_queue.get()
                to_node=front_of_queue.split()[1]
                amount=front_of_queue.split()[2]
                self.transaction(int(to_node),int(amount))
                asyncio.run(self.thread_sleep_transaction(self.gen_time())) 

        
        
    def stop_check_queue(self):
        self.t.join(timeout=1)

        # It will stop the busy while loop checking of the start_check_queue



    def thread_handler(self,to_node,amount):

        self.thread_handler_mutex.acquire()
        try:
            str_to_queue=str(self.number) + " " + str(to_node) + " " + str(amount)
            self.transaction_queue.put(str_to_queue)
        finally:
            self.thread_handler_mutex.release()

        #It is used to handle the threads created for creating transactions
    
    def transaction(self,to_node,amount): 
            
            self.transaction_mutex.acquire()
            try:
                global global_unique_transaction_id
                if self.coins-amount >=0 :
                    self.coins-=amount
                    transaction_string=str(global_unique_transaction_id)+"_"+str(self.number)+" "+str(self.number)+" pays "+str(to_node)+" "+str(amount)+" coins"
                    global_unique_transaction_id+=1
                    self.transaction_list.append(transaction_string)
            finally:
                self.transaction_mutex.release()

            # It basically defines the structure of the transaction.
    
    


def CreateNodes(n,z0,z1,pij):
    
    # It is used to crwate nodes slow/fast, low cpu/fast cpu etc
    
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



        node_list.append(Node(i+1,speed,cpu,n,z0,z1,pij))


    return node_list

def StopNodes(nodes_list):
    # It is used to set the flag so the threads can exist the busy loop
    for i in nodes_list:
        i.flag=1
        i.stop_check_queue()

def CreateBlocks(graph):

    # It is the function that will trigger the threads in all the nodes so that it will start creating the blocks

    for i in graph:
        i.trigger_block_creation()

def StopBlockCreation(graph):

        # It is used to set the flag so the threads can exist the busy loop

    for i in graph:
        i.flag_block=1

def StopCheckList(graph):

    # It is used to set the flag so the threads can exist the busy loop


    for i in graph:
        i.flag_block_simulation=1
        
        

def Print_chain(graph):

    # it is used to check and print the blockchain

    for i in graph:
        for j,l in i.block_chain:
            print(j,l,"------------")

def handleList(fin_graph):

    # It is used to trigger the thread that will simulate the latencies between the blocks
    for i in fin_graph:
        i.simulate_latency_block_list()
