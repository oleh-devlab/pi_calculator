import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from pi_core.time_model import fit_time_model, save_time_model


def fit_and_save_coefficients(benchmark_file_path, model_file_path):
    """
    Loads benchmark results and fits a quadratic time model.
    Saves fitted coefficients for later predictions.
    """
    try:
        model_data = fit_time_model(benchmark_file_path)
    except FileNotFoundError:
        print(f"Benchmark file not found: {benchmark_file_path}")
        print("Run benchmark_runtime.py first to generate benchmark data.")
        return
    except ValueError as e:
        print(f"Cannot fit model: {e}")
        return

    save_time_model(model_data, model_file_path)

    coeffs = model_data["coefficients"]
    print("\n--- FIT COMPLETED ---")
    print(f"Loaded points: {model_data['points_count']}")
    print(f"Training range: j in [{model_data['j_min']}, {model_data['j_max']}]")
    print(f"a = {coeffs['a']:.4e}")
    print(f"b = {coeffs['b']:.4e}")
    print(f"c = {coeffs['c']:.4f}")
    print(f"Saved coefficients to: {model_file_path}")
    print("Use predict_runtime.py to run predictions from the saved model.")


if __name__ == "__main__":
    BENCHMARK_FILE = "benchmark_results.json"
    MODEL_FILE = "time_model_coefficients.json"
    fit_and_save_coefficients(BENCHMARK_FILE, MODEL_FILE)