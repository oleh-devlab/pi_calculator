import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from pi_core.time_model import load_time_model, predict_time_seconds, time_units


def predict_from_saved_model(model_file_path, j_target):
    try:
        model_data = load_time_model(model_file_path)
    except FileNotFoundError:
        print(f"Model file not found: {model_file_path}")
        print("Run fit_time_model.py first to generate coefficients.")
        return

    predicted_seconds = predict_time_seconds(j_target, model_data)
    units = time_units(predicted_seconds)

    j_min = model_data.get("j_min")
    j_max = model_data.get("j_max")
    if j_min is not None and j_max is not None and not (j_min <= j_target <= j_max):
        print(f"Warning: j={j_target} is outside the trained range [{j_min}, {j_max}].")

    print("\n--- PREDICTION ---")
    print(f"j = {j_target:,}")
    print(f"Estimated time: {units['seconds']:.2f} seconds")
    print(f"Estimated time: {units['minutes']:.2f} minutes")
    print(f"Estimated time: {units['hours']:.2f} hours")
    print(f"Estimated time: {units['days']:.2f} days")


if __name__ == "__main__":
    MODEL_FILE = "time_model_coefficients.json"
    j_to_check = 100000
    predict_from_saved_model(MODEL_FILE, j_to_check)
