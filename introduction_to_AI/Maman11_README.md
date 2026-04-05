# Maman 11 – Tiles 8-Puzzle Solver

Student: *Omer Shraibshtein (205984271)*

Email:   *omershreib@gmail.com*

Last-Update: *05/04/2026*

***

## 1. General Overview

### 1.1 Program Architecture

This program implements a general framework for solving search problems using graph-search algorithms and heuristic functions,
as learned in the Open University Course of *Introduction to Artificial Intelligence* (semester 2026b). 
The `maman11/` package folder implements the required program that solves the **Tiles (8-puzzle) problem**.

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
- Cost-Optimal Solution – shortest path from an initial state to a goal state.  

---

### 1.4 Notations
This program uses these following notations:

- n – state
- n' – successor state of n (*i.e.*, n' is produced from n by a single action)    
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

Here is an example of a simple run (without any additional options):

```commandline
python -m introduction_to_AI.maman11.tiles 1 4 0 5 8 2 3 6 7
```

**Note:**

There are an optional command-line arguments that offers more features that surpass the requrements of this maman
and offer additinal features like solving attempnt of N-Tiles (instead of only focusing at this 8-Tiles version),
visualization option and more.

---

## 2. Tiles Problem Representation

### 2.1 State Representation

TilesGameState(State, TilesBoard)

This class combines:
- State abstraction
- TilesBoard functionality

The reason for this Tiles game state design is to separate search logic and board-tiles specific logic
In the price of a little more code, this heavily improves debugging, code reuse, and extensibility 
(*i.e.*, any new methods needed to be implemented and then applied to the tiles' board will not affect the `State` class that is being used
by other problems, for which these methods are irrelevant).

---

### 2.2 Initial State 

in a 2-dimentional list representation example:

```
[[6, 4, 8],
 [7, 5, 1],
 [2, 3, 0]]
```

---

### 2.3 Goal State

in a 2-dimentional list representation:

```
[[0, 1, 2],
 [3, 4, 5],
 [6, 7, 8]]
```
---

### 2.4 Actions

By a simple description, the term *Action* is defined as:

*"tile [x] move [direction]"*

where *direction* ∈ {LEFT, RIGHT, UP, DOWN} 

In vectorial representation:

- UP = [-1 0]
- DOWN = [+1 0]
- LEFT = [0 -1]
- RIGHT = [0 +1]

**Note:** 

In this *maman* the *action* is defined by the movement of the empty tile, which is very clean and clever way to do so.
Unfortunately, I noticed this too late, after all my program designed with a different less compact definition as depicted above  :disappointed:

Mathematically, my less compact action definition defined as the pair of (tile, direction).
This program implements this with an action object called `TileMovement`. 

In a simple description, any TileMovement object
contains 4 things:
1. the tile's value (*i.e.*, $1 \leq i \leq 9$)
2. the tile's current (x, y) position (*i.e.*, tile position before its action was applied on)
3. the tile's direction

Inside the tranision model, implemented by problem.update(state, action) -> newState, the action attribute expected to be a TileMovement.  

**Important:** 

the order of directions' check is as follows (from left to right):

LEFT, RIGHT, UP, DOWN.

For a pedagogical purpose, **This is matter!** because it can change the order of nodes' expansion, located at the same horizontal-level distance from the root node during graph-search. 

---

### 2.5 Transition Model

In this program, the transition model is implemented by the *Problem.update(state, action)* method, which returns
a *newState* object that is being received from *state* after appling this TileMovement *action* on *state*.

For each *state*, the image of Problem.update(*state*, ACTIONS) defines the transition Model 
(where in ACTIONS I mean all the legal actions that can be applied on *state*, producing a new successor state) 

Mathematically:

$$
T: STATES \times ACTIONS &rarr; STATES
$$

$$
T(state, action) = Problem.update(state, action) = newState 
$$

**Note:**

