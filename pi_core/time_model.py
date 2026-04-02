import json
from datetime import datetime, timezone

def _load_benchmark_points(json_file_path):
    import numpy as np

    with open(json_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    x_data = np.array([int(j) for j in data.keys()], dtype=float)
    y_data = np.array([float(t) for t in data.values()], dtype=float)

    if len(x_data) < 3:
        raise ValueError("At least 3 points are required to fit a quadratic model.")

    return x_data, y_data


def fit_time_model(json_file_path):
    import numpy as np

    x_data, y_data = _load_benchmark_points(json_file_path)

    a, b, c = np.polyfit(x_data, y_data, 2)

    return {
        "model": "quadratic",
        "degree": 2,
        "coefficients": {
            "a": float(a),
            "b": float(b),
            "c": float(c),
        },
        "benchmark_source": json_file_path,
        "points_count": int(len(x_data)),
        "j_min": int(np.min(x_data)),
        "j_max": int(np.max(x_data)),
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
    }


def save_time_model(model_data, model_file_path):
    with open(model_file_path, "w", encoding="utf-8") as f:
        json.dump(model_data, f, indent=4)


def load_time_model(model_file_path):
    with open(model_file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def predict_time_seconds(j, model_data):
    coeffs = model_data["coefficients"]
    a = coeffs["a"]
    b = coeffs["b"]
    c = coeffs["c"]
    seconds = a * (j**2) + b * j + c
    return max(0.0, float(seconds))


def time_units(seconds):
    return {
        "seconds": float(seconds),
        "minutes": float(seconds) / 60.0,
        "hours": float(seconds) / 3600.0,
        "days": float(seconds) / 86400.0,
    }
