from typing import Dict, List

graph: Dict[str, List[str]] = {
    "a": [ "c","b"],
    "b": ["d"],
    "c": ["e"],
    "d": ['f'],
    "e": [],
    "f": []
}

def DepthFirstPrint(graph: Dict[str, List[str]], start: str) -> None:
  """
  printing the graph in depth first order

  Args:
      graph (Dict[str, List[str]]): _description_
      start (str): _description_
  """
  stack: List[str] = [start]
    
  while len(stack) > 0:
    current: str = stack.pop()
    print(current)
    for neighbor in graph[current]:
      stack.append(neighbor)
      
      
def DepthFirstPrintRecursion(graph: Dict[str, List[str]], start: str) -> None:
  """
  printing the graph in depth first order using recursion

  Args:
      graph (Dict[str, List[str]]): _description_
      start (str): _description_
  """
  print(start)
  for neighbor in graph[start]:
    DepthFirstPrintRecursion(graph, neighbor)
        

print("Stack")
DepthFirstPrint(graph, 'a')

print("Recursion")
DepthFirstPrintRecursion(graph, 'a')