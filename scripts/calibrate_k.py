from mpmath import mp
import mpmath
import time
import multiprocessing
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from pi_core import calculate_pi as pi, count_accurate_digits

def worker_task(args):
    k, j = args
    try:
        start_time = time.perf_counter()
        with mp.workdps(int(k * j)):
            error = abs(pi(j, int(k * j)) - mp.pi)
            er = count_accurate_digits(error)
        end_time = time.perf_counter()
        seconds = end_time - start_time
        return (k, er, seconds, None)
    except Exception as e:
        return (k, -1, 0, str(e))


if __name__ == "__main__":
    j = 3000
    k_start = 1.203998
    k_step =  0.000001
    
    # Settings for multiprocessing
    NUM_CORES = 4

    max_er = 0
    min_k = -1
    final_seconds = "0"
    plateau_count = 0


    log_12 = mpmath.log10(12)
    log_2 = mpmath.log10(2)
    theoretical_max_digits = int(2 * log_12 + 2 * j * log_2)
    print(f"Theoretical maximum for j={j} is ~{theoretical_max_digits} digits.")
    
    delta_dps = k_step * j
    dynamic_plateau_limit = max(3, int(30 / delta_dps))
    print(f"Dynamic plateau limit set to {dynamic_plateau_limit} iterations.")

    max_theoretical_digits_error = int(0.01 * theoretical_max_digits)
    print(f"Acceptable error threshold set to {max_theoretical_digits_error} digits.")
    
    print(f"Starting calculations on {NUM_CORES} cores...")

    with multiprocessing.Pool(processes=NUM_CORES) as pool:
        task_generator = ((k_start + i * k_step, j) for i in range(10000))

        for k_res, er_res, sec_res, error_msg in pool.imap(worker_task, task_generator):
            if error_msg:
                print(f"Error for k={k_res}: {error_msg}")
                continue

            # print(f"Tested k={k_res}: {er_res} correct digits, time={sec_res:.4f}s")

            if er_res > max_er:
                max_er = er_res
                min_k = k_res
                final_seconds = f"{sec_res:.6f}"
                plateau_count = 0
                
            elif er_res == max_er and max_er > 0:
                plateau_count += 1

            else:
                plateau_count = 0
            
            if (plateau_count >= dynamic_plateau_limit):
                if max_er >= (theoretical_max_digits - max_theoretical_digits_error):
                    print(f"\nReal accuracy plateau reached at {max_er} digits!")
                    print(f"The mathematically optimal minimal k is {min_k}")
                    pool.terminate()
                    break
                else:
                    plateau_count = 0

    if min_k != -1:
        print(f"\n--- RESULTS ---")
        print(f"Best k: {min_k}")
        print(f"Calculated digits after decimal: {max_er}")
        
        file_name = "k_calibration.txt"

        try:
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(f"Calculated {max_er} digits after the decimal point of Pi. ")
                f.write(f"Time taken for the best result: {final_seconds} seconds. ")
                f.write(f"For j={j} and k={min_k}.")
            print(f"Results saved here: {file_name}")
        except Exception as e:
            print(f"Failed to save the file: {e}")
    else:
        print("No valid results found.")