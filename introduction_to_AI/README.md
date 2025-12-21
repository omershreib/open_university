# Heuristic Reversi Game Simulation - (Maman 13)

Student: Omer Shraibshtein (205984271)


## Game State Compact Representation:

My game state compact implementation is a follows:

GameState = (`PBB(RED)`, `PBB(WHITE)`, `player_turn`, `consecutive_passes`)

- "PBB" is an acronym of `PlayerBitBoard` (see `bitboard.py`)which is class object that captures an 
encoded bitmask representation of each player's discs on board during every stage of this game.
- `player_turn` is a `ColorDiscPlayer` class object (see `models.py`) that toggle between these
`ColorDiscPlayer.RED` and `ColorDiscPlayer.WHITE` players.
- `consecutive_passes` for identifying terminal state due to double consecutive-passed moves


### Explaining Bitboard Representation 

A **bitboard** is an integer where each bit represents one board cell:

- bit = 1 → the cell is occupied by the player
- bit = 0 → the cell is not occupied by the player


Just for intuition, a binary representation of a bitboard looks as follows:
`PlayerBitBoard.bitboard = 0b00000000010000000111000000010000`.

The length of this bitboard is `board_size x board_size`.By default, `board_size = 8`, which is the
classic Reversi game board, defines bitboard's bits indexes as follows: 

    
    0  1  2  3  4  5  6  7
    8  9  10 11 12 13 14 15
    16 17 18 19 20 21 22 23
    ...
    56 57 58 59 60 61 62 63


For convenient, `board_size` will be represented by **N**.
General formula for the cell position (row, column) of a single-bit index:

    bit = N x row + column

In terms of compactness, this `GameState` representation is VERY efficient, probably second best after
representing both players state with a single base-3 encoding sequence, so every cell can be
- 0 -> EMPTY
- 1 -> RED
- 2 -> WHITE

However, I think that this base-3 representation is less friendly... 

## Space Complexity Analysis
#### Assuming 64-bit system architecture (so the size of a reference cell is 8 bytes)

By neglecting memory requirement for the `player_turn` and `consecutive_passes` variables 
(meaningless compare to the size of the board) the size of each bitboard is `N^2` bits.
So overall, `GameState` space complexity equals to:

`2 x (N^2) + O(1) = Θ(N^2)`

where `O(1)` refers to the constants pair of `(player_turn, consecutive_passes)`

For example, for `N = 8`, the memory required to represent `GameState` is approximately:
2 x (8^2) = 2x64 = 128 bits = 16 bytes.


### Transition Model

This game states transition of (current_state, player_action) -> new_state
is implemented by:

`GameState.update(player_move: Move) -> GameState`

where:
- `Move` is a class object that stored the player's (row, column) move. Passed move is defined by (None, None) 
- `GameState.update()` returns a new `GameState` class object that
captures the new state of this game, according to the player's move.
- `GameState` uses `player_turn` to update this move on the correct player's bitboard.


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


QUESTION 1.1: when repeating this game run under this configuration, does this game ends with the same result?

Answer:      yes. since the evaluation function that I defined, which calculates the score difference between
                the current player and the opponent player, is purely deterministic and does not include randomness.
                As a result, this evaluation function will resolve the same evaluation score to each and every state
                of this game, which then causes the same players moves in every new run.


QUESTION 1.2:    assuming we have 2 heuristic evaluation functions - how can we check which one of them is more successful?

Answer:      in theory, a heuristic evaluation function h() is considered "good" if it's successfully causing its
                agent to win the game. in practices, and in rivalry game like Reversi, the "goodness" of an evaluation
                function is depended on many factors which includes:
                - the depth of the evaluation's minimax tree
                - the strategy / evaluation function used by the opponent
                - the identity of the agent player (if it is the root player or not)
                - deterministic or stochastic evalutaor (non-deterministic evaluation function should be tested statistically)

                thus, the best answer I have to this question is that h1() is "better" then h2() if:
                - upon both deterministic evaluation functions
                - and upon equal depths:
                    if agent player that uses h1() will always win opponent agent player that uses h2()
                    regardless to it identity (meaning that the h1() player will win the h2() player either when it is
                    or is not the root player).

                - upon both stochastic evaluation functions
                    if statistically h1() player wins h2() player more than h2() player win h1() player



QUESTION 1.3:    assuming that some heuristic evaluation function h() is "good" only in a specific part of the game,
                how and when should we replace it? what are the condition to make this replacement?


Answer:      honestly, I cannot think of a simple answer to this question...


Question 2.1: complexity of a full game run with heuristic evaluation function (depth = 2)?

Answer: 

Question 2.2:

Answer:

Question 2.3 (did not answered)

