# Maman 13 – Reversi Minimax Agents

Student: *Omer Shraibshtein*  
Last-Update: *14/05/2026*

***

- **Note**:  Writing this maman in Hebrew is (always, because of editing with Hebrew and English chars) demand 
a significant labor fource that I do not have right now. So I hop it will be ok that this maman is in English.



## 1. General Overview

This assignment implements the game **Reversi / Othello** as an adversarial search problem.

The main purpose of this maman is to study game-playing agents, especially:

- Minimax decision making
- Alpha-Beta pruning
- Heuristic evaluation functions
- Competition between two rival agents
- Reversi as a deterministic, turn-based, zero-sum game

The implementation follows the same architectural idea used in **Maman 11 – Tiles Problem**:  
the general search / agent logic is separated from the problem-specific game logic.

---

## 2. Program Architecture

### 2.1 Global Reusable Components

These components are shared across assignments:

- `models/` – abstract definitions of `State`, `Problem`, `Move`, `Evaluator`, and `Agent`
- `agents/` – general agents such as `MinMaxAgent`
- `minmax_tree_utils.py` – Minimax / Alpha-Beta decision logic
- `common.py` – shared utilities

### 2.2 Problem-Specific Package: `maman13/`

The `maman13/` package contains all Reversi-specific logic:

- `reversi.py` – main entry point
- `reversi_game_state.py` – Reversi state representation
- `reversi_game_problem.py` – adversarial problem definition
- `reversi_move.py` – move representation
- `reversi_evaluators.py` – heuristic evaluation functions
- `reversi_agents.py` – Reversi-specific agents
- `reversi_agents_factory.py` – factory for creating agents
- `reversi_runner.py` – game loop manager
- `bitboard.py` – efficient bitboard operations
- `bitboard_calculator.py` – conversion utilities between board cells and bits
- `reversi_graphic_displayer.py` – optional graphical display

---

## 3. Reversi Problem Representation

### 3.1 State Representation

A game state is represented by `ReversiGameState`.

Each state contains:

- Red player bitboard
- White player bitboard
- Current player turn
- Board size
- Number of consecutive passes
- The move that created the state

The board is represented internally using **bitboards**, which allow compact and efficient board calculations.

---

### 3.2 Initial State

The classic Reversi board is an `8 x 8` board.

The game starts with four disks in the center:

```text
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . W R . . .
. . . R W . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
```

Red begins the game.

---

### 3.3 Actions

An action is represented by `ReversiMove`.

A legal action is a board cell:

```text
(row, column)
```

A move is legal if placing a disk in that cell captures at least one opponent disk according to the rules of Reversi.

If a player has no legal moves, the only available action is:

```text
PASS
```

---

### 3.4 Transition Model

The transition model is implemented by:

```python
ReversiGameProblem.update(state, move) -> ReversiGameState
```

Mathematically:

$$
T: STATES \times ACTIONS \rightarrow STATES
$$

$$
T(state, action) = newState
$$

The transition model:

1. Applies the selected move
2. Flips all captured opponent disks
3. Switches the turn to the opponent
4. Updates the number of consecutive passes
5. Returns a new immutable-like game state


### Players Agents Actions

The RED and WHITE players are controlled by a `ReversiAgent` class object.
During the game, the agent of every player must choose its move.
This is implemented by `ReversiAgent.choose_move(state: GameState) -> Move`.
Let break this. This player's agent receives this current `GameState` and choose its move
according to some heuristic evaluation function.


### Python Bitwise Operators (Quick Reference)

This table summarizes the **bitwise operators in Python**, their symbols, meanings, and simple examples.
Bitwise operators work on integers **bit by bit**.

| Operator | Name       | Description                                         | Example  | Result |
|---------:|------------|-----------------------------------------------------|----------|--------|
| `&`      | AND        | Bit is 1 if **both** bits are 1                     | `5 & 3`  | `1`    |
| `|`      | OR         | Bit is 1 if **either** bit is 1                     | `5 | 3`  | `7`    |
| `^`      | XOR        | Bit is 1 if bits are **different**                  | `5 ^ 3`  | `6`    |
| `~`      | NOT        | Flips all bits (two’s complement)                   | `~5`     | `-6`   |
| `<<`     | Left shift | Shifts bits left (×2 per shift)                     | `5 << 1` | `10`   |
| `>>`     | Right shift| Shifts bits right (÷2 per shift, floor)             | `5 >> 1` | `2`    |


### Legal Moves Analysis 

Calculating player's legal moves is possible using `legal_moves_mask()`

