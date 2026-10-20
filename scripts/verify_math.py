#!/usr/bin/env python3
"""Independent brute-force check of every answer shown in the videos.

Runs in CI before rendering; a wrong answer fails the workflow.
Add one function per new problem.
"""

from fractions import Fraction as F
from itertools import combinations, product

PRIMES = {2, 3, 5, 7, 11}


def p01_dadu_berbeda() -> F:
    pairs = [(a, b) for a, b in product(range(1, 7), repeat=2) if a != b]
    return F(sum((a + b) in PRIMES for a, b in pairs), len(pairs))


def p02_tiga_koin() -> F:
    given = [o for o in product("GA", repeat=3) if "G" in o]
    return F(sum(o.count("G") == 2 for o in given), len(given))


def p03_kartu_bridge() -> F:
    deck = [(rank, suit) for rank in range(1, 14) for suit in "SHDC"]
    face = lambda c: c[0] >= 11  # J, Q, K  # noqa: E731
    red = lambda c: c[1] in "HD"  # noqa: E731
    pairs = list(combinations(deck, 2))
    good = sum(face(a) + face(b) == 1 and red(a) != red(b) for a, b in pairs)
    return F(good, len(pairs))


def p04_empat_koin() -> F:
    outcomes = list(product("AG", repeat=4))  # A = angka, G = gambar
    return F(sum(o.count("A") == 3 for o in outcomes), len(outcomes))


def p05_spinner_koin() -> F:
    outcomes = list(product(range(1, 7), "AG"))  # spinner with six equal sectors, fair coin
    return F(sum(n % 2 == 1 and c == "G" for n, c in outcomes), len(outcomes))


def p06_dua_dadu_atau() -> F:
    pairs = list(product(range(1, 7), repeat=2))
    return F(sum(a + b > 9 or a == b for a, b in pairs), len(pairs))


def p07_spinner_harapan() -> F:
    primes = [n for n in range(1, 9) if n > 1 and all(n % d for d in range(2, n))]
    return F(len(primes), 8) * 144  # expected frequency = probability x number of trials


EXPECTED = {
    p01_dadu_berbeda: F(7, 15),  # option B
    p02_tiga_koin: F(3, 7),  # option B
    p03_kartu_bridge: F(40, 221),  # option B
    p04_empat_koin: F(1, 4),  # option B
    p05_spinner_koin: F(1, 4),  # option B
    p06_dua_dadu_atau: F(5, 18),  # option B
    p07_spinner_harapan: F(72),  # option C
}

if __name__ == "__main__":
    ok = True
    for fn, want in EXPECTED.items():
        got = fn()
        ok &= got == want
        print(f"[{'PASS' if got == want else 'FAIL'}] {fn.__name__}: {got} (video shows {want})")
    raise SystemExit(0 if ok else 1)
