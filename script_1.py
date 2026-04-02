from mpmath import mp, mpf, log
import mpmath
import time
import os
import multiprocessing

# Some variables are in Ukrainian temporarily

# TODO: Import this func from the algorithm file
def pi(точність, степінь):
    mp.dps = точність
    n = mpf(12*2**степінь)
    cos = mpf(mpmath.sqrt(3)/2)
    end = int(log((n/12), 2))
    for iter in range(1, (end+1)):
        cos = mpf(mpmath.sqrt(mpf((1+cos)/2)))
    x = mpf(mpmath.sqrt(2-(2*cos)))
    pi_val = mpf((x*n)/2)
    error = abs(pi_val - mp.pi)
    return error

# TODO: Also import this function.
def leading_zeros_after_decimal(number):
    s = str(number)
    if '.' not in s:
        return 0
    fractional = s.split('.')[1]
    count = 0
    for digit in fractional:
        if digit == '0':
            count += 1
        else:
            break
    return count

def worker_task(args):
    k, j = args
    try:
        start_time = time.perf_counter()
        error = pi(int(k * j), j)
        er = leading_zeros_after_decimal(error)
        end_time = time.perf_counter()
        seconds = end_time - start_time
        return (k, er, seconds, None)
    except Exception as e:
        return (k, -1, 0, str(e))


if __name__ == "__main__":
    j = 10000
    k_start = 1.75
    k_step = 0.01
    max_pohybka = mpmath.sqrt(j) + 5
    
    # Settings for multiprocessing
    NUM_CORES = 4
    # Number of tasks "in flight" in the queue.
    TASKS_IN_FLIGHT = NUM_CORES * 2 

    max_er = 0
    min_k = -1
    final_seconds = "0"
    
    print(f"Starting calculations on {NUM_CORES} cores...")

    with multiprocessing.Pool(processes=NUM_CORES) as pool:
        task_generator = ((k_start + i * k_step, j) for i in range(100000))

        for k_res, er_res, sec_res, error_msg in pool.imap_unordered(worker_task, task_generator):
            
            if error_msg:
                # print(f"Error with k={k_res}: {error_msg}")
                continue

            print(f"Received result: er={er_res}, k={k_res:.2f}, time={sec_res:.4f}s")

            if er_res > max_pohybka:
                if er_res > max_er:
                    print(f"Found a new best result")
                    max_er = er_res
                    min_k = k_res
                    final_seconds = f"{sec_res:.6f}"
                    
                    print("Stopping all further calculations.")
                    pool.terminate() # Force stop all child processes
                    break

    if min_k != -1:
        print(f"Results")
        print(f"Best k: {min_k}")
        print(f"Calculated digits after decimal: {max_er}")
        
        try:
            with open("my_calc_pi_doc.txt", "w", encoding="utf-8") as f:
                f.write(f"Calculated {max_er} digits after the decimal point of Pi. ")
                f.write(f"Time taken for the best result: {final_seconds} seconds.")
                f.write(f"For {j}")
            print(f"Results saved here: my_calc_pi_doc.txt")
        except Exception as e:
            print(f"Failed to save the file: {e}")
    else:
        print("No valid results found within the given parameters.")