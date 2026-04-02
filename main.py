from mpmath import mp, mpf, log
import mpmath
import time

# We assume that the polygon is regular

def main():
    mp.dps = 25000
    n = mpf(12*2**10000) # Number of sides of the inscribed polygon, starting with a dodecagon (12 sides) and doubling the number of sides

    start = time.perf_counter()

    cos = mpf(mpmath.sqrt(3)/2) # cos of 30 degrees

    angle = mpf(360/n)

    end = int(log((n/12), 2))
    print(end)
    for iter in range(1, (end+1)):
        cos = mpf(mpmath.sqrt(mpf((1+cos)/2)))

    x = mpf(mpmath.sqrt(2-(2*cos))) # length of the side of the inscribed polygon with n sides
    pi = mpf((x*n)/2)

    end = time.perf_counter()
    
    error = abs(pi - mp.pi)
    print(pi)
    print()
    print(f"Error: {error}")
    print(f"Execution time: {end - start:.6f} seconds")
    print(f"{leading_zeros_after_decimal(error)} digits after the decimal point are correct")

def leading_zeros_after_decimal(number):
    """
    Counts the number of zeros after the decimal point until the first non-zero digit.
    """
    s = str(number)
    if '.' not in s:
        return 0 # No decimal point, so no leading zeros

    fractional = s.split('.')[1]
    count = 0
    for digit in fractional:
        if digit == '0':
            count += 1
        else:
            break
    return count

if __name__ == "__main__":
    main()