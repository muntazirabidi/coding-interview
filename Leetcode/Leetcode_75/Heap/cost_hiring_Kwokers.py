'''
You are given a 0-indexed integer array costs where costs[i] is the cost of hiring the ith worker.

You are also given two integers k and candidates. We want to hire exactly k workers according to the following rules:

You will run k sessions and hire exactly one worker in each session.
In each hiring session, choose the worker with the lowest cost from either the first candidates workers or the last candidates workers. Break the tie by the smallest index.
For example, if costs = [3,2,7,7,1,2] and candidates = 2, then in the first hiring session, we will choose the 4th worker because they have the lowest cost [3,2,7,7,1,2].
In the second hiring session, we will choose 1st worker because they have the same lowest cost as 4th worker but they have the smallest index [3,2,7,7,2]. Please note that the indexing may be changed in the process.
If there are fewer than candidates workers remaining, choose the worker with the lowest cost among them. Break the tie by the smallest index.
A worker can only be chosen once.
Return the total cost to hire exactly k workers.
'''

from typing import List, Set

class Solution:
    def totalCost(self, costs: List[int], k: int, candidates: int) -> int:
    # We'll use two heaps - think of them as two organized groups
    # of candidates we're currently considering
    import heapq
    front_heap = []  # People we can see from the front
    back_heap = []   # People we can see from the back
    
    # These pointers help us keep track of where we're looking in the line
    front = 0                  # First person we haven't looked at from front
    back = len(costs) - 1      # Last person we haven't looked at from back
    
    # First, let's look at our initial candidates
    # Look at 'candidates' number of people from front
    for i in range(candidates):
        if front <= back:  # Make sure we don't look at same person twice
            heapq.heappush(front_heap, (costs[front], front))
            front += 1
    
    # Look at 'candidates' number of people from back
    for i in range(candidates):
        if front <= back:  # Again, avoid overlap
            heapq.heappush(back_heap, (costs[back], back))
            back -= 1
    
    total_cost = 0  # Keep track of total hiring cost
    
    # Now, let's hire k people
    for _ in range(k):
        # Who has the lower cost - someone from front or back?
        # Remember to handle case where one group is empty
        
        # If front group is empty, hire from back
        if not front_heap:
            cost, index = heapq.heappop(back_heap)
            total_cost += cost
            if front <= back:  # If there are more people to look at
                heapq.heappush(back_heap, (costs[back], back))
                back -= 1
                
        # If back group is empty, hire from front
        elif not back_heap:
            cost, index = heapq.heappop(front_heap)
            total_cost += cost
            if front <= back:  # If there are more people to look at
                heapq.heappush(front_heap, (costs[front], front))
                front += 1
                
        # If both groups have people, compare them
        else:
            # Look at cheapest person from each group
            front_cost = front_heap[0][0]  # Cost of cheapest front person
            back_cost = back_heap[0][0]    # Cost of cheapest back person
            
            # Hire the cheaper one (or front if equal)
            if front_cost <= back_cost:
                cost, index = heapq.heappop(front_heap)
                total_cost += cost
                if front <= back:
                    heapq.heappush(front_heap, (costs[front], front))
                    front += 1
            else:
                cost, index = heapq.heappop(back_heap)
                total_cost += cost
                if front <= back:
                    heapq.heappush(back_heap, (costs[back], back))
                    back -= 1
    
    return total_cost