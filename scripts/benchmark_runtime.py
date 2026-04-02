import time
import multiprocessing
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from pi_core import DEFAULT_K, calculate_pi

def benchmark_worker(j_value):
    """
    Runs one calculation for the given 'j' and returns execution time.
    Uses a fixed 'k' because it has limited impact on total runtime.
    """
    # Use the shared empirical coefficient.
    k = DEFAULT_K
    
    try:
        start_time = time.perf_counter()
        calculate_pi(j_value, int(k * j_value))
        end_time = time.perf_counter()
        
        seconds = end_time - start_time
        print(f"  Completed for j={j_value}, time: {seconds:.4f} s")
        return (j_value, seconds, None)
    except Exception as e:
        print(f"  Error for j={j_value}: {e}")
        return (j_value, -1, str(e))

# --- Main block ---
if __name__ == "__main__":
    # --- Benchmark settings ---
    # List of 'j' values for which execution time will be measured.
    # This set is selected to collect useful data within roughly 10 minutes.
    J_VALUES_TO_TEST = [5000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000]
    
    # Number of CPU cores for parallel benchmark execution.
    NUM_CORES = 4
    
    print("Starting data collection for performance analysis...")
    print(f"Testing {len(J_VALUES_TO_TEST)} 'j' values on {NUM_CORES} cores.")
    
    results_data = {}
    
    # Create a process pool.
    with multiprocessing.Pool(processes=NUM_CORES) as pool:
        # pool.map distributes J_VALUES_TO_TEST values across workers.
        results = pool.map(benchmark_worker, J_VALUES_TO_TEST)
    
    print("\n--- Data collection completed ---")
    print("Collected results (j, time in seconds):")
    
    # Filter out failed runs and fill the results dictionary.
    valid_results = []
    for j_res, time_res, error_msg in results:
        if not error_msg:
            print(f"  j = {j_res:<5} | Time = {time_res:.4f} s")
            results_data[j_res] = time_res
            valid_results.append((j_res, time_res))

    # Save results to a file for later analysis.
    file_path = "benchmark_results.json"
    try:
        with open(file_path, "w") as f:
            json.dump(results_data, f, indent=4)
        print(f"\nData saved to file: {file_path}")
        print("These data can now be used to build a more accurate model.")
    except Exception as e:
        print(f"\nFailed to save file: {e}")