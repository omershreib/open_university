# Maman 15 - Markov Decision Process

**Student:** Omer Shraibshtein (205984271)
**Date:** 10/06/2026


This project implements Markov Decision Process algorithms for a grid-world problem. The implementation supports Value Iteration and Policy Iteration, saves the utility and policy matrices as NumPy files, and creates result plots under the `results/` folder.

---

## 1. Implementation Overview

### 1.1 Python Files

| File | Role |
|---|---|
| `mdp.py` | Defines the `MDP` class, loads the `states` and `rewards` matrices from the `.npz` file, implements the transition model, checks legal/blocked/terminal positions, and serves as the command-line entry point. |
| `parse_args.py` | Parses the command-line arguments: input filename and algorithm name. |
| `utils.py` | Contains common constants and helper functions, including directions, direction labels, state-key conversion, utility initialization, and formatting helpers. |
| `value_iteration.py` | Implements the Value Iteration algorithm using repeated Bellman optimality updates. |
| `run_value_iteration.py` | Runs Value Iteration, converts the returned dictionaries into matrices, saves `.npy` files, and creates the value/policy plots. |
| `run_question_2.py` | Runs all Question 2 experiments: base Value Iteration, different gamma values, and different `p` values. |
| `init_policy.py` | Initializes the policy for Policy Iteration. The initial action is `UP` when possible; otherwise the first legal action is selected according to the order `UP`, `DOWN`, `RIGHT`, `LEFT`. |
| `simplified_value_iteration.py` | Implements the Policy Evaluation stage required in Question 3. This is Simplified Value Iteration: repeatedly update each state using only the action dictated by the current policy. |
| `improve_policy.py` | Implements the Policy Improvement stage. For every state, it chooses the action with the highest Q-value. |
| `policy_iteration.py` | Implements the full Policy Iteration algorithm. One Policy Iteration step is Policy Evaluation followed by Policy Improvement. After every improvement, utilities are reset before the next evaluation. |
| `run_policy_iteration.py` | Runs Policy Iteration, saves the final utility/policy matrices, and creates the required graph of Simplified Value Iteration iterations per Policy Iteration iteration. |
| `run_question_3.py` | Runs the Question 3 Policy Iteration experiment. |
| `policy_translation.py` | Converts action vectors into readable policy symbols such as arrows and indifference combinations. |
| `plot_value_iteration.py` | Draws the utility heat-map. |
| `plot_policy_matrix.py` | Draws the policy grid. |
| `plot_policy_iteration_history.py` | Draws the Question 3 graph: Policy Iteration number vs. Simplified Value Iteration iterations. |
| `Output.md` | Displays the selected result images in the order of Questions 2 and 3. |
| `results/` | Contains all generated plots and saved NumPy result matrices. |

---

### 1.2 Transition Model

The transition model is stochastic. For each desired action `a`, the agent may move in three possible ways:

1. Move in the desired direction with probability `p`.
2. Slip to the left diagonal direction relative to the desired action with probability `(1-p)/2`.
3. Slip to the right diagonal direction relative to the desired action with probability `(1-p)/2`.

Therefore, for every desired action:

```text
p + (1-p)/2 + (1-p)/2 = 1
```

The code first calculates the three successor positions:

```text
desired successor = current position + desired action
left slip successor = current position + left slip action
right slip successor = current position + right slip action
```

If a slip direction is invalid because it leads outside the board or into a blocked state, then the probability of that failed slip is transferred to the desired action. For example, if the right slip is invalid and the left slip is valid, then:

```text
P(desired) = p + (1-p)/2
P(left slip) = (1-p)/2
P(right slip) = 0
```

If both slips are invalid, then the desired action receives probability `1`.

The Q-value is computed as:

```text
Q(s,a) = R(s) + gamma * sum over s' of P(s' | s,a) * U(s')
```

Value Iteration uses:

```text
U'(s) = max over a of Q(s,a)
```

Policy Evaluation inside Policy Iteration uses the simplified update:

```text
U'(s) = Q(s, pi(s))
```

where `pi(s)` is the action dictated by the current policy.

---

### 1.3 How to Run the Program

Run the commands from the `maman15` folder.

For Value Iteration:

```bash
python -m mdp input_2026b.npz ValueIteration
```

For Policy Iteration:

```bash
python -m mdp input_2026b.npz PolicyIteration
```

The required image output files are saved in the `results/` folder.

The utility and policy matrix result by value iteration and policy iteration are saved in `npz_results/`

---

## 2. Question 2 - Value Iteration

### 2.a Base Run

For Question 2.a, I used:

```text
epsilon = 0.001
gamma = 0.9
p = 0.8
```

The algorithm converged after:

```text
50 Value Iteration iterations
```

---

### 2.b Effect of Gamma

The tested gamma values were:

```text
0, 0.25, 0.5, 0.75, 1
```

Measured convergence iterations:

| Gamma | Value Iteration iterations |
|---:|---:|
| 0 | 1 |
| 0.25 | 9 |
| 0.5 | 17 |
| 0.75 | 36 |
| 1 | 94 |

