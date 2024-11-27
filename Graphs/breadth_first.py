from typing import Dict, List

graph: Dict[str, List[str]] = {
    "a": [ "c","b"],
    "b": ["d"],
    "c": ["e"],
    "d": ['f'],
    "e": [],
    "f": []
}

def BreadthFirstPrint(graph: Dict[str, List[str]], start: str) -> None:
  """
  printing the graph in breadth first order

  Args:
      graph (Dict[str, List[str]]): _description_
      start (str): _description_
  """
  queue: List[str]  = [start]
  
  while len(queue) > 0:
    current: str = queue.pop(0)
    print(current)
    for neighbor in graph[current]:
      queue.append(neighbor)
      

BreadthFirstPrint(graph, 'a')