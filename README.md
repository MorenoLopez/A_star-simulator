# A* Pathfinding Visualizer

An interactive, real-time visualizer for the A* (A-Star) pathfinding algorithm built with Python and Pygame.

This tool dynamically adapts to screen resolutions, provides full GUI control over grid dimensions and node coordinates, supports direct drag-and-drop interaction, and displays the internal state of the priority queue (Open Set) step-by-step.

---

## Understanding the A* Algorithm

A* is a graph traversal and path search algorithm that finds the shortest path between a starting node and a target node. It combines the guaranteed optimality of Dijkstra's algorithm with the efficiency of a heuristic-driven search.

### The Core Formula

At each step, A* selects the node $n$ from the priority queue that minimizes the total estimated cost function $f(n)$:

$$f(n) = g(n) + h(n)$$

* **$g(n)$**: The exact cost of the path from the starting node to node $n$.
* **$h(n)$**: The heuristic function estimating the remaining cost from node $n$ to the target node.
* **$f(n)$**: The total estimated cost of a path passing through node $n$.

### Heuristic Function: Manhattan Distance

For a grid allowing movement in four cardinal directions (up, down, left, right), A* uses Manhattan distance as its heuristic:

$$h(n) = |x_n - x_{\text{target}}| + |y_n - y_{\text{target}}|$$

This heuristic is **admissible** (it never overestimates the actual cost to reach the target), which guarantees that A* will always find an optimal shortest path if one exists.

### Node Sets

* **Open Set (Priority Queue)**: Discovered nodes waiting to be evaluated, sorted by ascending $f(n)$ values.
* **Closed Set**: Nodes that have already been evaluated and processed.

---

## A* vs. Dijkstra: Key Distinctions

* **Dijkstra's Algorithm** is equivalent to A* without a heuristic ($h(n) = 0$). It expands outward in uniform, concentric circles regardless of target direction.
* **A* Search** uses $h(n)$ to direct exploration toward the target.

### Behavior on Empty Grids

On an obstacle-free grid, every node along a direct path toward the target yields an identical $f(n)$ score. Because candidate nodes share the same priority ($f = \text{constant}$), A* resolves ties based on insertion order into the priority queue. This produces a diagonal sweeping pattern that may superficially resemble Dijkstra's algorithm, even though evaluation remains strictly directional.

---

## Features

* **Adaptive Fullscreen**: Automatically scales cell size and centers the grid based on screen resolution.
* **GUI Control Panel**:
  * Adjust grid dimensions (columns and rows) in real time.
  * Modify Start and End coordinates using GUI buttons or drag-and-drop.
* **Interactive Canvas**:
  * Left-Click: Draw walls / Drag Start (Green) and End (Red) nodes.
  * Right-Click: Erase walls.
* **Playback Controls**:
  * Pause / Play automatic step iteration.
  * Step forward and backward manually (`<` / `>`).
  * Reset grid walls and state history.
* **Real-time Queue Inspection**: Displays current node, reconstructed path, Closed Set, and sorted Open Set entries.

---

## Installation & Setup

### Prerequisites

* Python 3.8+
* Pygame

### Quick Start

```bash
# Clone the repository
git clone https://github.com/user/a-star-sim.git
cd a-star-sim

# Install dependencies
pip install -r requirements.txt

# Run the visualizer
python a_star_sim.py
```

---

## Controls Reference

* **Left Click**: Draw wall / Drag Start or End nodes.
* **Right Click**: Erase wall.
* **Escape Key**: Exit application.
