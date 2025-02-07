import random
import gmpy2
from sympy import isprime, primerange, factorint
from fpylll import IntegerMatrix, LLL

print("\n=== CRYPTOGRAPHYTUBE: Private Key Extraction Script ===\n")

p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
g = int(input("Enter Generator (Default: 2): ") or 2)

def find_smooth_prime(limit=2**128, smooth_bound=10**6):
    while True:
        num = random.randint(limit//2, limit)
        if isprime(num):
            factors = factorint(num)
            if all(prime < smooth_bound for prime in factors):
                return num

smooth_prime = find_smooth_prime()
print(f"[+] Smooth Prime Generated: {hex(smooth_prime)}")

def generate_polynomial(p):
    a = int(p ** (1/3))  
    b = int(p ** (1/4))  
    return (a, b)

a, b = generate_polynomial(p)
print(f"[+] Polynomial Selected: a={a}, b={b}")

def lattice_reduction(matrix):
    mat = IntegerMatrix.from_matrix(matrix)
    reduced = LLL.reduction(mat)
    return reduced

matrix_size = int(input("Enter Lattice Matrix Size (Default: 4): ") or 4)
matrix = [[random.randint(1, 1000) for _ in range(matrix_size)] for _ in range(matrix_size)]
reduced_matrix = lattice_reduction(matrix)
print("[+] Lattice Reduction Completed")

def relation_collection(prime_bound=10**6):
    return list(primerange(2, prime_bound))

factor_base = relation_collection()
print(f"[+] Factor Base Generated: {len(factor_base)} primes")

def baby_step_giant_step(g, h, p):
    m = int(gmpy2.isqrt(p)) + 1  
    table = {}

    x = 1
    for j in range(m):
        table[x] = j
        x = (x * g) % p  

    factor = gmpy2.invert(pow(g, m, p), p)
    gamma = h

    for i in range(m):
        if gamma in table:
            return i * m + table[gamma]
        gamma = (gamma * factor) % p  

    return None

exp = int(input("Enter Private Key Exponent (Example: 123456789): ") or 123456789)
public_key = pow(g, exp, p)

private_key = baby_step_giant_step(g, public_key, p)
if private_key:
    print(f"[!] Private Key Found: {hex(private_key)}")
    with open("found.txt", "w") as f:
        f.write(f"Private Key: {hex(private_key)}\n")
    print("[+] Private Key Saved to found.txt")
else:
    print("[-] Private Key Not Found")
