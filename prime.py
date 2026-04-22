import numba
import time
import numpy as np

# Keep is_prime for reference or potential other uses, though not used by sieve
@numba.jit(nopython=True)
def is_prime(n):
    """Returns True if n is a prime number, else False."""
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    # Check only odd divisors from 3 up to sqrt(n)
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

@numba.jit(nopython=True)
def sieve_of_eratosthenes(limit):
    """
    Generates primes up to a given limit using the Sieve of Eratosthenes.
    Optimized to skip marking even multiples for odd primes.
    Uses NumPy arrays for performance.
    """
    primes_result = np.empty(0, dtype=np.int64)

    if limit >= 2:
        # Create boolean NumPy array
        is_prime_array = np.ones(limit + 1, dtype=np.bool_)
        is_prime_array[0] = is_prime_array[1] = False

        # Mark multiples of 2 first
        # Start from 4 (2*2), step by 2
        is_prime_array[4 : limit+1 : 2] = False

        # Iterate over odd numbers for p (starting from 3)
        # We only need to iterate up to sqrt(limit)
        for p in range(3, int(limit**0.5) + 1, 2):
            # If p is prime (i.e., is_prime_array[p] is True)
            if is_prime_array[p]:
                # Mark multiples of p.
                # Start from p*p.
                # Step by 2*p because we only need to mark odd multiples of odd primes.
                # Even multiples are already marked by p=2.
                is_prime_array[p*p : limit+1 : 2*p] = False
        
        # Collect all prime numbers
        # Use np.where to get indices where is_prime_array is True
        primes_result = np.where(is_prime_array)[0]

    return primes_result

# Redefine primes_up_to to use the sieve for consistency
def primes_up_to(n):
    """Returns a NumPy array of all prime numbers up to n using Sieve of Eratosthenes."""
    return sieve_of_eratosthenes(n)


if __name__ == "__main__":
        n = 10
        print(f"Prime numbers up to {n:,}: {primes_up_to(n)}")
        
        # Use the corrected value for n
        n_large = 1_000_000_000
        start = time.time()
        primes = primes_up_to(n_large)
        end = time.time()
        
        # Calculate all gaps and output them for plotting
        all_gaps = np.diff(primes)
        
        print(f"Prime numbers up to {n_large:,}: {len(primes):_} found in {end - start:.2f} seconds.")
        # Output gaps as comma-separated string. This format is easier to parse.
        # The format is "gaps: <comma_separated_values>"
        print(f"gaps: {','.join(map(str, all_gaps))}")
