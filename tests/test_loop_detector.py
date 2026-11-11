import unittest
from src.loop_detector import (
    Verdict, finite_state_analysis, bounded_execution,
    countdown_ranking_proof, example_cycle, example_halt,
)

class TerminationTests(unittest.TestCase):
    def test_cycle(self):
        result = example_cycle()
        self.assertEqual(result.verdict, Verdict.NON_TERMINATING)
        self.assertEqual(result.steps, 256)

    def test_halt(self):
        result = example_halt()
        self.assertEqual(result.verdict, Verdict.TERMINATES)
        self.assertEqual(result.steps, 5)

    def test_bounded_unknown(self):
        result = bounded_execution(0, lambda x: x + 1, lambda x: x == 10, 4)
        self.assertEqual(result.verdict, Verdict.UNKNOWN)

    def test_bounded_halt(self):
        result = bounded_execution(0, lambda x: x + 1, lambda x: x == 10, 10)
        self.assertEqual(result.verdict, Verdict.TERMINATES)

    def test_zero_fuel(self):
        self.assertEqual(bounded_execution(0, lambda x: x + 1, lambda x: x == 0, 0).verdict,
                         Verdict.TERMINATES)
        self.assertEqual(bounded_execution(0, lambda x: x + 1, lambda x: x == 1, 0).verdict,
                         Verdict.UNKNOWN)

    def test_ranking(self):
        self.assertEqual(countdown_ranking_proof(5).verdict, Verdict.TERMINATES)
        self.assertEqual(countdown_ranking_proof(5).steps, 5)
        self.assertEqual(countdown_ranking_proof(-3).steps, 0)

    def test_bad_bound(self):
        with self.assertRaises(ValueError):
            finite_state_analysis(0, lambda x: x + 1, lambda x: False, 2)

    def test_bad_fuel(self):
        with self.assertRaises(ValueError):
            bounded_execution(0, lambda x: x, lambda x: False, -1)

if __name__ == '__main__':
    unittest.main()
