"""
Dynamic Programming Assignment - Longest Common Subsequence
Implement three versions: naive recursive, memoization, and tabulation.
"""

import json
import time


# ============================================================================
# PART 1: NAIVE RECURSIVE SOLUTION
# ============================================================================

def lcs_recursive(seq1, seq2):
    """
    Find the length of longest common subsequence using pure recursion.
    """

    # Base case: if either sequence is empty
    if len(seq1) == 0 or len(seq2) == 0:
        return 0

    # Case 1: last characters match
    if seq1[-1] == seq2[-1]:
        return 1 + lcs_recursive(seq1[:-1], seq2[:-1])

    # Case 2: last characters don't match
    else:
        option1 = lcs_recursive(seq1[:-1], seq2)
        option2 = lcs_recursive(seq1, seq2[:-1])
        return max(option1, option2)


# ============================================================================
# PART 2: MEMOIZATION (TOP-DOWN WITH CACHING)
# ============================================================================

def lcs_memoization(seq1, seq2):
    """
    Find the length of longest common subsequence using memoization.
    """

    cache = {}

    def helper(i, j):

        # Check cache first
        if (i, j) in cache:
            return cache[(i, j)]

        # Base case
        if i == 0 or j == 0:
            return 0

        # If characters match
        if seq1[i-1] == seq2[j-1]:
            result = 1 + helper(i-1, j-1)

        # If characters don't match
        else:
            result = max(helper(i-1, j), helper(i, j-1))

        # Store result in cache
        cache[(i, j)] = result
        return result

    return helper(len(seq1), len(seq2))


# ============================================================================
# PART 3: TABULATION (BOTTOM-UP WITH TABLE)
# ============================================================================

def lcs_tabulation(seq1, seq2):
    """
    Find the length of longest common subsequence using tabulation.
    """

    m = len(seq1)
    n = len(seq2)

    # Create table filled with 0
    table = [[0 for _ in range(n + 1)] for _ in range(m + 1)]

    # Fill the table
    for i in range(1, m + 1):
        for j in range(1, n + 1):

            # Characters match
            if seq1[i-1] == seq2[j-1]:
                table[i][j] = 1 + table[i-1][j-1]

            # Characters don't match
            else:
                table[i][j] = max(table[i-1][j], table[i][j-1])

    return table[m][n]


# ============================================================================
# TESTING & TIMING
# ============================================================================

def load_sequence(filename):
    """Load DNA sequence from JSON file."""
    with open(f"sequences/{filename}", "r") as f:
        return json.load(f)


def test_small_cases():
    """Test all implementations on small known cases."""
    print("="*70)
    print("TESTING ON SMALL CASES")
    print("="*70 + "\n")
    
    test_cases = [
        ("AGGTAB", "GXTXAYB", 4),
        ("ABCDGH", "AEDFHR", 3),
        ("ABC", "AC", 2),
        ("", "ABC", 0),
    ]
    
    for seq1, seq2, expected in test_cases:
        print(f"Test: '{seq1}' vs '{seq2}'")
        print(f"  Expected LCS length: {expected}")
        
        result = lcs_recursive(seq1, seq2)
        print(f"  Recursive: {result}")

        result = lcs_memoization(seq1, seq2)
        print(f"  Memoization: {result}")

        result = lcs_tabulation(seq1, seq2)
        print(f"  Tabulation: {result}")

        print()


def time_recursive():
    """Time the recursive solution on progressively larger inputs."""
    print("\n" + "="*70)
    print("TIMING RECURSIVE SOLUTION")
    print("="*70 + "\n")
    
    sizes = [10, 20, 50]
    
    for size in sizes:
        data = load_sequence(f"dna_{size}.json")
        seq1 = data["sequence1"]
        seq2 = data["sequence2"]
        
        print(f"Sequence length: {size}")
        
        start = time.perf_counter()
        result = lcs_recursive(seq1, seq2)
        elapsed = time.perf_counter() - start
        
        print(f"  LCS length: {result}")
        print(f"  Time: {elapsed:.4f} seconds\n")
        
        if elapsed > 5:
            print("Stopping because recursion is too slow.\n")
            break


def compare_all_approaches():
    """Compare performance of all approaches."""
    print("\n" + "="*70)
    print("COMPARING ALL APPROACHES")
    print("="*70 + "\n")
    
    sizes = [10, 20, 50, 100, 200, 500, 1000]

    print(f"{'Size':<10} {'Recursive':<15} {'Memoization':<15} {'Tabulation':<15}")
    print("-" * 70)

    for size in sizes:
        data = load_sequence(f"dna_{size}.json")
        seq1 = data["sequence1"]
        seq2 = data["sequence2"]

        # Recursive
        if size <= 20:
            start = time.perf_counter()
            lcs_recursive(seq1, seq2)
            rec_time = time.perf_counter() - start
            rec_str = f"{rec_time:.4f}s"
        else:
            rec_str = "Too slow"

        # Memoization
        try:
            start = time.perf_counter()
            lcs_memoization(seq1, seq2)
            mem_time = time.perf_counter() - start
            mem_str = f"{mem_time:.4f}s"
        except:
            mem_str = "ERROR"

        # Tabulation
        start = time.perf_counter()
        lcs_tabulation(seq1, seq2)
        tab_time = time.perf_counter() - start
        tab_str = f"{tab_time:.4f}s"

        print(f"{size:<10} {rec_str:<15} {mem_str:<15} {tab_str:<15}")


if __name__ == "__main__":
    print("DYNAMIC PROGRAMMING ASSIGNMENT\n")

    test_small_cases()
    time_recursive()
    compare_all_approaches()