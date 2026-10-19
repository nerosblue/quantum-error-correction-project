# Simulating Quantum Error Correction in Python

A hands-on exploration of error correction, starting from a classical repetition code and building up to a quantum surface code, simulated with [Stim](https://github.com/quantumlib/Stim) and decoded with [PyMatching](https://github.com/oscarhiggott/PyMatching).

## Why I built this
<!-- Rewrite in your own words: e.g. your interest in encryption, why fault tolerance matters, the link to error-correcting codes from your EE degree. -->

## Part 1: Classical repetition code
Protect one bit by copying it *n* times, flip each copy with probability *p*, then decode by majority vote.

![Classical repetition code](part1_classical_repetition.png)

**Result:** below p = 0.5, more copies make the decoded bit more reliable. Above it, more copies make things *worse*. That crossover is a **threshold**, the central idea in error correction.

## Part 2: Quantum surface code
Using Stim, I simulated a rotated surface code memory experiment with noise on gates, measurements and resets, at code distances 3, 5 and 7. PyMatching decoded the error syndromes using minimum-weight perfect matching.

![Surface code threshold](part2_surface_code_threshold.png)

**Result:** the curves cross at a physical error rate of roughly **0.8–0.9%**. Below that, larger codes give lower logical error rates (at 0.3% noise, distance 7 is about 6x more reliable than distance 3). Above it, adding qubits makes things worse. This is why hardware quality and decoding both matter for fault-tolerant quantum computing.

## What I learned
<!-- 2–4 bullets in your own words. -->

## Next steps
- Add more distances and shots to estimate the threshold more precisely
- Measure decoding time, since real-time QEC must decode faster than errors accumulate
- Try Riverlane's open-source Deltakit SDK

## Run it
```bash
pip install -r requirements.txt
python part1_classical_repetition.py
python part2_surface_code.py
```
