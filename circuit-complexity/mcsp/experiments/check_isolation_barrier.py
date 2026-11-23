"""Exhaust a 16-bit instance of the shared-map decoder and its two-bit restrictions."""

from itertools import combinations


# Each space has three seed bits and a complement bit. Columns are bit masks.
# The last mask selects four independent prefix positions for decoding.
SPACES = (
    ((0xCCF, 0xF99, 0xF66), (0xAF, 0xB3, 0x52), 0x113),
    ((0xF96, 0xFCC, 0x539), (0x71, 0xF8, 0x91), 0x017),
)
ROWS = (0xFC, 0xF3, 0xCF, 0x3F)
PREFIX = (1 << 12) - 1
TAIL = (1 << 4) - 1
WORD = (1 << 16) - 1


def multiply(columns, seed):
    result = 0
    for i, column in enumerate(columns):
        if (seed >> i) & 1:
            result ^= column
    return result


def expand(bits):
    return sum(((bits & row).bit_count() % 2) << j for j, row in enumerate(ROWS))


def make_fixture():
    words = set()
    decoders = []
    for header, pool, pivots in SPACES:
        inverse = {}
        for seed in range(8):
            middle = multiply(pool, seed)
            for sign in (0, 1):
                prefix = multiply(header, seed) ^ (sign * PREFIX)
                tail = expand(middle) ^ (sign * TAIL)
                words.add(prefix | (tail << 12))
                key = prefix & pivots
                assert key not in inverse
                inverse[key] = (prefix, middle, sign)
        decoders.append((pivots, inverse))
    return words, decoders


def recognizes(word, decoders):
    prefix = word & PREFIX
    for pivots, inverse in decoders:
        predicted, middle, sign = inverse[prefix & pivots]
        if predicted == prefix:
            return (word >> 12) == (expand(middle) ^ (sign * TAIL))
    return False


def check_isolation(words):
    for a, b in combinations(range(16), 2):
        block = (1 << a) | (1 << b)
        fibers = {}
        for word in words:
            fibers.setdefault(word & ~block, set()).add(word & block)
        minterms = {next(iter(fiber)) for fiber in fibers.values() if len(fiber) == 1}
        assert minterms == {0, 1 << a, 1 << b, block}


if __name__ == "__main__":
    words, decoders = make_fixture()
    assert len(words) == 30   # both spaces contain the two constant words
    assert all((word ^ WORD) in words for word in words)
    assert all(((x ^ y) & PREFIX).bit_count() > 2 for x, y in combinations(words, 2))
    assert all(recognizes(word, decoders) == (word in words) for word in range(WORD + 1))
    check_isolation(words)

    balls = {word for word in range(WORD + 1) if word.bit_count() in (0, 1, 15, 16)}
    check_isolation(words | balls)
    print("Checked all 65,536 inputs and all 480 two-bit minterms in each class.")
