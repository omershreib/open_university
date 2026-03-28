# Maman 11 – Tiles 8-Puzzle Solver

Student: *Omer Shraibshtein (205984271)*

Email:   *omershreib@gmail.com*

Last-Update: *28/03/2026*

***

## 1. General Overview

### 1.1 Program Architecture

This program implements a general framework for solving search problems using graph-search algorithms and heuristic functions,
as learned in the Open University Course of *Introduction to Artificial Intelligent* (semester 2026b). 
The `maman11/` package folder implements the required program solves the **Tiles (8-puzzle) problem**.

This program is divided into two main parts:

#### 1. Global Modules and Packages
These components are problem-independent and designed for reuse across multiple assignments 
(namely, `maman13/` and `maman15/` that will come in the future):

- `models/` – abstract representations of core concepts:
  - `State`
  - `Problem`
  - `Node`
  - `Evaluator`
  - `Atomic_Agent`

- `agents/` – implementations of agent-based search algorithms:
  - `DeterministicAgent`
  - `BFSAgent`
  - `HeuristicAgent`
  - `AStarAgent`

- `common.py`, `search_strategies.py` – shared utilities and strategies

#### 2. Problem-Specific Package (`maman11/`)
Contains all code specifically designed to deal with the Tiles problem:

- State representation (`tiles_game_state.py`)
- Problem definition (`tiles_game_problem.py`)
- Heuristics (`tiles_evaluators.py`)
- Main execution (`tiles.py`)
- (optional) Visualization (`tiles_graphic_displayer.py`)

---

### 1.2 Design Principles

The program is designed according to two main principles:

1. **Code Reusability**
   - Global modules allow reuse of search algorithms and data structures in future assignments.

2. **Abstraction**
   - Separation between *problem definition* and *search strategy*.
   - Any new problem can be implemented using the same basic class objects (`State`, `Problem`, `Evaluator`).

---

### 1.3 Terminology

- **State** – a configuration of the tiles on the board
- **Board** – a numpy 2d-array implementation of this Tiles game in the shape of (3,3)
- **Action** – a legal tile movement, prioritize in this order (from left to right): left, right, up, down  
- **Node** – a state container that can be used in a search tree 
- **Expanded Node** – the operation in which a parent node reveals its children nodes during graph-search
- **Heuristic Function** \( h(n) \) – estimate of distance to a goal state
- **Optimal Solution** – shortest path from initial state to a goal state  

---

### 1.4 Notation

We use the following notation:

- \( n \) – a state  
- \( h(n) \) – heuristic value  
- \( h^*(n) \) – true cost to goal  
- \( g(n) \) – cost from start state to \( n \)  
- \( f(n) = g(n) + h(n) \) – A* evaluation function  

---

### 1.5 How to Run the Program

In terminal from this program's root directory:

```
python -m introduction_to_AI.maman11.tiles <tiles...> [options]
```

#### Required Arguments

- tiles – A sequence of n^2 integers representing the board (row-wise)

here is an example of a simple running (without any additional options):

```commandline
python -m introduction_to_AI.maman11.tiles 6 4 8 7 5 1 2 3 0
```

### 1.6 Command-Line Arguments (Optional)

This program supports flexible execution via command-line arguments.

#### Optional Arguments

- --alg, -a : algorithm (bfs, manhattan, rowcol, ...)
- --graphic, -g : enable graphic displayer (visualize the solution of this game using matplotlib)
- --verbose, -v : enable verbose output (visualize the solution of this game to terminal)

Note: running this program with `-a 'all'` will attempt solving this game, following a legal tiles board
provided to it, with **every** algorithm this program support, which includes:
- BFS: ('bfs')
- ManhattanDistance ('manhattan')
- Misplaced ('misplaced')
- LinearConflict ('linear_conflict')
- RowColumns ('rowcol') 
- Max-RowColumns-And-ManhattanDistance ('max_rowcol_md')
- ManhattanDistance-Plus-LinearConflict ('md_plus_lc')

Example for optional argument usage:

```commandline
python -m introduction_to_AI.maman11.tiles 1 4 0 5 8 2 3 6 7 -a 'manhattan' -g -v
```

#### Support for General n x n

Example (4x4):

python -m introduction_to_AI.maman11.tiles 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 0

---

## 2. Tiles Problem Representation

### 2.1 State Representation

TilesGameState(State, TilesBoard)

This class combines:
- State abstraction (get_key, get_value)
- TilesBoard functionality (numpy board, board-tiles operations)

The reason for this Tiles game state design is to separate search logic and board-tiles specific logic
This heavily improves debugging, reuse, and extensibility (in the price of a little more code)

---

### 2.2 Initial State (Board representation)

Example:

[[6, 4, 8],
 [7, 5, 1],
 [2, 3, 0]]

---

### 2.3 Goal State (Board representation)

[[0, 1, 2],
 [3, 4, 5],
 [6, 7, 8]]

---

### 2.4 Actions

UP, DOWN, LEFT, RIGHT

In vectorial representation (implemented using numpy)

UP = [-1 0]
DOWN = [+1 0]
LEFT = [0 -1]
RIGHT = [0, +1]

---

### 2.5 Transition Model

T(s, a) = s'

---

### 2.6 Cost Function

Since all possible (legal) tiles movements have the same cost 
(e.g. moving tile #2 UP and moving tile #7 LEFT have an equal cost)
than

TilesGameProblem().action_cost(curr_state, action, result_state) = c(s,a,s') = 1

---

## 3. Algorithms

### 3.1 BFS

- FIFO queue
- optimal

---

### 3.2 RowCol (A*)

h(n) = wrong rows + wrong columns

Admissible and consistent.

---

### 3.3 Manhattan + Linear Conflict (A*)

h(n) = MD(n) + 2 * LC(n)

---

## 4. Experimental Results

To be added.

---

