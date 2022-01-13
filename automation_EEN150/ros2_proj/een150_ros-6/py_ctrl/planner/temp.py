from queue import PriorityQueue

# q = PriorityQueue()
# q.put((3, {"a": 1}))
# q.put((2, {"a": 1}))
# q.put((2, {"a": 1}))
# q.put((1, {"a": 1}))


# while not q.empty():
#     print(q.get())

import heapq

class MyHeap(object):
   def __init__(self, initial=None, key=lambda x:x):
       self.key = key
       self.index = 0
       if initial:
           self._data = [(key(item), i, item) for i, item in enumerate(initial)]
           self.index = len(self._data)
           heapq.heapify(self._data)
       else:
           self._data = []

   def push(self, item):
       heapq.heappush(self._data, (self.key(item), self.index, item))
       self.index += 1

   def pop(self):
       return heapq.heappop(self._data)[2]

initial_state = {"v1": False, "v2": 0}

h = MyHeap(key=lambda x: x[0])
h.push((7, initial_state))
h.push((2, initial_state))
h.push((2, initial_state))
h.push((4, initial_state))

while len(h._data) > 0:
    print(h.pop())