```python
def legal_moves_mask(player: PlayerBitBoard, opponent: PlayerBitBoard) -> int:
    full = player.full
    player_bitmask = player.bitboard & full
    opponent_bitmask = opponent.bitboard & full
    free_bitmask = (~(player_bitmask | opponent_bitmask)) & full

    moves_mask = 0
    for shift_f in player.all_possible_shifts():
        possible_move = shift_f(player_bitmask) & opponent_bitmask

        while possible_move:
            moves_mask |= shift_f(possible_move) & free_bitmask
            possible_move = shift_f(possible_move) & opponent_bitmask

    return moves_mask & full
```

where:
- `player.bitboard`   → bits where the current player has discs
- `opponent.bitboard` → bits where the opponent has discs

The constant mask:

- `full` → 1s in all valid board positions (e.g., for 8×8: 64 ones)

Masking with `& full` ensures we ignore any bits outside the board.

---

As a reminder, a move is considered legal in Reversi if the played disc would flip **at least one opponent disc**.

That happens when in **at least one direction**:

1. the move cell is **empty**.
2. the cell next to the move contains an opponent disc, and  
3. continuing in the same direction you eventually reach a player disc.  
4. between this player's move and the end-player-disc exist **only** opponent discs - at least one.

Visually (in one direction):

```
(player)  (opponent) (opponent)  (empty)
   P          O         O          .
```

---


### Step A — Compute the “free cells” mask

```python
free_bitmask = (~(player_bitmask | opponent_bitmask)) & full
```

where:
- `player_bitmask | opponent_bitmask` → all occupied cells
- `~(...) & full` → all empty cells within the game board

So `free_bitmask` has a 1 exactly where a move could potentially be placed.

---

### Step B — Scan all 8 directions

```python
for shift_f in player.all_possible_shifts():
```

`all_possible_shifts()` returns 8 shift functions:

- up, down, left, right
- up-left, up-right, down-left, down-right

Each `shift_f(x)` moves the entire bitboard `x` by **one cell** in that direction, while preventing wrap-around at edges.

---

For a fixed direction `shift_f` the code does:

```python
possible_move = shift_f(player_bitmask) & opponent_bitmask
```

where:

- `shift_f(player_bitmask)` marks the cell **one step away** from every player disc in this direction.
- `& opponent_bitmask` keeps only those cells that contain an opponent disc.

So `possible_move` is:

> “all opponent discs that are **adjacent** (in this direction) to at least one player disc”.

This matches the Reversi rule: to flip, the move must connect to a chain of opponent discs that is anchored by a player disc on one end.
Iteratively, we continue to call `shift_f()` to check if we can flip opponent disc in this direction.

---

### 3.5 Terminal States

A state is terminal if one of the following conditions holds:

1. The board is full
2. Both players pass consecutively

When the game reaches a terminal state, the winner is the player with more disks.

---

## 4. Utility and Evaluation

### 4.1 Utility Function

The utility of a state for a player is:

$$
utility(state, player) = score(player) - score(opponent)
$$

Meaning:

```text
number of player's disks - number of opponent's disks
```

A positive value means the player is currently winning.  
A negative value means the opponent is currently winning.

---

### 4.2 Score Heuristic

The implemented heuristic is `ReversiScoreEvaluator`.

```python
evaluate(state, player) = state.score(player) - state.score(player.opponent())
```

This heuristic prefers states where the current player owns more disks than the opponent.

This is a simple and deterministic heuristic.

---

## 5. Agents

### 5.1 Hungry Score Agent

The `hungry_score` agent is a greedy agent.

It checks the legal moves available in the current state and chooses a move according to the immediate score obtained after applying that move.

This agent does not look ahead deeply into the game tree.

---

### 5.2 Heuristic Score Minimax Agent

The `heuristic_score` agent uses:

- Minimax search
- Alpha-Beta pruning
- `ReversiScoreEvaluator`
- Configurable search depth

The agent tries to choose the move that maximizes its expected utility while assuming the opponent also plays rationally.

---

## 6. Minimax and Alpha-Beta Search

### 6.1 Minimax Idea

Reversi is modeled as a two-player adversarial game:

- RED is the maximizing player
- WHITE is the minimizing player

The maximizing player tries to maximize the evaluation score.  
The minimizing player tries to minimize it.

The Minimax decision rule is:

$$
a^* = argmax_a \ MinValue(Result(s, a))
$$

---

### 6.2 Alpha-Beta Pruning

Alpha-Beta pruning improves Minimax by avoiding branches that cannot affect the final decision.

It keeps two bounds:

- `alpha` – the best value found so far for MAX
- `beta` – the best value found so far for MIN

If a branch is already worse than a previously found alternative, it is pruned.

This does not change the final Minimax result, but it can significantly reduce the number of expanded nodes.

---

## 7. How to Run the Program

From the project root, run:

```commandline
python -m introduction_to_AI.maman13.reversi -red heuristic_score -white hungry_score --ahead 4 -v
```

