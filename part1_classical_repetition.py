"""
Part 1: Classical repetition code (no quantum needed).

Idea: to protect one bit, copy it n times. Noise flips each copy with
probability p. Decode by majority vote. If fewer than half the copies
flip, we recover the original bit.

Question we answer: when does adding more copies actually help?
"""
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(seed=42)  # fixed seed so results are repeatable


def encode(bit, n):
    """Copy one bit n times, e.g. 1 -> [1, 1, 1]."""
    return np.full(n, bit)


def add_noise(codeword, p):
    """Flip each bit independently with probability p."""
    flips = rng.random(codeword.size) < p
    return codeword ^ flips


def decode(received):
    """Majority vote: return 1 if more than half the bits are 1."""
    return int(received.sum() > received.size / 2)


def logical_error_rate(n, p, trials=20_000):
    """Fraction of trials where the decoded bit is wrong."""
    errors = 0
    for _ in range(trials):
        bit = rng.integers(2)
        if decode(add_noise(encode(bit, n), p)) != bit:
            errors += 1
    return errors / trials


if __name__ == "__main__":
    physical_rates = np.linspace(0.01, 0.6, 15)
    code_sizes = [1, 3, 5, 7]  # n=1 means "no protection"

    for n in code_sizes:
        rates = [logical_error_rate(n, p) for p in physical_rates]
        plt.plot(physical_rates, rates, marker="o", label=f"n = {n} copies")
        print(f"n={n}: done")

    plt.xlabel("Physical error rate (chance each copy flips)")
    plt.ylabel("Logical error rate (chance decoded bit is wrong)")
    plt.title("Classical repetition code: more copies help only below p = 0.5")
    plt.axvline(0.5, color="grey", linestyle="--", label="threshold (p = 0.5)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.savefig("part1_classical_repetition.png", dpi=150, bbox_inches="tight")
    print("Saved plot to part1_classical_repetition.png")
