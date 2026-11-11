# CLA-2 Task 4 — Infinite Loop Detection in Software

**Course:** 21CSC301T — Formal Language and Automata  
**Institution:** SRM Institute of Science and Technology, Tiruchirappalli  
**Team:** Abhishek Toppo (RA2411026050048), Pratyush Gosain (RA2411026050056)

## Problem

Can an algorithm determine whether **every arbitrary program** halts on a given input? No. The general halting problem

**HALT_TM = {⟨M, w⟩ | Turing machine M halts on input w}**

is Turing-recognizable but undecidable. Its complement is not Turing-recognizable. The practical engineering solution is to use *restricted exact analyses*, *bounded simulation*, and *sound but incomplete proofs*.

## Implemented demonstrations

| Method | What it does | Meaning of result |
|---|---|---|
| Finite-state analysis | Stores visited states; detects halting or repeated nonhalting state | Exact for deterministic, pure finite-state transitions with a valid state bound |
| Fuel-bounded execution | Simulates at most k transitions | `TERMINATES` if halt observed; otherwise `UNKNOWN` |
| Ranking-function proof | Proves termination of a specified integer countdown loop | `TERMINATES` for that restricted loop only |

A timeout or exhausted budget **does not prove** that a program runs forever. The simulator is not a general Python program analyzer.

## Run (Python 3.10+, no external packages)

From the repository root:

```powershell
python -m src.loop_detector
python -m unittest discover -s tests -v
```

## Example output

```text
Finite-state cycle
  Verdict: NON_TERMINATING
  Steps: 256
Finite-state halting
  Verdict: TERMINATES
  Steps: 5
Bounded run: insufficient fuel
  Verdict: UNKNOWN
  Steps: 4
Bounded run: enough fuel
  Verdict: TERMINATES
  Steps: 10
Ranking proof: countdown
  Verdict: TERMINATES
  Steps: 7
```

## Computational model and correctness

A deterministic finite-state system has state set S, transition δ: S → S and halting predicate H: S → {true, false}. Starting from s₀, the detector checks H(s), then whether s was previously visited. A repeated nonhalting state forces the same future behavior and therefore proves an infinite cycle. If the bound |S| ≤ N is valid, the procedure terminates after at most N + 1 state observations.

The fuel-bounded simulator checks at most k transitions. If it sees a halt, it returns `TERMINATES`. Otherwise, it returns `UNKNOWN`; a program might halt on step k + 1.

For the countdown loop `while n > 0: n -= 1`, the ranking function f(n) = n takes values in the nonnegative integers and strictly decreases each iteration, proving termination. The function in the code certifies only this specific loop schema.

## Real-world interpretation

Compiler warnings, IDE inspections, watchdogs and CI timeouts provide useful evidence but cannot universally decide program termination. Safety-critical software combines bounded loops, restricted programming models, static analysis, testing and runtime resource limits.

## Project files

```text
FLA_Task4_Repo/
├── README.md
├── GITHUB_SETUP.md
├── .gitignore
├── src/
│   ├── __init__.py
│   └── loop_detector.py
├── tests/
│   ├── __init__.py
│   └── test_loop_detector.py
└── docs/
    └── DEMO_GUIDE.md
```

## Academic context

The implementation follows the Task 4 report's focus on the halting problem, diagonalization, finite-state cycle detection, bounded halting and ranking functions. The code is an educational demonstration, not a universal loop detector.
