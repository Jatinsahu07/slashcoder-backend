# app/data/practice_problems.py

PRACTICE_PROBLEMS = {

    # ---------------------- VERY EASY (15) ----------------------
    # Replace the "Very Easy" section in app/data/practice_problems.py with this list

"Very Easy": [
    {
        "id": "sum_even_digits",
        "title": "Sum of Even Digits",
        "description": "Compute the sum of even digits of a non-negative integer N.",
        "description_full": "Given a non-negative integer N, compute the sum of all digits of N that are even (0,2,4,6,8). Print 0 if none.",
        "input": "Single integer N",
        "output": "Sum of even digits",
        "example": "Input:\n123456\nOutput:\n12",
        "constraints": "0 ≤ N < 10^1000",
        "explanation": "",
        "tests": [
            {"input": "123456", "output": "12"},
            {"input": "7", "output": "0"},
            {"input": "24680", "output": "20"}
        ]
    },
    {
        "id": "product_nonzero_digits",
        "title": "Product of Non-zero Digits",
        "description": "Multiply all non-zero digits of N.",
        "description_full": "Given a positive integer N, compute the product of its digits ignoring any zeros. If all digits are zero, output 0.",
        "input": "Single integer N",
        "output": "Product of non-zero digits",
        "example": "Input:\n1023\nOutput:\n6",
        "constraints": "1 ≤ length(N) ≤ 1000",
        "explanation": "",
        "tests": [
            {"input": "1023", "output": "6"},
            {"input": "1000", "output": "1"},
            {"input": "305", "output": "15"}
        ]
    },
    {
        "id": "count_set_bits",
        "title": "Count Set Bits",
        "description": "Count number of 1s in binary representation.",
        "description_full": "Given a non-negative integer N, print the number of set bits (1s) in its binary representation.",
        "input": "Single integer N",
        "output": "Count of ones in binary",
        "example": "Input:\n5\nOutput:\n2",
        "constraints": "0 ≤ N ≤ 10^9",
        "explanation": "",
        "tests": [
            {"input": "5", "output": "2"},
            {"input": "0", "output": "0"},
            {"input": "1023", "output": "10"}
        ]
    },
    {
        "id": "digit_frequency",
        "title": "Digit Frequency",
        "description": "Count frequency of digit D in N.",
        "description_full": "Given a non-negative integer N and a single digit D (0–9), print how many times D appears in N.",
        "input": "Two space-separated values: N D",
        "output": "Frequency count",
        "example": "Input:\n122321 2\nOutput:\n3",
        "constraints": "N fits in string, D is single digit",
        "explanation": "",
        "tests": [
            {"input": "122321 2", "output": "3"},
            {"input": "1000000 0", "output": "6"},
            {"input": "7 3", "output": "0"}
        ]
    },
    {
        "id": "swap_case_string",
        "title": "Swap Case",
        "description": "Swap uppercase to lowercase and vice versa.",
        "description_full": "Given a string S, swap the case of each alphabetic character (lower→upper, upper→lower). Non-letters remain unchanged.",
        "input": "Single line string S",
        "output": "Case-swapped string",
        "example": "Input:\nHelloWorld\nOutput:\nhELLOwORLD",
        "constraints": "1 ≤ |S| ≤ 200",
        "explanation": "",
        "tests": [
            {"input": "Hello", "output": "hELLO"},
            {"input": "aBc123", "output": "AbC123"},
            {"input": "ABC", "output": "abc"}
        ]
    },
    {
        "id": "remove_vowels",
        "title": "Remove Vowels",
        "description": "Remove vowels from a string.",
        "description_full": "Given a string S, remove all vowels (a,e,i,o,u — both cases) and print the resulting string. If empty, print an empty line.",
        "input": "Single string S",
        "output": "String without vowels",
        "example": "Input:\napple\nOutput:\nppl",
        "constraints": "1 ≤ |S| ≤ 200",
        "explanation": "",
        "tests": [
            {"input": "apple", "output": "ppl"},
            {"input": "AEIOU", "output": ""},
            {"input": "Banana", "output": "Bnn"}
        ]
    },
    {
        "id": "sum_of_odds",
        "title": "Sum of Odd Numbers",
        "description": "Sum all odd integers from 1 to N.",
        "description_full": "Given positive integer N, compute the sum of all odd integers ≤ N.",
        "input": "Single integer N",
        "output": "Sum of odd numbers up to N",
        "example": "Input:\n6\nOutput:\n9",
        "constraints": "1 ≤ N ≤ 10^9",
        "explanation": "",
        "tests": [
            {"input": "6", "output": "9"},
            {"input": "1", "output": "1"},
            {"input": "10", "output": "25"}
        ]
    },
    {
        "id": "gcd_two_numbers",
        "title": "GCD of Two Numbers",
        "description": "Compute greatest common divisor of two numbers.",
        "description_full": "Given two positive integers A and B, print gcd(A, B).",
        "input": "Two integers A B",
        "output": "GCD value",
        "example": "Input:\n12 8\nOutput:\n4",
        "constraints": "1 ≤ A,B ≤ 10^12",
        "explanation": "",
        "tests": [
            {"input": "12 8", "output": "4"},
            {"input": "100 25", "output": "25"},
            {"input": "7 13", "output": "1"}
        ]
    },
    {
        "id": "is_power_of_two",
        "title": "Is Power of Two",
        "description": "Check if N is power of two.",
        "description_full": "Given a positive integer N, print YES if N is a power of two, otherwise NO.",
        "input": "Single integer N",
        "output": "YES or NO",
        "example": "Input:\n8\nOutput:\nYES",
        "constraints": "1 ≤ N ≤ 10^12",
        "explanation": "",
        "tests": [
            {"input": "8", "output": "YES"},
            {"input": "6", "output": "NO"},
            {"input": "1", "output": "YES"}
        ]
    },
    {
        "id": "count_divisible_by_k",
        "title": "Count Divisible By K",
        "description": "Count how many in array divisible by K.",
        "description_full": "Given N followed by N integers and integer K, print count of array elements divisible by K.",
        "input": "First line N, second line N integers, third line K",
        "output": "Count",
        "example": "Input:\n5\n2 3 4 5 6\n2\nOutput:\n3",
        "constraints": "1 ≤ N ≤ 10^5, elements fit 32-bit",
        "explanation": "",
        "tests": [
            {"input": "5\n2 3 4 5 6\n2", "output": "3"},
            {"input": "3\n1 3 5\n2", "output": "0"},
            {"input": "4\n10 20 30 40\n10", "output": "4"}
        ]
    },
    {
        "id": "sum_prefixes",
        "title": "Sum of Prefixes",
        "description": "Compute cumulative sums of array prefixes.",
        "description_full": "Given N and an array of N integers, print N numbers where i-th is sum of first i elements.",
        "input": "N then N integers",
        "output": "N prefix sums separated by space",
        "example": "Input:\n4\n1 2 3 4\nOutput:\n1 3 6 10",
        "constraints": "1 ≤ N ≤ 10^5",
        "explanation": "",
        "tests": [
            {"input": "4\n1 2 3 4\n", "output": "1 3 6 10"},
            {"input": "3\n5 -1 2\n", "output": "5 4 6"},
            {"input": "1\n7\n", "output": "7"}
        ]
    },
    {
        "id": "alternating_sum",
        "title": "Alternating Sum",
        "description": "Compute alternating sum of a sequence.",
        "description_full": "Given N and N integers a1..aN, compute a1 - a2 + a3 - a4 + ...",
        "input": "N then N integers",
        "output": "Alternating sum value",
        "example": "Input:\n4\n5 2 3 1\nOutput:\n5 -2 +3 -1 → 5",
        "constraints": "1 ≤ N ≤ 10^5",
        "explanation": "",
        "tests": [
            {"input": "4\n5 2 3 1\n", "output": "5"},
            {"input": "3\n1 1 1\n", "output": "1"},
            {"input": "2\n10 3\n", "output": "7"}
        ]
    },
    {
        "id": "binary_one_runs",
        "title": "Longest Run of Ones",
        "description": "Length of longest consecutive 1s in binary.",
        "description_full": "Given positive integer N, print the length of the longest consecutive run of 1s in its binary representation.",
        "input": "Single integer N",
        "output": "Length of longest run",
        "example": "Input:\n13\nOutput:\n2",
        "constraints": "1 ≤ N ≤ 10^9",
        "explanation": "",
        "tests": [
            {"input": "13", "output": "2"},
            {"input": "7", "output": "3"},
            {"input": "8", "output": "1"}
        ]
    },
    {
        "id": "count_trailing_zeros_small",
        "title": "Trailing Zeros in Factorial (small)",
        "description": "Count trailing zeros in N! (small N).",
        "description_full": "Given integer N (small), print number of trailing zeros in N! (factorial). N up to 1000 but tests small.",
        "input": "Single integer N",
        "output": "Count of trailing zeros",
        "example": "Input:\n5\nOutput:\n1",
        "constraints": "0 ≤ N ≤ 1000",
        "explanation": "",
        "tests": [
            {"input": "5", "output": "1"},
            {"input": "10", "output": "2"},
            {"input": "25", "output": "6"}
        ]
    }
],

"Easy": [
    {
        "id": "reverse_integer",
        "title": "Reverse Integer",
        "description": "Reverse digits of integer N.",
        "description_full": "Given an integer N, print the number formed by reversing its digits. Leading zeros should be removed.",
        "input": "Single integer N",
        "output": "Reversed integer",
        "example": "Input:\n1200\nOutput:\n21",
        "constraints": "0 ≤ N < 10^1000",
        "explanation": "",
        "tests": [
            {"input": "1200", "output": "21"},
            {"input": "987654", "output": "456789"},
            {"input": "1001", "output": "1001"}
        ]
    },
    {
        "id": "count_vowels",
        "title": "Count Vowels",
        "description": "Count vowels in string S.",
        "description_full": "Given a string S, count the number of vowels (a,e,i,o,u in both cases).",
        "input": "String S",
        "output": "Count of vowels",
        "example": "Input:\napple\nOutput:\n2",
        "constraints": "1 ≤ |S| ≤ 10^5",
        "explanation": "",
        "tests": [
            {"input": "apple", "output": "2"},
            {"input": "HELLO", "output": "2"},
            {"input": "xyz", "output": "0"}
        ]
    },
    {
        "id": "sum_array",
        "title": "Sum of Array",
        "description": "Compute sum of N integers.",
        "description_full": "Given integer N and N integers, compute their total sum.",
        "input": "N then N integers",
        "output": "Sum of array",
        "example": "Input:\n5\n1 2 3 4 5\nOutput:\n15",
        "constraints": "1 ≤ N ≤ 10^5",
        "explanation": "",
        "tests": [
            {"input": "5\n1 2 3 4 5", "output": "15"},
            {"input": "3\n10 10 10", "output": "30"},
            {"input": "1\n99", "output": "99"}
        ]
    },
    {
        "id": "linear_search",
        "title": "Linear Search",
        "description": "Search target X in array.",
        "description_full": "Given N, array A of N integers, and target X, print the index (0-based) of X if present, otherwise -1.",
        "input": "N\nA1 A2 .. AN\nX",
        "output": "Index or -1",
        "example": "Input:\n5\n1 3 5 7 9\n7\nOutput:\n3",
        "constraints": "1 ≤ N ≤ 10^5",
        "explanation": "",
        "tests": [
            {"input": "5\n1 3 5 7 9\n7", "output": "3"},
            {"input": "4\n2 4 6 8\n10", "output": "-1"},
            {"input": "3\n5 5 5\n5", "output": "0"}
        ]
    },
    {
        "id": "string_palindrome",
        "title": "Check Palindrome",
        "description": "Check if string is palindrome.",
        "description_full": "Given string S, print YES if it reads the same backward, otherwise NO.",
        "input": "String S",
        "output": "YES or NO",
        "example": "Input:\nlevel\nOutput:\nYES",
        "constraints": "1 ≤ |S| ≤ 10^5",
        "explanation": "",
        "tests": [
            {"input": "level", "output": "YES"},
            {"input": "hello", "output": "NO"},
            {"input": "a", "output": "YES"}
        ]
    },
    {
        "id": "count_words",
        "title": "Count Words",
        "description": "Count words in a sentence.",
        "description_full": "Given a sentence S, count how many words it contains. Words are separated by spaces.",
        "input": "String S",
        "output": "Word count",
        "example": "Input:\nI love coding\nOutput:\n3",
        "constraints": "1 ≤ |S| ≤ 10^5",
        "explanation": "",
        "tests": [
            {"input": "I love coding", "output": "3"},
            {"input": "Hello World", "output": "2"},
            {"input": "one", "output": "1"}
        ]
    },
    {
        "id": "second_largest",
        "title": "Second Largest Element",
        "description": "Find second largest in array.",
        "description_full": "Given N and N integers, print the second largest distinct integer. If no second largest exists, print -1.",
        "input": "N then N integers",
        "output": "Second largest",
        "example": "Input:\n5\n1 2 3 4 5\nOutput:\n4",
        "constraints": "1 ≤ N ≤ 10^5",
        "explanation": "",
        "tests": [
            {"input": "5\n1 2 3 4 5", "output": "4"},
            {"input": "3\n10 10 10", "output": "-1"},
            {"input": "4\n5 1 5 3", "output": "3"}
        ]
    },
    {
        "id": "merge_strings",
        "title": "Merge Two Strings",
        "description": "Interleave characters of two strings.",
        "description_full": "Given strings A and B, print a new string formed by alternating characters from each (A1,B1,A2,B2,...). If one ends, append rest of the other.",
        "input": "Two strings A and B",
        "output": "Merged string",
        "example": "Input:\nab cd\nOutput:\nacbd",
        "constraints": "1 ≤ |A|,|B| ≤ 200",
        "explanation": "",
        "tests": [
            {"input": "ab cd", "output": "acbd"},
            {"input": "a xyz", "output": "axyz"},
            {"input": "hello hi", "output": "h e ll il o"}
        ]
    },
    {
        "id": "factorial_small",
        "title": "Factorial (Small)",
        "description": "Compute factorial for small N.",
        "description_full": "Given N, print N!. N will be small (≤15) so factorial fits in 64-bit.",
        "input": "Single integer N",
        "output": "N!",
        "example": "Input:\n5\nOutput:\n120",
        "constraints": "0 ≤ N ≤ 15",
        "explanation": "",
        "tests": [
            {"input": "5", "output": "120"},
            {"input": "0", "output": "1"},
            {"input": "7", "output": "5040"}
        ]
    },
    {
        "id": "rotate_array_left",
        "title": "Left Rotate Array",
        "description": "Rotate array left by K.",
        "description_full": "Given N, array A, and integer K, rotate array left by K positions.",
        "input": "N\nA1..AN\nK",
        "output": "Rotated array",
        "example": "Input:\n5\n1 2 3 4 5\n2\nOutput:\n3 4 5 1 2",
        "constraints": "1 ≤ N ≤ 10^5",
        "explanation": "",
        "tests": [
            {"input": "5\n1 2 3 4 5\n2", "output": "3 4 5 1 2"},
            {"input": "4\n10 20 30 40\n1", "output": "20 30 40 10"},
            {"input": "3\n1 2 3\n3", "output": "1 2 3"}
        ]
    },
    {
        "id": "string_compress_basic",
        "title": "Basic String Compression",
        "description": "Compress consecutive characters.",
        "description_full": "Given string S, compress it as cX where c is the character and X is consecutive count.",
        "input": "String S",
        "output": "Compressed string",
        "example": "Input:\naaaabbc\nOutput:\na4b2c1",
        "constraints": "1 ≤ |S| ≤ 200",
        "explanation": "",
        "tests": [
            {"input": "aaaabbc", "output": "a4b2c1"},
            {"input": "xy", "output": "x1y1"},
            {"input": "zzzz", "output": "z4"}
        ]
    },
    {
        "id": "sum_of_pairs",
        "title": "Sum of Adjacent Pairs",
        "description": "Print sum of every adjacent pair.",
        "description_full": "Given N and N integers, print N-1 integers where i-th is Ai + A(i+1).",
        "input": "N then N integers",
        "output": "N-1 integers",
        "example": "Input:\n4\n1 2 3 4\nOutput:\n3 5 7",
        "constraints": "1 ≤ N ≤ 10^5",
        "explanation": "",
        "tests": [
            {"input": "4\n1 2 3 4", "output": "3 5 7"},
            {"input": "3\n5 5 5", "output": "10 10"},
            {"input": "2\n10 1", "output": "11"}
        ]
    },
    {
        "id": "max_digit",
        "title": "Maximum Digit",
        "description": "Find largest digit in N.",
        "description_full": "Given non-negative integer N, print its largest digit.",
        "input": "Single integer N",
        "output": "Largest digit",
        "example": "Input:\n5381\nOutput:\n8",
        "constraints": "0 ≤ N ≤ 10^1000",
        "explanation": "",
        "tests": [
            {"input": "5381", "output": "8"},
            {"input": "1000", "output": "1"},
            {"input": "999999", "output": "9"}
        ]
    },
    {
        "id": "count_lowercase",
        "title": "Count Lowercase Letters",
        "description": "Count lowercase letters in S.",
        "description_full": "Given string S, print how many characters are lowercase English letters.",
        "input": "String S",
        "output": "Lowercase count",
        "example": "Input:\nHeLLo\nOutput:\n2",
        "constraints": "1 ≤ |S| ≤ 10^5",
        "explanation": "",
        "tests": [
            {"input": "HeLLo", "output": "2"},
            {"input": "abc", "output": "3"},
            {"input": "XYZ", "output": "0"}
        ]
    },
    {
        "id": "multiply_every_third",
        "title": "Multiply Every Third Element",
        "description": "Multiply every third element and print product.",
        "description_full": "Given N and an array A, multiply A3 * A6 * A9 ...; if none exist, print 1.",
        "input": "N and N integers",
        "output": "Product",
        "example": "Input:\n6\n1 2 3 4 5 6\nOutput:\n18",
        "constraints": "1 ≤ N ≤ 10^5",
        "explanation": "",
        "tests": [
            {"input": "6\n1 2 3 4 5 6", "output": "18"},
            {"input": "2\n5 6", "output": "1"},
            {"input": "3\n7 2 4", "output": "4"}
        ]
    },
    {
        "id": "string_reverse_words",
        "title": "Reverse Words in Sentence",
        "description": "Reverse the order of words.",
        "description_full": "Given a sentence S with words separated by spaces, print words in reverse order.",
        "input": "Sentence S",
        "output": "Reversed word order",
        "example": "Input:\nI love coding\nOutput:\ncoding love I",
        "constraints": "1 ≤ |S| ≤ 10^5",
        "explanation": "",
        "tests": [
            {"input": "I love coding", "output": "coding love I"},
            {"input": "hello world", "output": "world hello"},
            {"input": "one", "output": "one"}
        ]
    },
    {
        "id": "sum_diagonal_matrix",
        "title": "Matrix Diagonal Sum",
        "description": "Sum primary diagonal of NxN matrix.",
        "description_full": "Given integer N and an NxN matrix, print the sum of its primary diagonal.",
        "input": "N then NxN matrix",
        "output": "Diagonal sum",
        "example": "Input:\n2\n1 2\n3 4\nOutput:\n5",
        "constraints": "1 ≤ N ≤ 300",
        "explanation": "",
        "tests": [
            {"input": "2\n1 2\n3 4", "output": "5"},
            {"input": "3\n1 0 0\n0 1 0\n0 0 1", "output": "3"},
            {"input": "1\n9", "output": "9"}
        ]
    },
    {
        "id": "max_frequency_char",
        "title": "Max Frequency Character",
        "description": "Find most frequent character in S.",
        "description_full": "Given string S, print the character that appears most frequently. If multiple, print the lexicographically smallest.",
        "input": "String S",
        "output": "Single character",
        "example": "Input:\naabccc\nOutput:\nc",
        "constraints": "1 ≤ |S| ≤ 10^5",
        "explanation": "",
        "tests": [
            {"input": "aabccc", "output": "c"},
            {"input": "bbbaa", "output": "b"},
            {"input": "xyz", "output": "x"}
        ]
    },
    {
        "id": "sum_positions",
        "title": "Sum of Positions of Character",
        "description": "Sum positions of a character in S.",
        "description_full": "Given string S and character C, sum all positions (1-indexed) where C occurs.",
        "input": "S then C",
        "output": "Sum of positions",
        "example": "Input:\nbanana\na\nOutput:\n12",
        "constraints": "1 ≤ |S| ≤ 10^5",
        "explanation": "",
        "tests": [
            {"input": "banana\na", "output": "12"},
            {"input": "hello\no", "output": "5"},
            {"input": "abc\nd", "output": "0"}
        ]
    },
    {
        "id": "filter_greater",
        "title": "Filter Elements Greater Than X",
        "description": "Print elements greater than X.",
        "description_full": "Given N, array A, and integer X, print all elements greater than X in order. If none, print -1.",
        "input": "N\nA1..AN\nX",
        "output": "Filtered list",
        "example": "Input:\n5\n1 3 5 7 9\n4\nOutput:\n5 7 9",
        "constraints": "1 ≤ N ≤ 10^5",
        "explanation": "",
        "tests": [
            {"input": "5\n1 3 5 7 9\n4", "output": "5 7 9"},
            {"input": "3\n1 2 3\n5", "output": "-1"},
            {"input": "4\n10 20 5 15\n15", "output": "20"}
        ]
    }
],
"Medium": [

    {
        "id": "pair_with_sum",
        "title": "Pair With Given Sum",
        "description": "Check if any two numbers sum to X.",
        "description_full": "Given N integers and a number X, print YES if any two numbers in the list sum to X, otherwise print NO.",
        "input": "N\nA1 A2 .. AN\nX",
        "output": "YES or NO",
        "example": "Input:\n5\n1 4 2 7 5\n6\nOutput:\nYES",
        "constraints": "1 ≤ N ≤ 10^5",
        "explanation": "",
        "tests": [
            {"input": "5\n1 4 2 7 5\n6", "output": "YES"},
            {"input": "4\n10 20 30 40\n100", "output": "NO"},
            {"input": "3\n1 1 1\n2", "output": "YES"}
        ]
    },

    {
        "id": "longest_word_length",
        "title": "Longest Word Length",
        "description": "Find the length of the longest word in a sentence.",
        "description_full": "Given a sentence S, print the length of its longest word.",
        "input": "Sentence S",
        "output": "Integer length",
        "example": "Input:\nI love programming\nOutput:\n11",
        "constraints": "1 ≤ |S| ≤ 200000",
        "explanation": "",
        "tests": [
            {"input": "I love programming", "output": "11"},
            {"input": "hello world", "output": "5"},
            {"input": "one", "output": "3"}
        ]
    },

    {
        "id": "distinct_elements",
        "title": "Count Distinct Elements",
        "description": "Count number of unique elements.",
        "description_full": "Given N and an array A, print the number of distinct integers in A.",
        "input": "N then N integers",
        "output": "Count",
        "example": "Input:\n6\n1 2 2 3 3 3\nOutput:\n3",
        "constraints": "1 ≤ N ≤ 200000",
        "explanation": "",
        "tests": [
            {"input": "6\n1 2 2 3 3 3", "output": "3"},
            {"input": "4\n5 5 5 5", "output": "1"},
            {"input": "5\n10 20 30 40 50", "output": "5"}
        ]
    },

    {
        "id": "prefix_equal_subarrays",
        "title": "Count Equal Prefix Subarrays",
        "description": "Count subarrays where prefix sum *2 = total sum.",
        "description_full": "Given N and array A, count indices i such that sum(A1..Ai) * 2 = sum(A1..AN).",
        "input": "N then N integers",
        "output": "Count",
        "example": "Input:\n4\n1 2 3 3\nOutput:\n1",
        "constraints": "1 ≤ N ≤ 2e5",
        "explanation": "",
        "tests": [
            {"input": "4\n1 2 3 3", "output": "1"},
            {"input": "3\n1 1 1", "output": "0"},
            {"input": "5\n2 2 2 2 2", "output": "0"}
        ]
    },

    {
        "id": "largest_subarray_sum",
        "title": "Maximum Subarray Sum",
        "description": "Find maximum sum of a contiguous subarray.",
        "description_full": "Given N and an array A, compute the maximum sum of any contiguous subarray (Kadane’s algorithm).",
        "input": "N then N integers",
        "output": "Maximum subarray sum",
        "example": "Input:\n5\n-1 2 -3 4 5\nOutput:\n9",
        "constraints": "1 ≤ N ≤ 200000",
        "explanation": "",
        "tests": [
            {"input": "5\n-1 2 -3 4 5", "output": "9"},
            {"input": "3\n-5 -1 -3", "output": "-1"},
            {"input": "4\n1 2 3 4", "output": "10"}
        ]
    },

    {
        "id": "balanced_parentheses",
        "title": "Balanced Parentheses",
        "description": "Check if parentheses string is balanced.",
        "description_full": "Given string S containing only '(' and ')', print YES if parentheses are balanced, otherwise NO.",
        "input": "String S",
        "output": "YES or NO",
        "example": "Input:\n(()())\nOutput:\nYES",
        "constraints": "1 ≤ |S| ≤ 200000",
        "explanation": "",
        "tests": [
            {"input": "()()", "output": "YES"},
            {"input": "(()", "output": "NO"},
            {"input": "())(()", "output": "NO"}
        ]
    },

    {
        "id": "sum_of_subarrays",
        "title": "Sum of All Subarrays",
        "description": "Compute sum of all possible subarrays.",
        "description_full": "Given N and array A, compute the sum of all subarray sums.",
        "input": "N then N integers",
        "output": "Total sum",
        "example": "Input:\n3\n1 2 3\nOutput:\n20",
        "constraints": "1 ≤ N ≤ 200000",
        "explanation": "",
        "tests": [
            {"input": "3\n1 2 3", "output": "20"},
            {"input": "1\n5", "output": "5"},
            {"input": "2\n1 4", "output": "11"}
        ]
    },

    {
        "id": "first_non_repeating_char",
        "title": "First Non-Repeating Character",
        "description": "Find first character with frequency 1.",
        "description_full": "Given string S, print the first character that appears exactly once. If none, print -1.",
        "input": "String S",
        "output": "Character or -1",
        "example": "Input:\nabacbd\nOutput:\nc",
        "constraints": "1 ≤ |S| ≤ 200000",
        "explanation": "",
        "tests": [
            {"input": "abacbd", "output": "c"},
            {"input": "aaaa", "output": "-1"},
            {"input": "abc", "output": "a"}
        ]
    },

    {
        "id": "kth_largest",
        "title": "Kth Largest Element",
        "description": "Find the Kth largest element in array.",
        "description_full": "Given N, array A, and integer K, print the K-th largest distinct element. If not possible, print -1.",
        "input": "N\nA1..AN\nK",
        "output": "Kth largest or -1",
        "example": "Input:\n5\n3 1 5 5 2\n2\nOutput:\n3",
        "constraints": "1 ≤ N ≤ 200000",
        "explanation": "",
        "tests": [
            {"input": "5\n3 1 5 5 2\n2", "output": "3"},
            {"input": "3\n10 10 10\n1", "output": "10"},
            {"input": "4\n1 2 3 4\n5", "output": "-1"}
        ]
    },

    {
        "id": "matrix_rotate_90",
        "title": "Rotate Matrix 90° Clockwise",
        "description": "Rotate an NxN matrix 90° clockwise.",
        "description_full": "Given N and an NxN matrix, output the matrix rotated 90 degrees clockwise.",
        "input": "N then NxN integers",
        "output": "Rotated matrix",
        "example": "Input:\n2\n1 2\n3 4\nOutput:\n3 1\n4 2",
        "constraints": "1 ≤ N ≤ 200",
        "explanation": "",
        "tests": [
            {"input": "2\n1 2\n3 4", "output": "3 1\n4 2"},
            {"input": "1\n9", "output": "9"},
            {"input": "3\n1 2 3\n4 5 6\n7 8 9", "output": "7 4 1\n8 5 2\n9 6 3"}
        ]
    },

    {
        "id": "remove_duplicates_sorted",
        "title": "Remove Duplicates From Sorted Array",
        "description": "Remove duplicates but keep order.",
        "description_full": "Given sorted array A of N integers, print the array after removing duplicates (keep first occurrences).",
        "input": "N then sorted array",
        "output": "Array without duplicates",
        "example": "Input:\n6\n1 1 2 2 3 3\nOutput:\n1 2 3",
        "constraints": "1 ≤ N ≤ 200000",
        "explanation": "",
        "tests": [
            {"input": "6\n1 1 2 2 3 3", "output": "1 2 3"},
            {"input": "3\n5 5 5", "output": "5"},
            {"input": "4\n1 2 3 4", "output": "1 2 3 4"}
        ]
    },

    {
        "id": "longest_increasing_subarray",
        "title": "Longest Increasing Subarray",
        "description": "Find longest strictly increasing contiguous segment.",
        "description_full": "Given N and array A, find the length of the longest contiguous strictly increasing subarray.",
        "input": "N then array",
        "output": "Length",
        "example": "Input:\n5\n1 2 2 3 4\nOutput:\n3",
        "constraints": "1 ≤ N ≤ 200000",
        "explanation": "",
        "tests": [
            {"input": "5\n1 2 2 3 4", "output": "3"},
            {"input": "4\n4 3 2 1", "output": "1"},
            {"input": "6\n1 2 3 4 5 6", "output": "6"}
        ]
    },

    {
        "id": "frequency_sort",
        "title": "Frequency Sort Characters",
        "description": "Sort characters by decreasing frequency.",
        "description_full": "Given string S, sort characters by decreasing frequency. For ties, sort lexicographically.",
        "input": "String S",
        "output": "Sorted string",
        "example": "Input:\naabccc\nOutput:\ncccaa",
        "constraints": "1 ≤ |S| ≤ 200000",
        "explanation": "",
        "tests": [
            {"input": "aabccc", "output": "cccaa"},
            {"input": "zzzxy", "output": "zzzxy"},
            {"input": "abc", "output": "abc"}
        ]
    },

    {
        "id": "max_consecutive_sum",
        "title": "Max Sum of K Consecutive Elements",
        "description": "Find maximum sum of any K consecutive elements.",
        "description_full": "Given N, array A, and integer K, compute the maximum sum of any K-length subarray.",
        "input": "N\nA1..AN\nK",
        "output": "Maximum sum",
        "example": "Input:\n5\n1 4 2 10 2\n2\nOutput:\n12",
        "constraints": "1 ≤ N ≤ 200000",
        "explanation": "",
        "tests": [
            {"input": "5\n1 4 2 10 2\n2", "output": "12"},
            {"input": "3\n1 2 3\n3", "output": "6"},
            {"input": "4\n10 1 1 1\n1", "output": "10"}
        ]
    },

    {
        "id": "count_inversions",
        "title": "Count Inversions",
        "description": "Count number of inversions in array.",
        "description_full": "Given N and array A, count number of pairs (i < j) such that A[i] > A[j].",
        "input": "N then N integers",
        "output": "Inversion count",
        "example": "Input:\n3\n3 1 2\nOutput:\n2",
        "constraints": "1 ≤ N ≤ 200000",
        "explanation": "",
        "tests": [
            {"input": "3\n3 1 2", "output": "2"},
            {"input": "3\n1 2 3", "output": "0"},
            {"input": "4\n4 3 2 1", "output": "6"}
        ]
    },

    {
        "id": "row_with_max_ones",
        "title": "Row with Maximum Ones",
        "description": "Find row with max number of 1s in a binary matrix.",
        "description_full": "Given N and an NxN binary matrix, print the index (0-based) of the row with the maximum number of 1s. If tie, choose smallest index.",
        "input": "N then NxN matrix",
        "output": "Row index",
        "example": "Input:\n3\n0 1 1\n1 1 0\n0 0 0\nOutput:\n1",
        "constraints": "1 ≤ N ≤ 500",
        "explanation": "",
        "tests": [
            {"input": "3\n0 1 1\n1 1 0\n0 0 0", "output": "1"},
            {"input": "2\n1 1\n1 1", "output": "0"},
            {"input": "2\n0 0\n1 0", "output": "1"}
        ]
    }
]

}
