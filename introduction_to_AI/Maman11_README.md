## Maman 11 - Heuristic Solutions For The Tiles Game Problem

**Student:** *Omer Shraibshtein (205984271)*

**Date:** *24/03/2026*

***

### Program Layout

<pre>
     src/
        ├──__init__.py
        ├──agents.py
        ├──common.py
        ├──search_strategies.py
        └──maman11/
            ├──tiles.py
            ├──tiles_board.py
            ├──tiles_evaluators.py
            ├──tiles_game_problem.py
            ├──tiles_game_state.py
            ├──tiles_graphic_displayer.py
            ├──tiles_main_utils.py
            └──tile_movement.py
        └──models/
            ├──__init__.py
            ├──evaluator.py
            ├──node.py
            ├──problem.py
            └──state.py
</pre>

# Program Components

On the root */src* folder there are 3 modules:
    - `agents.py ` contains abstraction agents classes models for both *deterministic* agents (like the `BFSAgent`) and *heuristic* 
agents (like the `AStarAgent`)
    - `common.py` contains common functions like the `expand`, `make_node` and many more.
    - `search_strategies.py` currently contains `best_first_search` and `astar_search`, but hopefully, during this course, 
this module will increase with a lot more search-strategies that I will learn.


The *models* package contains abstraction class models for `problem`, `state`, `node`, and `evaluator.

The *maman11* folder contains the specific tiles program, while using the *model* package to define:
    1. what is the *tiles-game-problem*
    2. what is a *tiles-game-state*


# Tiles Game Problem - Introduction:

In order to explain the `TilesGameProblem`, I must explain first the implementation of `TilesGameState`.
I could simply provide a np.numpy 2d array in the shape of (3,3) (defined with `dtype=unit8` for memory efficient),
but I wrapped it with an extra layers of code for 2 reasons:
    1. In order to keep abstractions.
    2. To provide this `State` class object more functionality that I think will complicate explaining the solution of 
the tiles problem if they would be implemented outside this class.



# Tiles Game Problem - Definitions:

The `TilesGameProblem` components are defined as follows:
    - **State Space:** 

a np.numpy 2d array in the shape of (3,3) (defined with `dtype=unit8` for memory efficient)
    - **Init Space:*     




