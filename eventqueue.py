import heapq

class Event:
    def __init__(self,timestamp,eventid):
        self.timestamp=timestamp
        self.eventid=eventid
        
    def __lt__(self, other):
        return self.timestamp < other.timestamp

event_queue=[]       

heapq.heappush(event_queue,Event(timestamp=10,eventid=2))
heapq.heappush(event_queue,Event(timestamp=4,eventid=33))

first=heapq.heappop(event_queue)
print(first.eventid)
second=heapq.heappop(event_queue)
print(second.eventid)

