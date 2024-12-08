from minheap import MinHeap
      
class MaxHeap:
    def __init__(self):
        self.min_heap = MinHeap()
    
    def insert(self, value):
        # Insert negative value into min heap
        self.min_heap.insert(-value)
    
    def remove_max(self):
        # Remove minimum (which is negative of our maximum) and negate it
        min_val = self.min_heap.remove_min()
        return -min_val if min_val is not None else None
    
    def peek_max(self):
        # Look at minimum (which is negative of our maximum) and negate it
        min_val = self.min_heap.peek()
        return -min_val if min_val is not None else None



# Run the tests
if __name__ == "__main__":
    
    # Usage example
    max_heap = MaxHeap()
    values = [5, 3, 7, 1, 4]
    print("Inserting:", values)

    for value in values:
        max_heap.insert(value)

    # Remove all values (should come out in descending order)
    while True:
        max_val = max_heap.remove_max()
        if max_val is None:
            break
        print(f"Removed max: {max_val}")