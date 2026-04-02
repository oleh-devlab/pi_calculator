from mpmath import mp, mpf, log
import mpmath


# We assume that the polygon is regular.
def calculate_pi(j: mpf, precision=None) -> mpf:
    if precision is None:
        precision = mp.dps

    with mp.workdps(precision):
        # Number of sides of the inscribed polygon, starting with a dodecagon.
        n = mpf(12 * 2**j)
        cos = mpf(mpmath.sqrt(3) / 2)  # cos(30 degrees)
        end = int(log(n / 12, 2))

        for _ in range(1, end + 1):
            cos = mpf(mpmath.sqrt(mpf((1 + cos) / 2)))

        x = mpf(mpmath.sqrt(2 - (2 * cos)))
        return mpf((x * n) / 2)


def count_accurate_digits(error):
    if error == 0:
        return mp.dps

    return int(-mpmath.log10(error))
