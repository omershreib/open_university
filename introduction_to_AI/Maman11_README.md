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

#### Global Modules
Reusable, problem-independent components:
- models/ – abstract definitions of State, Problem, Node, Evaluator, Agent (AtomicAgent)
- agents/ – BFS,  A*, and supporting agents
- common.py, search_strategies.py – shared utilities and strategies

#### Problem-Specific Package (maman11/)
Contains all logic specific to the Tiles problem:
- tiles_game_state.py
- tiles_game_problem.py
- tiles_evaluators.py
- tiles.py (main entry point)

---

#### 2. Problem-Specific Package (`maman11/`)
Contains all code specifically designed to deal with the Tiles problem:

- State representation (`tiles_game_state.py`)
- Problem definition (`tiles_game_problem.py`)
- Heuristics (`tiles_evaluators.py`)
- Main execution (`tiles.py`)
- (optional) Visualization (`tiles_graphic_displayer.py`)

---

### 1.2 Design Principles
This program is designed according to two main principles:

1. Code Reusability – shared modules reused across future assignments (mamans)  
2. Abstraction – separation between search logic and problem logic  


### 1.3 Terminology

- State – abstract State representation used by search algorithms  
- Board – concrete tile configuration  
- Action – tile movement  
- Expanded Node – a node whose children were generated  
- Heuristic Function h(n) – estimate to goal  
- Optimal Solution – shortest path from initial state to a goal state  

---

### 1.4 Notations
This program uses these following notations:

- n – state  
- g(n) – cost from start  
- h(n) – heuristic  
- h*(n) – true cost 
- f(n) = g(n) + h(n)

---

### 1.5 How to Run the Program

In terminal:

```
python -m introduction_to_AI.maman11.tiles <tiles...> [options]
```

#### Required Arguments

- tiles – A sequence of n^2 integers representing the board (row-wise)

here is an example of a simple running (without any additional options):

```commandline
python -m introduction_to_AI.maman11.tiles 1 4 0 5 8 2 3 6 7
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

```commandline
python -m introduction_to_AI.maman11.tiles 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 0
```

---

## 2. Tiles Problem Representation

### 2.1 State Representation

TilesGameState(State, TilesBoard)

This class combines:
- State abstraction
- TilesBoard functionality

The reason for this Tiles game state design is to separate search logic and board-tiles specific logic
In the price of a little more code, this heavily improves debugging, code reuse, and extensibility 
(i.e. any new methods I want to apply on the tiles-board will not affect the `State` class that will used
by other problems that these methods are irrelevant for them).

---

### 2.2 Initial State 

*Board* representation example:

[[6, 4, 8],
 [7, 5, 1],
 [2, 3, 0]]

---

### 2.3 Goal State

In *Board* representation:

[[0, 1, 2],
 [3, 4, 5],
 [6, 7, 8]]

---

### 2.4 Actions

UP, DOWN, LEFT, RIGHT

In vectorial representation:

- UP = [-1 0]
- DOWN = [+1 0]
- LEFT = [0 -1]
- RIGHT = [0 +1]

---

### 2.5 Transition Model

T(s, a) = s'

---

### 2.6 Cost Function

Since all possible (legal) tiles movements have the same cost 
(e.g. moving tile #2 UP and moving tile #7 LEFT have an equal cost)
then:

TilesGameProblem().action_cost(curr_state, action, result_state) = c(s,a,s') = 1

---

## 3. Algorithms

### 3.1 BFS

- FIFO queue
- optimal

---

### 3.2 RowCol (A*)

h(n) = wrong rows + wrong columns

Admissible:
h(n) ≤ h*(n)

Consistent:
|h(n) - h(n')| ≤ 1

---

### 3.3 Manhattan + Linear Conflict (A*)

*" Starts with Manhattan distance, then for each row and column, the number of tiles
    \"in conflict\" are identified, and 2 * this number is added to the total distance.
    (It will take at least 2 additional moves to reshuffle the conflicting tiles into
    their correct positions.) This is an admissible improvement over
    Manhattan-Distance (`Hansson, Mayer, Young, 1985`)."*

Source:
Hansson, Mayer, Young, 1985: https://academiccommons.columbia.edu/doi/10.7916/D8154QZT/download


This citation was found in this *slidingtilepuzzle* python library: https://slidingtilepuzzle.readthedocs.io/en/latest/_modules/slidingpuzzle/heuristics.html#linear_conflict_distance


MD(n) = sum of Manhattan distances  

LC(n) = number of conflicts  

h(n) = MD(n) + 2·LC(n)

Admissible:
Each conflict adds ≥ 2 moves

---

## 4. Experimental Results

To be added.

---

