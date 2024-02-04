import random 

class node:
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



        node_list.append(node(i+1,speed,cpu))

    return node_list