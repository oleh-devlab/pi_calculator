from mpmath import mp
import time

from pi_core import DEFAULT_K, calculate_pi, count_accurate_digits

def main():
    j = 5000

    # Derive precision from j using the shared empirical coefficient.
    precision = int(DEFAULT_K * j) + 10 # add a small buffer to ensure we can count accurate digits correctly

    start = time.perf_counter()
    pi = calculate_pi(j, precision)
    end = time.perf_counter()
    
    with mp.workdps(precision):
        error = abs(pi - mp.pi)
        # print(pi)
        # print()
        # print(f"Error: {error}")
        print(f"Execution time: {end - start:.6f} seconds")
        print(f"{count_accurate_digits(error)} digits after the decimal point are correct")

if __name__ == "__main__":
    main()