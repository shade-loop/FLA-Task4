"""CLA-2 Task 4: restricted approaches to software termination analysis.

No algorithm here decides termination for arbitrary Python programs.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Hashable, TypeVar

S = TypeVar('S', bound=Hashable)

class Verdict(str, Enum):
    TERMINATES = 'TERMINATES'
    NON_TERMINATING = 'NON_TERMINATING'
    UNKNOWN = 'UNKNOWN'

@dataclass(frozen=True)
class Result:
    verdict: Verdict
    steps: int
    explanation: str
    trace: tuple[object, ...]


def finite_state_analysis(initial: S, transition: Callable[[S], S],
                          is_halted: Callable[[S], bool],
                          max_states: int) -> Result:
    """Exact for deterministic, pure finite-state transitions with <= max_states states.

    A repeated nonhalting state proves a cycle. The bound is a verified
    assumption supplied by the caller, not inferred for arbitrary code.
    """
    if max_states < 1:
        raise ValueError('max_states must be positive')
    visited: set[S] = set()
    trace: list[S] = []
    state = initial
    for step in range(max_states + 1):
        if is_halted(state):
            trace.append(state)
            return Result(Verdict.TERMINATES, step, 'Reached a halting state.', tuple(trace))
        if state in visited:
            trace.append(state)
            return Result(Verdict.NON_TERMINATING, step,
                          'Repeated a nonhalting state in a deterministic system.', tuple(trace))
        if len(visited) >= max_states:
            raise ValueError('More distinct nonhalting states than declared max_states; assumption invalid')
        visited.add(state)
        trace.append(state)
        state = transition(state)
    raise AssertionError('unreachable')


def bounded_execution(initial: S, transition: Callable[[S], S],
                      is_halted: Callable[[S], bool], fuel: int) -> Result:
    """Executes at most fuel transitions; exhaustion means UNKNOWN, not LOOP."""
    if fuel < 0:
        raise ValueError('fuel must be nonnegative')
    state = initial
    trace: list[S] = []
    for step in range(fuel + 1):
        trace.append(state)
        if is_halted(state):
            return Result(Verdict.TERMINATES, step, 'Halted within the step budget.', tuple(trace))
        if step == fuel:
            return Result(Verdict.UNKNOWN, step,
                          'Budget exhausted; execution may halt later or run forever.', tuple(trace))
        state = transition(state)
    raise AssertionError('unreachable')


def countdown_ranking_proof(start: int) -> Result:
    """Sound proof for the SPECIFIC transition n -> n-1 while n > 0.

    Ranking function f(n)=n is a nonnegative integer and strictly decreases
    on each iteration. This is not a generic termination prover.
    """
    if not isinstance(start, int):
        raise TypeError('start must be an integer')
    return Result(Verdict.TERMINATES, max(start, 0),
                  'For n > 0, f(n)=n decreases by 1 and is bounded below by 0.',
                  (start, max(start, 0)))


def example_cycle() -> Result:
    # Eight-bit counter cycles modulo 256; state 0 never equals halt sentinel 256.
    return finite_state_analysis(0, lambda x: (x + 1) % 256,
                                 lambda x: x == 256, max_states=256)


def example_halt() -> Result:
    return finite_state_analysis(0, lambda x: x + 1,
                                 lambda x: x == 5, max_states=6)


def main() -> None:
    examples = [
        ('Finite-state cycle', example_cycle()),
        ('Finite-state halting', example_halt()),
        ('Bounded run: insufficient fuel', bounded_execution(0, lambda x: x + 1, lambda x: x == 10, 4)),
        ('Bounded run: enough fuel', bounded_execution(0, lambda x: x + 1, lambda x: x == 10, 12)),
        ('Ranking proof: countdown', countdown_ranking_proof(7)),
    ]
    print('CLA-2 TASK 4 | RESTRICTED TERMINATION ANALYSIS')
    print('=' * 55)
    for name, result in examples:
        print(f'\n{name}\n  Verdict: {result.verdict.value}\n  Steps: {result.steps}')
        print(f'  Reason: {result.explanation}')
        print(f'  Trace preview: {list(result.trace[:12])}' + (' ...' if len(result.trace) > 12 else ''))
    print('\nReminder: UNKNOWN is not proof of non-termination.')

if __name__ == '__main__':
    main()