Problem.update(state, action) assumed to receive a legal action and **does not perform any legality check**. 
The legality check of an *action* being applied to a *state* is being handled by the expand() method **before** calling Problem.update(). 
In a graph search, the expand() method calls Problem.get_actions(), which handle filtering **only** legal actions, yielding its node's children. 

Problem.get_actions() check if a tile's *action* applied to a *state* is legal according 3 conditions:
1. the current tile (1-8) position (*i.e.*, before moving it) is valid. Namely, the current $(x,y)$ tile position is on the game board ⟺ $0 < x,y < 3$.
2. the target position of this tile (1-8) caused by this action is valid.

**Note:** 

The condition in which the target $(x', y')$ position must contains, before this action, the **empty tile** (in this program, the empty tile location is defined by `0`)
is always true, because all possible *state* actions derived from the current position of the empty tile.


### Transition Model - Use Case Example 

```
state = [[0, 7, 8],    
        [2, 1, 5],   
        [6, 4, 3]]

Problem.get_actions(state) returns (in order): [(7, RIGHT), (2, UP)]

then, the image of the transition model when applied on this state looks as follows: 

                         [[7, 0, 8],    
T(state, (7, RIGHT)) ⟶  [2, 1, 5],   
                         [6, 4, 3]]


                      [[2, 7, 8],    
T(state, (2, UP)) ⟶  [0, 1, 5],   
                      [6, 4, 3]]

```
---

### 2.6 Cost Function

