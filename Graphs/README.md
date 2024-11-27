# Graph Algorithms Study Guide

## Core Concepts

### Graph Basics

- A graph is a collection of nodes/vertices and edges
- Nodes represent entities, edges represent connections between nodes
- Two main types:
  - Directed graphs: Edges have direction (one-way connections)
  - Undirected graphs: Edges are bidirectional (two-way connections)
- Cycles: Paths that lead back to the starting node
- Components: Isolated groups of connected nodes

![Alt text](images/graph.png)

### Graph Representations

1. Adjacency List (Most common)

```javascript
{
  'a': ['b', 'c'],
  'b': ['a', 'd'],
  'c': ['a', 'e'],
  'd': ['b'],
  'e': ['c']
}
```

2. Edge List

```javascript
[
  ["a", "b"],
  ["b", "c"],
  ["c", "d"],
];
```

### Traversal Algorithms

#### Depth First Traversal (DFS)

- Uses a stack (LIFO)
- Explores one direction as far as possible before backtracking
- Can be implemented:
  1. Iteratively using an explicit stack
  2. Recursively using the call stack
- Time: O(e) where e is number of edges
- Space: O(n) where n is number of nodes

#### Breadth First Traversal (BFS)

- Uses a queue (FIFO)
- Explores all neighbors at current depth before going deeper
- Must be implemented iteratively
- Best for finding shortest paths
- Time: O(e)
- Space: O(n)

## Key Problems & Patterns

### 1. Has Path

**Problem**: Determine if there exists a path between two nodes in a directed graph

- Use either DFS or BFS
- Return true if destination found
- Return false if traversal completes without finding destination
- Time: O(e), Space: O(n)

### 2. Undirected Path

**Problem**: Determine if path exists between nodes in an undirected graph

- Convert edge list to adjacency list if needed
- Must track visited nodes to prevent cycles
- Use Set for O(1) lookups of visited nodes
- Time: O(e), Space: O(n)

### 3. Connected Components Count

**Problem**: Count number of separate connected components in graph

- Iterate through all nodes
- For unvisited nodes, do full traversal and increment count
- Mark nodes as visited during traversal
- Time: O(e), Space: O(n)

### 4. Largest Component

**Problem**: Find size of largest connected component

- Similar to component count but track size during traversal
- Keep running max of component sizes
- Time: O(e), Space: O(n)

### 5. Shortest Path

**Problem**: Find shortest path between two nodes

- Use BFS (crucial - DFS won't guarantee shortest path)
- Track distance with each node in queue
- Can use tuple/pair of (node, distance) in queue
- Time: O(e), Space: O(n)

### 6. Island Count (Grid Problems)

**Problem**: Count number of islands in 2D grid

- Treat grid as graph where:
  - Nodes are positions (r,c)
  - Neighbors are up/down/left/right
- Use DFS or BFS to explore islands
- Mark visited positions
- Time: O(rc), Space: O(rc) where r = rows, c = columns

### 7. Minimum Island

**Problem**: Find size of smallest island in grid

- Similar to island count but track sizes
- Keep running minimum of island sizes
- Ignore water/visited positions
- Time: O(rc), Space: O(rc)

## Interview Tips

1. Graph Recognition

- Many problems can be modeled as graphs:
  - Social networks (friends connections)
  - Course prerequisites
  - City/road networks
  - File system directories
  - State machines

2. Problem Solving Steps

   - Draw the graph! Visualize nodes and edges
   - Choose traversal method (usually DFS for simpler cases, BFS for shortest paths)
   - Consider if you need to track visited nodes (usually yes for undirected graphs)
   - Think about what data you need to track during traversal (counts, sizes, paths)

3. Code Organization

   - Separate graph building from traversal logic
   - Use helper functions for traversal
   - Consider both iterative and recursive solutions for DFS

4. Common Patterns

   - Converting between edge lists and adjacency lists
   - Using visited set to prevent cycles
   - Combining iterative and recursive code for component problems
   - Grid problems as graphs with position-based neighbors

5. Edge Cases
   - Empty graphs
   - Single node graphs
   - Disconnected components
   - Cycles in undirected graphs
   - Grid boundaries in matrix problems

## Common Complexity

- Most graph algorithms: O(e) time, O(n) space
- Grid problems: O(rc) time and space
- Building adjacency list: O(e) time
- Lookups in visited set: O(1) time

Remember: When dealing with undirected graphs, always consider cycle prevention using a visited set!
