# Demonstration and screenshot guide

From the repository root, run:

```powershell
python -m src.loop_detector
python -m unittest discover -s tests -v
```

Capture **real screenshots** of these commands' outputs for your assignment. Show (1) the finite-state cycle verdict, (2) a halting example, (3) the bounded `UNKNOWN` verdict, and (4) passing unit tests.

Explain during the demonstration that a repeated state proves a loop only for a deterministic system whose entire relevant state is modeled. Explain that exhausting the step budget does not prove nontermination.