Since all possible (legal) tiles movements have the same cost 
(*e.g.*, moving tile #2 UP and moving tile #7 LEFT have an equal cost)
then:

$TilesGameProblem().action_cost(curr_state, action, result_state) = c(n,a,n') = 1$

---

## 3. Algorithms

This *maman* required to compare 3 algorithmic solutions attemp to solve this Tiles game:
- BFS (Un-informed deterninistic algorithm)
- 2 additional informed search (A* based) heuristics 

### 3.1 BFS - quick overview

- implemented using a FIFO queue
- cost-optimal
- requires a high memory usage becuase it need to save all nodes in memory.

---


### 3.2 - A* Search Based Heuristic

For both of my heuristic examples, there are 2 things that required to check:

Admissible:
$h(n) ≤ h*(n)$

Consistent:
$h(n) ≤ c(n,a,n') + h(n')$

**Note:** 

1. if h(n) is *consistent*, then h(n) is also *admissible* (not vice-verca).
2. according to the course book (pages 105-106), if a heuristic h(n) is admissible then A* search that uses h(n) is guaranteed to be cost-optimal.

---

### 3.2.1 WrongRowCol (A*)

This is a unique heuristic example I manage to create myself - defined by: 

$h(n) := wrong rows + wrong columns$

#### Pseudo-Code of WrongRowCol Evaluation Function:

```python

def wrong_row_col(state n, state s) {
   # retuns the total WrongRowCol score of state n
   #
   # args:
   #  n - the current state
   #  s - the goal state
   int score ⟵ 0;

   for each tile between 1 and 9 {
      int curr_x, curr_y ⟵ n.arg_pos(tile);
      int goal_x, goal_y ⟵ s.arg_pos(tile);

      if (curr_x != goal_x) then score++;
      if (curr_y != goal_y) then score++;
   }

   return score;
}
```

*WrongRowCol* is inpired by *Manhattan Distance*, in the way that *Manhattan Distance* calculates the numbers of tiles movements
(in a relaxed case senario) towards its goal (x, y) position. This derives more simple idea: 
*if a tile need to move, then it is currently located in the wrong row/column.*

Therefore, I decided to check if a heuristic that, estimates the distance to its goal state by counting all
tiles that being located at a wrong row or column, can work. Fortunatly, this idea proved to work. Furthemore, in term of the number of expanded nodes, 
empirical running tests of this Tiles game show that *WrongRowCol* stands somewhere between *Misplaced* and *Manhattan Distance*.


### Example Use Case:

```
state = [[0, 7, 8],    
        [2, 1, 5],   
        [6, 4, 3]]

sum of WrongRowCol's score according to the correct row+column of every tile

for example, tile #2 is located in position (1,0) while its goal position is (0,2), so both row and columns are wrong ==> +2
by another example, tile #7 is located in the correct row (1) but in the wrong column (0 != 2) ==> +1

                       [[ , +2, +1],    
 WrongRowCol(state) =  [+2, +1, 0],   = 8
                       [0, +1, +1]]
```


---

## WrongRowCol - Proof of Consistency:

Let tile *x* be located at position ($r_i$, $c_k$) is state n, and suppose a single action causing *x* to move from row $r_i$ to row $r_j$, producing state n'.

Only one tile moves, so:
- moving in/out to/from its goal row/column change WrongRowCol scoure by $\pm 1$
- diagonal movements are forbidden, and therefore only the row/column position can be changed between neigboors states

---

### Cases Analysis

#### Case 1: Neither $r_i$ nor $r_j$ is the goal row

Following this case senario, the number of wrong rows and wrong columns remain the same - so:

$h(n) - h(n') = 0 \leq 1$

---

#### Case 2: $r_j$ is the goal row (tile moves INTO goal row)

Following this case senario, the number of wrong rows decreased by one (the number of wrong columns remain the same) - so:

$h(n) - h(n') = (+1) \leq 1$


#### Case 3: $r_i$ is the goal row (tile moves OUT of goal row)

Following this case senario, the number of wrong rows increased by one (the number of wrong columns remain the same) - so:

$h(n) - h(n') = (-1) \leq 1$


### Conclusion

In all cases:

$h(n) - h(n') \leq 1$

Therefore the heuristic is consistent.

Since consistency implies admissibility, the heuristic is also admissible.

Q.E.D.

**Note:** 

1. the case where *x* moves vertically (between columns, instead of rows) is symmetrical.
2. as explained earlier, because *WrongRowCol* proved to be admissible, this A* search is also cost-optimal.

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

lc(n, $r_i$) = the number of tiles that must be removed from row $r_i$ in order to solve the linear conflict.  
lc(n, $c_i$) = the number of tiles that must be removed from column $c_i$ in order to solve the linear conflict.  

LC(n) = estimated cost to solve all linear conflicts in this n-state. 

The lower bound of it is: 

$LC(n) = 2 \times \sum_{0 \leq i \leq 2} [lc(n, r_i) + lc(n, c_i)]$ 

the overall heuristic:

h(n) = MD(n) + LC(n)

The reason this **2** factor is because of *Corollary 5* in the `Hansson` paper claims that:

*"If there is a unique shortest path, p, between position X and position Y in the N 
Puzzle, then any alternate path will be at least 2 moves longer than p."*

---

## LinearConflict - Proof of Consistency: (based on the original proof written in the `Hansson` paper)

Let tile *x* be located at position ($r_i$, $c_k$) is state n, and suppose a single action causing *x* to move from row $r_i$ to row $r_j$, producing state n'.

Only one tile moves, so:
- Manhattan distance changes by ±1
- Only affected rows/columns may change LC

---

### Key Property

For any row r:

lc(n', r) ∈ { lc(n, r), lc(n, r) ± 1 }

Therefore:

LC(n') - LC(n) ∈ {0, ±2}

---

### Cases Analysis

#### Case 1: Neither $r_i$ nor $r_j$ is the goal row

MD changes by ±1, LC unchanged:

$h(n) - h(n') \leq 1$

---

#### Case 2: $r_j$ is the goal row (tile moves INTO goal row)

MD decreases by 1:

$MD(n) - MD(n') = +1$

LC may:
- stay the same → h(n) - h(n') = +1  
- increase by 2, resulting:

$$ 
\begin{aligned}
h(n) - h(n') &= MD(n) + LC(n) - [MD(n') + LC(n')] \\
&= [MD(n) - MD(n')] + 2 \times \sum_{0 \leq i \leq 2} \left( [lc(n, r_i) + lc(n, c_i)] - [lc(n', r_i) + lc(n', c_i)] \right) \\ 
&= (+1) + 2 \times [lc(n, r_j) - lc(n', r_j)] \\ 
&= (+1) + 2 \times [lc(n, r_j) - (lc(n, r_j) + 1)] \\
&= (+1) + 2 \times (-1) \\
&= 1 - 2 \\
&= (-1) \leq 1 \\
\end{aligned} 
$$

Both satisfy consistency.

---

#### Case 3: $r_i$ is the goal row (tile moves OUT of goal row)

MD increases by 1:

MD(n) - MD(n') = -1

LC may:
- stay the same → h(n) - h(n') = -1
- decrease by 2, resulting:

$$ 
\begin{aligned}
h(n) - h(n') &= MD(n) + LC(n) - [MD(n') + LC(n')] \\
&= [MD(n) - MD(n')] + 2 \times \sum_{0 \leq i \leq 2} \left( [lc(n, r_i) + lc(n, c_i)] - [lc(n', r_i) + lc(n', c_i)] \right) \\ 
&= (-1) + 2 \times [lc(n, r_j) - lc(n', r_j)] \\ 
&= (-1) + 2 \times [lc(n, r_j) - (lc(n, r_j) - 1)] \\
&= (-1) + 2 \times 1 \\
&= (-1) + 2 \\
&= (1) \leq 1 \\
\end{aligned} 
$$

Both satisfy consistency.

---

### Conclusion

In all cases:

$h(n) - h(n') \leq 1$

Therefore the heuristic is consistent.

Since consistency implies admissibility, the heuristic is also admissible.

Q.E.D.

**Note:** 

1. the case where *x* moves vertically (between columns, instead of rows) is symmetrical.
2. as explained earlier, because *LinearConflict* proved to be admissible, this A* search is also cost-optimal.

---

Admissible:
Each conflict adds ≥ 2 moves

---

## 4. Experimental Results

To be added.

---


## 5. Appendix

### 5.1 Command-Line Arguments (Optional)

Because this maman was really interesting and fun to investigate, I extended the scale of this maman's requirements 
and checked if I can solve the **general case** of this game (*i.e.* for $n \geq 3$). In addition, I include examples
of experimental algorithms that I tested during the creation of this *maman*.

**Note:** 

Only `BFS`, `WrongRowsColumns`, and `ManhattanDistance-Plus-LinearConflict` will be formally explained as part
of this maman's requirement (required to implement BFS and 2 additional *"more-informatics heuristics* compare to *ManhattanDistance* and *Misplaced* that depicted in the course book)

This program supports flexible execution via command-line arguments.

#### Optional Arguments

- --alg, -a: algorithm (bfs, manhattan, rowcol, ...)
- --graphic, -g: enable graphic displayer (visualize the solution of this game using matplotlib)
- --verbose, -v: enable verbose output (visualize the solution of this game through the terminal)

Note: running this program with `-a 'all'` will attempt to solve this game, following a legal tiles board
provided to it, with **every** algorithm this program supports, which includes:
- BFS: 'bfs'
- ManhattanDistance: 'manhattan'
- Misplaced: 'misplaced'
- LinearConflict: 'linear_conflict'
- WrongRowsColumns 'rowcol' 
- Max-RowColumns-And-ManhattanDistance 'max_rowcol_md'
- ManhattanDistance-Plus-LinearConflict 'md_plus_lc'

Example for optional argument usage:

```commandline
python -m introduction_to_AI.maman11.tiles 1 4 0 5 8 2 3 6 7 -a 'manhattan' -g -v
```

Example (4x4):

```commandline
python -m introduction_to_AI.maman11.tiles 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 0
```


