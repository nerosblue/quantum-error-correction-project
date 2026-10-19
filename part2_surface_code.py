"""
Part 2: Quantum surface code, simulated with Stim and decoded with PyMatching.

Stim builds a noisy quantum error-correction circuit and samples
"syndromes" (the error-detection signals). PyMatching is the decoder:
it reads the syndromes and guesses which errors happened, using
minimum-weight perfect matching.

Question we answer: is there a physical error rate (the "threshold")
below which making the code bigger makes the logical qubit MORE reliable?
"""
import numpy as np
import matplotlib.pyplot as plt
import stim
import pymatching


def logical_error_rate(distance, p, shots=50_000):
    """Simulate a rotated surface code memory experiment and decode it."""
    circuit = stim.Circuit.generated(
        "surface_code:rotated_memory_z",
        distance=distance,
        rounds=distance,                      # repeat error-checks d times
        after_clifford_depolarization=p,      # noise after each gate
        before_measure_flip_probability=p,    # noisy measurements
        after_reset_flip_probability=p,       # noisy resets
    )

    # Sample: what the detectors saw, and whether the logical qubit actually flipped
    sampler = circuit.compile_detector_sampler()
    detections, actual_flips = sampler.sample(shots, separate_observables=True)

    # Build the decoder from the circuit's error model
    error_model = circuit.detector_error_model(decompose_errors=True)
    decoder = pymatching.Matching.from_detector_error_model(error_model)

    predicted_flips = decoder.decode_batch(detections)
    mistakes = np.any(predicted_flips != actual_flips, axis=1).sum()
    return mistakes / shots


if __name__ == "__main__":
    physical_rates = np.logspace(-2.5, -1.7, 8)  # from about 0.3% to 2%
    distances = [3, 5, 7]                         # code size (bigger = more qubits)

    for d in distances:
        rates = [logical_error_rate(d, p) for p in physical_rates]
        plt.loglog(physical_rates, rates, marker="o", label=f"distance {d}")
        print(f"distance {d}: " + ", ".join(f"{r:.4f}" for r in rates))

    plt.xlabel("Physical error rate per operation")
    plt.ylabel("Logical error rate")
    plt.title("Surface code: below the threshold, bigger codes win")
    plt.legend()
    plt.grid(alpha=0.3, which="both")
    plt.savefig("part2_surface_code_threshold.png", dpi=150, bbox_inches="tight")
    print("Saved plot to part2_surface_code_threshold.png")
