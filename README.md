# Pathfinding Algorithm Visualizer

An interactive pathfinding algorithm visualizer built with Python (Pygame). This tool allows you to observe step-by-step how different exploration and optimization algorithms traverse a grid, manage their internal data structures (Queue/Stack), and calculate the shortest path.

Live Web Version: https://pathfinding-algorithms-visualizer.netlify.app

---

## Features

* Interactive Dropdown Menu: Direct and instant selection of the algorithm to execute.
* Data Structure Inspector: Real-time visualization of the internal queue state (Open Set / Queue / Stack) along with f, g, h scores.
* Supported Algorithms:
  * A* Search (Heuristic + Path cost)
  * Dijkstra's Algorithm (Shortest path search without heuristic)
  * Greedy Best-First Search (Heuristic-based search)
  * Breadth-First Search (BFS) (Breadth-first exploration - FIFO)
  * Depth-First Search (DFS) (Depth-first exploration - LIFO)
* Interactive Grid Editor:
  * Draw and erase walls using the mouse.
  * Drag and drop Start and End points.
  * Dynamic grid resizing (Cols / Rows) from the control panel.
* Simulation Controls: Auto-play, pause, step-by-step navigation (forward/backward), and quick reset.

---

## Controls and Shortcuts

### Mouse
* Left Click + Drag: Draw walls / Drag Start or End node.
* Right Click + Drag: Erase walls.

### Keyboard
* Space: Start / Pause simulation.
* Left Arrow / Right Arrow: Step-by-step navigation (Backward / Forward).
* R: Reset the grid (Clear all walls).

---

## Installation and Setup

### Prerequisites
* Python 3.10+

### Steps

1. Clone the repository:
```bash
git clone https://github.com/MorenoLopez/pathfinding_algos_visualizer.git
cd pathfinder-algo-visualizer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python pathfinder_algo_visualizer.py
```

---

## Web Version

If you prefer to try the visualizer directly in your browser without installing Python, check out the Netlify deployment: https://pathfinding-algorithms-visualizer.netlify.app