### Arguments

- `--red_agent`, `-red` – select the RED player agent
- `--white_agent`, `-white` – select the WHITE player agent
- `--ahead`, `-a` – Minimax search depth
- `--verbose`, `-v` – print the game step-by-step
- `--graphic`, `-g` – show graphical display
- `--methodical`, `-m` – display only the first chosen number of states before jumping to the final state

Supported agents:

```text
heuristic_score
hungry_score
```

---

## 8. Example Run

```commandline
python -m introduction_to_AI.maman13.reversi \
  -red heuristic_score \
  -white hungry_score \
  --ahead 4 \
  -v \
  -g
```

This command runs a Reversi game where:

- RED uses Minimax with score heuristic
- WHITE uses the greedy hungry-score agent
- The Minimax depth is 4
- The game is printed step-by-step
- The graphical display is enabled

---

## 9. Answer Question

### Question 2.a:

when repeating this game run under this configuration, does this game ends with the same result?

#### Answer:

yes. since the evaluation function that I defined, which calculates the score difference between
                the current player and the opponent player, is purely deterministic and does not include randomness.
                As a result, this evaluation function will resolve the same evaluation score to each and every state
                of this game, which then causes the same players moves in every new run.


### Question 2.b:

assuming we have 2 heuristic evaluation functions - how can we check which one of them is more successful?

---

#### Answer
In general, a heuristic evaluation function will be considered "better" than another if the agent using it beats another agent using the other heuristic function. In practice, this definition is too simplistic. This is because its preference over its opponent depends on many factors such as:
- The depth of the minimax tree
- Whether the player is the maximum or minimum
- Whether the evaluation function is deterministic or stochastic (in the latter case, the number of victories must be statistically checked)

Each of these factors has an impact on the victory or loss of a 1-on-2 heuristic.

Also, different heuristic evaluation functions are better or worse at different stages of the game (beginning, middle, or end), and knowing this, it is possible to have a game strategy in which one starts with one heuristic function, and after a number of states, replaces it with another.

A less simplistic answer is that we would prefer a heuristic whose ability to win depends as little as possible on being the maximum or minimum player, and is also cheap in resources (i.e., does not require a very deep minimax tree to win).

---

### Question b.3: 

assuming that some heuristic evaluation function h() is "good" only in a specific part of the game,
how and when should we replace it? what are the condition to make this replacement?

#### Answer:

In general, I admit that this is a very complex question that I am not sure I have a complete answer for.

I would try to answer this problem as follows:
1. Given a large number of heuristics, I would run them against each other
2. This Darwinian experiment is based on the hypothesis that there are central nodes (i.e., the configuration of the game) through which winning heuristics pass the most. These nodes can be located at the beginning, in the middle, or towards the end of the game
3. The classification of the heuristic function by stages (beginning, middle, end) will be according to the likelihood that they will pass through those "winning" nodes

It is possible at the same time to identify "losing" nodes, and consider replacing a heuristic if it is identified that the current heuristic is approaching (for example, using the Hamming distance) these states.

---

### Question c.1:


What is the complexity of running a full game with a heuristic evaluation function that is constantly running at depth 2 relative to a situation where the current player is required to choose an action?

For this purpose, assume: 10 = b-branching factor – the order of magnitude of the number of possible actions in each situation.


#### Answer

total tree nodes (moves):
        ~ 1 + 10 + 100 = 111 = O(100)
    
since Reversi game usually lasted for M = 60 moves (approximately, and diffidently cannot be bigger than 64, or n^2 for 
the general case), then complexity is equal to O(60 * 100) = O(6000)
                    for the general case: O((n^2) * 100)

---

#### Question c.2:

In contrast, what is the complexity if you were to perform a calculation for the entire depth of the tree to select an action?

#### Answer

If the agent searches the entire game tree until the end of the game, the complexity is:

O(b^m)

where:
- b=10
- m = number of moves remaining until the end of the game

So:

O(10^m)

For Reversi, after the initial 4 discs, there are at most about 60 moves remaining, 
so the worst-case order is approximately:

O(10^60)

---

#### Question c.3:

In what order should the player check the actions (branches in the search tree) so that pruning is maximized?

#### Answer


To maximize pruning, the player should check the best moves first.

Meaning:

At MAX nodes: check moves from the highest estimated value to the lowest.
At MIN nodes: check moves from the lowest estimated value to the highest.

In Reversi, good ordering can be based on heuristic priorities such as:

*corners* -> *edges* -> *highMobility* -> *highScore* -> etc

With perfect ordering, Alpha-Beta can reduce the effective complexity from:

O(b^d)

to approximately:

O(b^(d/2))

For depth 2:

O(10^1)=O(10)

instead of:

O(10^2) = O(100)

which is quite significant!