Conclusion: increasing `gamma` gives more importance to future rewards. When `gamma = 0`, only the immediate reward matters, so convergence is immediate. As `gamma` increases, rewards farther in the future affect the current state's utility more strongly. Therefore the utility influence spreads farther across the board, and convergence becomes slower. In the experiment, this is clear: the number of iterations increased from `1` when `gamma = 0` to `94` when `gamma = 1`.

---

### 2.c Effect of p

The tested values of `p` were:

```text
0.4, 0.6, 0.8, 1
```

Measured convergence iterations:

| p | Value Iteration iterations |
|---:|---:|
| 0.4 | 86 |
| 0.6 | 68 |
| 0.8 | 50 |
| 1 | 26 |

Conclusion: `p` controls how reliable the desired action is. When `p` is low, the environment is more stochastic, so the agent must consider more uncertainty from accidental slips. This makes the utility propagation less direct and usually slows convergence. When `p` increases, the environment becomes more deterministic, so the desired action is more reliable and the policy can move more directly toward good rewards and away from bad rewards. In the experiment, convergence became faster as `p` increased: from `86` iterations for `p = 0.4` to `26` iterations for `p = 1`.

#### Multiplying all rewards by a constant

If all rewards are multiplied by a positive constant, for example `10`, then all utility values are also multiplied by the same constant. The optimal policy should not change, because the relative preference between actions remains the same. In other words, multiplying every reward by `10` changes the scale of the utility matrix, but it does not change which action is best in each state.

---

## 3. Question 3 - Policy Iteration

Policy Iteration was implemented according to the assignment requirement:

1. Initialize the policy to `UP` in every state.
2. If `UP` is impossible, choose the first legal action according to this order:

```text
UP, DOWN, RIGHT, LEFT
```

3. Run Policy Evaluation using Simplified Value Iteration.
4. Run Policy Improvement.
5. After policy improvement, reset the expected utility values to zero before the next Simplified Value Iteration evaluation.
6. Stop when the policy is stable.

The algorithm converged after:

```text
19 Policy Iteration iterations
```

The number of Simplified Value Iteration iterations required in each Policy Iteration iteration was:

```text
[88, 70, 60, 53, 52, 51, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50]
```

The total number of Simplified Value Iteration iterations was therefore:

```text
1024
```

### Number of Possible Policies

Let `S_valid` be the set of all valid non-terminal states. For every state `s`, let `A(s)` be the set of legal actions in that state.

The exact number of deterministic policies is:

```text
product over all valid non-terminal states s of |A(s)|
```

That is:

```text
|A(s1)| * |A(s2)| * ... * |A(sn)|
```

If every valid non-terminal state had exactly four legal actions, the number would be:

```text
4^n
```

where `n` is the number of valid non-terminal states. In this implementation, the exact number can be computed directly from the board with:

```python
from math import prod

num_policies = prod(
    len(mdp.get_actions([x, y]))
    for x in range(mdp.shape[0])
    for y in range(mdp.shape[1])
    if mdp.is_updatable_pos([x, y])
)

print(num_policies)
```

This formula is the required policy-permutation count because each valid non-terminal state independently chooses one legal action.

---

## 4. Final Conclusions

### 4.1 Where was convergence faster?

There are two possible ways to compare convergence:

1. Compare only the outer algorithm iterations.
2. Compare the total number of utility-update sweeps.

Using outer iterations:

| Algorithm | Outer iterations |
|---|---:|
| Value Iteration | 50 |
| Policy Iteration | 19 |

By this measurement, Policy Iteration converged in fewer outer iterations.

However, each Policy Iteration iteration includes a full Simplified Value Iteration evaluation. The total number of Simplified Value Iteration iterations was:

```text
1024
```

Therefore, if we compare the total number of repeated utility-update sweeps, Value Iteration was faster in this implementation:

| Algorithm | Utility-update sweeps |
|---|---:|
| Value Iteration | 50 |
| Policy Iteration | 1024 |

Conclusion: Policy Iteration required fewer outer iterations, but Value Iteration required fewer total utility-update sweeps.

---

### 4.2 Are the final values and policies the same?

The final Value Iteration and Policy Iteration results are expected to represent the same optimal solution. The final policies should be the same, and the final utility matrices should be equal or very close up to small numerical differences caused by iterative convergence and floating-point precision.

In the generated plots, the final utility heat-maps and policy matrices produced by Value Iteration and Policy Iteration are visually consistent. Therefore, the result supports the expected conclusion: both algorithms converge to the same optimal policy, while small numerical differences in utilities may still exist because both methods stop according to an epsilon-based convergence threshold.

---

## 5. Output Files

The generated files are saved under the `results/` folder, including:

- Value Iteration utility plots
- Value Iteration policy plots
- Policy Iteration utility plot
- Policy Iteration policy plot
- Simplified Value Iteration count plot
- Saved `.npy` utility matrices
- Saved `.npy` policy matrices

The file `Output.md` displays selected images from the `results/` folder in the order of the assignment questions.
