# Pi Calculator

A program that approximates the value of pi to an arbitrary level of precision.

## Status

🚧 **Work in Progress:** The documentation is being translated and the UI is in development.

## Project Structure

- `main.py` — Main entry point for Pi calculation and accuracy reporting.
- `pi_core/core.py` - Core math functions (Pi calculation and accurate-digit count).
- `pi_core/config.py` - Shared configuration constants (e.g. DEFAULT_K).
- `pi_core/time_model.py` - Time-model utilities (fit, save/load, predict, unit conversions).
- `scripts/calibrate_k.py` - Empirically searches for an effective k coefficient.
- `scripts/benchmark_runtime.py` - Collects benchmark timings for selected j values.
- `scripts/fit_time_model.py` - Fits quadratic time-model coefficients from benchmark data.
- `scripts/predict_runtime.py` - Predicts runtime from saved coefficients.

## Requirements

- Python 3.10+
- mpmath
- numpy

Install dependencies:

```bash
pip install mpmath numpy
```

### Optional: Massive Performance Boost

The core algorithm heavily relies on `mpmath` for arbitrary-precision arithmetic. By default, `mpmath` uses Python's built-in arithmetic, which is fine for basic testing but becomes slow when calculating thousands of digits.

For a **massive speedup**, it is highly recommended to install `gmpy2`. The `mpmath` library will automatically detect it and use its C-based backend without any code changes required on your part.

```bash
pip install gmpy2
```

Note for Windows users: `gmpy2` is a C extension.
If pip fails to build it, you can:
- use conda (`conda install gmpy2`)
- or download a precompiled `.whl` file

If you can't install it, the calculator will still work using the pure Python backend (just slower).

## Usage and changing settings

Currently, the project is in its minimal working state. There is no command-line interface yet. 

To run the calculator, execute:
```bash
python main.py
```

To change the target precision or other parameters, manually edit the configuration variables inside `main.py`. Example:
```py
j = 1000
```

## Understanding the Parameters: j and k

To calculate Pi using the polygon approximation method, the algorithm relies on two primary parameters:

- **`j` (Iterations):** This dictates the number of times the sides of the inscribed polygon are doubled. The total number of sides is $n = 12 \cdot 2^j$. A higher `j` geometrically pushes the polygon closer to a perfect circle, increasing the theoretical number of accurate Pi digits.
- **`k` (Precision Multiplier):** Because the algorithm calculates nested square roots and extremely small differences (e.g., `2 - 2*cos`), standard floating-point arithmetic suffers from catastrophic cancellation. To prevent this, `mpmath` requires a high internal working precision (`dps`). The required precision grows linearly with `j`. Therefore, `k` is an empirical coefficient used to set the internal precision: $DPS = k \cdot j$.

Setting `k` too low results in lost digits due to rounding errors. Setting `k` too high wastes CPU time computing digits that are mathematically inaccessible for the current `j`. 

The included script `scripts/calibrate_k.py` uses multiprocessing to empirically find the "sweet spot"—the minimal mathematically optimal `k` that achieves the theoretical maximum accuracy for a given `j` in the shortest amount of time.

## Typical Workflow

1. Collect benchmark data:

```bash
python scripts/benchmark_runtime.py
```

This creates `benchmark_results.json`.

2. Fit time-model coefficients:

```bash
python scripts/fit_time_model.py
```

This creates `time_model_coefficients.json`.

3. Predict runtime:

```bash
python scripts/predict_runtime.py
```

The output includes seconds, minutes, hours, and days.

### Optional: Re-calibrate k

```bash
python scripts/calibrate_k.py
```

This script searches for an empirical k value and writes a summary to `k_calibration.txt`.

## Limitations
- Hardware-specific timing: benchmark and prediction results depend on CPU, OS, Python version, and whether gmpy2 is available.
- Empirical precision coefficient: `DEFAULT_K` in `pi_core/config.py` is empirical, not mathematically universal.
- Extrapolation is risky: predictions far above the trained range are only rough estimates.

## The History and Essence of the Algorithm

The algorithm was developed and the initial implementation was written in early summer 2025.

The algorithm is based on the similarity between a polygon with a large number of sides and a circle.

At the time of development, I was not aware that Archimedes had already used this method, so this implementation is mainly for educational purposes.

The detailed history of this algorithm's development will be added in future updates