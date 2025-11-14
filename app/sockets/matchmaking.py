# app/sockets/matchmaking.py
# ======================================================
# Slashcoder Matchmaking — OLD system (clean + both-submit rule)
# - Emits room, problem (HackerRank-style fields), timeLimit, testsCount, startTime
# - "run_code" event for custom test runs (Judge0)
# - "submit_code" waits for BOTH players before deciding result (2s calculating)
# - Firestore XP + W/L + matches logs
# ======================================================

import random
import time
import datetime
import httpx
import socketio
import firebase_admin
from firebase_admin import credentials, firestore


# ---------- SINGLE sio instance ----------
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",
    allow_credentials=True
)


# ---------- FIRESTORE INIT (Railway Safe) ----------
import os, json


FIREBASE_KEY = os.getenv("FIREBASE_KEY")
if not FIREBASE_KEY:
    raise Exception("Missing FIREBASE_KEY in Railway variables.")

# Convert JSON string → dict
service_account_info = json.loads(FIREBASE_KEY)

# Initialize Firebase Admin safely
if not firebase_admin._apps:
    cred = credentials.Certificate(service_account_info)
    firebase_admin.initialize_app(cred)

db = firestore.client()



# ---------- CONFIG ----------
JUDGE0_URL = "https://ce.judge0.com/submissions?base64_encoded=false&wait=true"
LANG_TO_ID = {"python": 71, "cpp": 54, "java": 62, "javascript": 63}

# XP awards (you can tune)
WIN_XP = 25
LOSS_XP = 10

# ---------- STATE ----------
waiting_player = None   # {"sid","uid","name","xp"}
matches = {}            # room -> match dict

# ===============================
# --- PASTE PROBLEMS & gen_tests_for_problem HERE ---
# ===============================
#
# IMPORTANT: Paste your original PROBLEMS dictionary (Very Easy / Easy / Medium)
# and your full gen_tests_for_problem(pid, title) function here.
#
# The generator must return a list of tests:
#   [{"input": "...", "output": "..."}, ...]  (3 hidden tests usually)
#
# Example minimal placeholder (will be overwritten by your pasted generator):
#
# ======================================================
# FULL PROBLEMS (40 QUESTIONS) + TEST GENERATOR
# Compatible with HackerRank-style UI (description_full, input, output, example, explanation)
# ======================================================

PROBLEMS = {
    "Very Easy": [
        {
            "id": "ve1",
            "title": "Print Hello World",
            "description": "Print the phrase 'Hello World'.",
            "description_full": "Your task is to output the exact phrase Hello World.\nThis is the simplest possible programming task.",
            "input": "-",
            "output": "Hello World",
            "constraints": "-",
            "example": "Hello World",
            "explanation": "Simply print the phrase."
        },
        {
            "id": "ve2",
            "title": "Add Two Numbers",
            "description": "Add two integers.",
            "description_full": "You will be given two integers on one line. Print their sum.",
            "input": "a b",
            "output": "a+b",
            "constraints": "-100 ≤ a,b ≤ 100",
            "example": "2 3\nOutput:\n5",
            "explanation": "2+3 = 5."
        },
        {
            "id": "ve3",
            "title": "Maximum of Two",
            "description": "Print the maximum of two integers.",
            "description_full": "Given two integers, output the larger one.",
            "input": "a b",
            "output": "max(a,b)",
            "constraints": "-100 ≤ a,b ≤ 100",
            "example": "5 9\nOutput:\n9",
            "explanation": "9 is larger than 5."
        },
        {
            "id": "ve4",
            "title": "Square of a Number",
            "description": "Print n squared.",
            "description_full": "Given an integer n, print n multiplied by itself.",
            "input": "n",
            "output": "n^2",
            "constraints": "0 ≤ n ≤ 50",
            "example": "6\nOutput:\n36",
            "explanation": "6×6 = 36"
        },
        {
            "id": "ve5",
            "title": "Absolute Value",
            "description": "Print absolute value of n.",
            "description_full": "Given an integer n, print its absolute (non-negative) value.",
            "input": "n",
            "output": "|n|",
            "constraints": "-100 ≤ n ≤ 100",
            "example": "-7\nOutput:\n7",
            "explanation": "Absolute of -7 is 7."
        },
        {
            "id": "ve6",
            "title": "Even or Odd",
            "description": "Check if an integer is even or odd.",
            "description_full": "Given an integer n, print EVEN if it is divisible by 2, else print ODD.",
            "input": "n",
            "output": "EVEN or ODD",
            "constraints": "-1000 ≤ n ≤ 1000",
            "example": "4\nOutput:\nEVEN",
            "explanation": "4 % 2 == 0."
        },
        {
            "id": "ve7",
            "title": "Multiply Two Numbers",
            "description": "Print product of a and b.",
            "description_full": "Given two integers a and b, print their multiplication result.",
            "input": "a b",
            "output": "a*b",
            "constraints": "-20 ≤ a,b ≤ 20",
            "example": "4 6\nOutput:\n24",
            "explanation": "4×6 = 24."
        },
        {
            "id": "ve8",
            "title": "String Length",
            "description": "Print length of string.",
            "description_full": "Given a string s, print the number of characters in it.",
            "input": "s",
            "output": "len(s)",
            "constraints": "1 ≤ |s| ≤ 50",
            "example": "hello\nOutput:\n5",
            "explanation": "'hello' contains 5 characters."
        },
        {
            "id": "ve9",
            "title": "Reverse String",
            "description": "Print reversed string.",
            "description_full": "Given a string s, print the reverse of s.",
            "input": "s",
            "output": "reverse(s)",
            "constraints": "1 ≤ |s| ≤ 20",
            "example": "abc\nOutput:\ncba",
            "explanation": "Reversed."
        },
        {
            "id": "ve10",
            "title": "Greet User",
            "description": "Print 'Hello <name>'.",
            "description_full": "Given a name, greet the user by printing Hello <name>.",
            "input": "name",
            "output": "Hello <name>",
            "constraints": "Name is a single word",
            "example": "Alice\nOutput:\nHello Alice",
            "explanation": "Prefix 'Hello ' before name."
        }
    ],

    "Easy": [
        {
            "id": "e1",
            "title": "Find Maximum Number",
            "description": "Find the maximum of N integers.",
            "description_full": "You will be given an integer N, followed by N integers. Print the largest integer.",
            "input": "N\narray",
            "output": "max(array)",
            "constraints": "1 ≤ N ≤ 100",
            "example": "5\n1 9 3 7 2\nOutput:\n9",
            "explanation": "9 is the largest number."
        },
        {
            "id": "e2",
            "title": "Find Minimum Number",
            "description": "Find the minimum of N integers.",
            "description_full": "Print the smallest integer in the given list.",
            "input": "N\narray",
            "output": "min(array)",
            "constraints": "1 ≤ N ≤ 100",
            "example": "4\n5 2 8 1\nOutput:\n1",
            "explanation": "1 is minimum."
        },
        {
            "id": "e3",
            "title": "Sum of N Numbers",
            "description": "Print sum of array elements.",
            "description_full": "Given N and an array of N integers, print their sum.",
            "input": "N\narray",
            "output": "sum(array)",
            "example": "3\n5 5 5\nOutput:\n15",
            "explanation": "Sum = 15."
        },
        {
            "id": "e4",
            "title": "Count Vowels",
            "description": "Count vowels in the string.",
            "description_full": "Given a string s, count how many characters are vowels (a,e,i,o,u).",
            "input": "s",
            "output": "count of vowels",
            "example": "apple\nOutput:\n2",
            "explanation": "a,e,i,o,u considered."
        },
        {
            "id": "e5",
            "title": "Palindrome Check",
            "description": "Check if string is palindrome.",
            "description_full": "Given a string s, print YES if s equals its reverse, else NO.",
            "input": "s",
            "output": "YES or NO",
            "example": "madam\nOutput:\nYES",
            "explanation": "madam reversed is madam."
        },
        {
            "id": "e6",
            "title": "Digit Count",
            "description": "Count number of digits.",
            "description_full": "Given an integer n, print the number of digits in it.",
            "input": "n",
            "output": "digit count",
            "example": "1234\nOutput:\n4",
            "explanation": "4 digits."
        },
        {
            "id": "e7",
            "title": "Product of Digits",
            "description": "Multiply digits of n.",
            "description_full": "Given a number n, multiply all its digits and print result.",
            "input": "n",
            "output": "product",
            "example": "234\nOutput:\n24",
            "explanation": "2*3*4 = 24."
        },
        {
            "id": "e8",
            "title": "Factorial",
            "description": "Find factorial of n.",
            "description_full": "Given n (n ≤ 12), compute n!.",
            "input": "n",
            "output": "n!",
            "example": "5\nOutput:\n120",
            "explanation": "5! = 120."
        },
        {
            "id": "e9",
            "title": "Nth Fibonacci",
            "description": "Print Nth Fibonacci number.",
            "description_full": "Given n (1-indexed), print the nth Fibonacci number.",
            "input": "n",
            "output": "F(n)",
            "example": "6\nOutput:\n8",
            "explanation": "1,1,2,3,5,8..."
        },
        {
            "id": "e10",
            "title": "Sort Numbers",
            "description": "Sort N integers in ascending order.",
            "description_full": "Print the sorted version of the given integer array.",
            "input": "N\narray",
            "output": "sorted array",
            "example": "4\n9 1 5 3\nOutput:\n1 3 5 9",
            "explanation": "Ascending order."
        },
        {
            "id": "e11",
            "title": "Count Words",
            "description": "Count words in sentence.",
            "description_full": "Given a sentence, count how many words exist (split by spaces).",
            "input": "sentence",
            "output": "number of words",
            "example": "I love coding\nOutput:\n3",
            "explanation": "3 words."
        },
        {
            "id": "e12",
            "title": "Sum of Even Numbers",
            "description": "Sum all even numbers up to N.",
            "description_full": "Given N, calculate sum of all even numbers between 1 and N (inclusive).",
            "input": "N",
            "output": "sum",
            "example": "10\nOutput:\n30",
            "explanation": "2+4+6+8+10 = 30."
        },
        {
            "id": "e13",
            "title": "Unique Characters",
            "description": "Count unique characters.",
            "description_full": "Given a string s, count how many unique characters appear in s.",
            "input": "s",
            "output": "count",
            "example": "abca\nOutput:\n3",
            "explanation": "a,b,c"
        },
        {
            "id": "e14",
            "title": "Prime Check",
            "description": "Check if number is prime.",
            "description_full": "Given an integer n, print YES if prime else NO.",
            "input": "n",
            "output": "YES or NO",
            "example": "7\nOutput:\nYES",
            "explanation": "7 is prime."
        },
        {
            "id": "e15",
            "title": "Second Largest",
            "description": "Find second largest number.",
            "description_full": "Given N integers, print the second largest value.",
            "input": "N\narray",
            "output": "second largest",
            "example": "5\n1 9 3 7 5\nOutput:\n7",
            "explanation": "Sorted: 1,3,5,7,9"
        }
    ],

    "Medium": [
        {
            "id": "m1",
            "title": "Matrix Sum",
            "description": "Sum all elements of an NxN matrix.",
            "description_full": "You will be given N followed by an NxN matrix. Print the sum of all elements.",
            "input": "N\nmatrix",
            "output": "sum",
            "constraints": "1 ≤ N ≤ 10",
            "example": "2\n1 2\n3 4\nOutput:\n10",
            "explanation": "1+2+3+4 = 10."
        },
        {
            "id": "m2",
            "title": "GCD of Two Numbers",
            "description": "Compute the greatest common divisor.",
            "description_full": "Given two integers a and b, compute gcd(a,b).",
            "input": "a b",
            "output": "gcd",
            "example": "12 18\nOutput:\n6",
            "explanation": "GCD(12,18) = 6."
        },
        {
            "id": "m3",
            "title": "LCM of Two Numbers",
            "description": "Compute the least common multiple.",
            "description_full": "Given two integers a and b, compute the LCM.",
            "input": "a b",
            "output": "lcm",
            "example": "4 6\nOutput:\n12",
            "explanation": "LCM = a*b/gcd."
        },
        {
            "id": "m4",
            "title": "Rotate Array",
            "description": "Rotate array right by k.",
            "description_full": "Given N, K, and array A, rotate A to the right by K positions.",
            "input": "N K\narray",
            "output": "rotated array",
            "example": "5 2\n1 2 3 4 5\nOutput:\n4 5 1 2 3",
            "explanation": "Last 2 come first."
        },
        {
            "id": "m5",
            "title": "Rearrange String",
            "description": "Sort characters of string.",
            "description_full": "Given string s, print its characters in sorted order.",
            "input": "s",
            "output": "sorted string",
            "example": "dbca\nOutput:\nabcd",
            "explanation": "Sorted lexicographically."
        },
        {
            "id": "m6",
            "title": "Count Primes ≤ N",
            "description": "Count primes up to N.",
            "description_full": "Given N, count how many prime numbers exist from 1 to N.",
            "input": "N",
            "output": "count",
            "example": "10\nOutput:\n4",
            "explanation": "Primes: 2,3,5,7"
        },
        {
            "id": "m7",
            "title": "Binary Search",
            "description": "Return index of target or -1.",
            "description_full": "Given a sorted array and target, print index if present else -1.",
            "input": "N\narray\ntarget",
            "output": "index",
            "example": "5\n1 2 3 7 9\n7\nOutput:\n3",
            "explanation": "Index 3."
        },
        {
            "id": "m8",
            "title": "Frequency Count",
            "description": "Most frequent element in array.",
            "description_full": "Given N and array A, find the element appearing most frequently. If tie, return smallest.",
            "input": "N\narray",
            "output": "value",
            "example": "5\n1 2 2 3 3\nOutput:\n2",
            "explanation": "2 & 3 appear twice → choose smaller."
        },
        {
            "id": "m9",
            "title": "Longest Word",
            "description": "Print longest word in sentence.",
            "description_full": "Given a sentence, print the longest word.",
            "input": "sentence",
            "output": "longest word",
            "example": "I love coding\nOutput:\ncoding",
            "explanation": "coding is longest."
        },
        {
            "id": "m10",
            "title": "Intersection of Arrays",
            "description": "Find common elements.",
            "description_full": "Given two arrays, print sorted intersection (common elements).",
            "input": "N M\narray1\narray2",
            "output": "intersected array",
            "example": "3 3\n1 2 3\n2 3 4\nOutput:\n2 3",
            "explanation": "2,3 are common."
        },
        {
            "id": "m11",
            "title": "Sum of Digits (Recursion)",
            "description": "Recursively sum digits.",
            "description_full": "Given n, calculate sum of its digits (n may be large).",
            "input": "n",
            "output": "digit sum",
            "example": "123\nOutput:\n6",
            "explanation": "1+2+3 = 6"
        },
        {
            "id": "m12",
            "title": "Balanced Parentheses",
            "description": "Check if parentheses balanced.",
            "description_full": "Given a string containing (), [], {}, print YES if it is balanced.",
            "input": "s",
            "output": "YES or NO",
            "example": "{[()]}\nOutput:\nYES",
            "explanation": "Balanced."
        },
        {
            "id": "m13",
            "title": "Merge Sort Output",
            "description": "Sort array using merge sort.",
            "description_full": "Given N and array A, print sorted version (you may use built-in sort).",
            "input": "N\narray",
            "output": "sorted array",
            "example": "4\n4 2 7 1\nOutput:\n1 2 4 7",
            "explanation": "Sorted result."
        },
        {
            "id": "m14",
            "title": "Missing Number",
            "description": "Find missing number 1..n.",
            "description_full": "Given N-1 numbers of range 1..N, find the missing number.",
            "input": "N-1\narray",
            "output": "missing number",
            "example": "4\n1 4 3\nOutput:\n2",
            "explanation": "2 missing."
        },
        {
            "id": "m15",
            "title": "Kadane Max Subarray",
            "description": "Find maximum subarray sum.",
            "description_full": "Given N and array A, compute the largest possible sum of any contiguous subarray (Kadane's algorithm).",
            "input": "N\narray",
            "output": "max sum",
            "example": "5\n-2 1 -3 4 -1\nOutput:\n4",
            "explanation": "[4] is best."
        }
    ]
}

# ======================================================
# TEST CASE GENERATOR (3 hidden tests per problem)
# ======================================================

def gen_tests_for_problem(pid: str, title: str):
    tests = []

    # ---- VERY EASY ----
    if pid == "ve1":  # Hello World
        tests = [{"input": "", "output": "Hello World"} for _ in range(3)]

    elif pid == "ve2":  # Add two numbers
        for _ in range(3):
            a = random.randint(-50, 50)
            b = random.randint(-50, 50)
            tests.append({"input": f"{a} {b}", "output": str(a+b)})

    elif pid == "ve3":  # Max of two
        for _ in range(3):
            a = random.randint(-100,100)
            b = random.randint(-100,100)
            tests.append({"input": f"{a} {b}", "output": str(max(a,b))})

    elif pid == "ve4":
        for _ in range(3):
            n = random.randint(0,50)
            tests.append({"input": f"{n}", "output": str(n*n)})

    elif pid == "ve5":
        for _ in range(3):
            n = random.randint(-100,100)
            tests.append({"input": str(n), "output": str(abs(n))})

    elif pid == "ve6":
        for _ in range(3):
            n = random.randint(-1000,1000)
            tests.append({"input": str(n), "output": ("EVEN" if n%2==0 else "ODD")})

    elif pid == "ve7":
        for _ in range(3):
            a = random.randint(-20,20)
            b = random.randint(-20,20)
            tests.append({"input": f"{a} {b}", "output": str(a*b)})

    elif pid == "ve8":
        for _ in range(3):
            s = "".join(random.choices("abcdefghijklmnopqrstuvwxyz", k=random.randint(1,12)))
            tests.append({"input": s, "output": str(len(s))})

    elif pid == "ve9":
        for _ in range(3):
            s = "".join(random.choices("abcdxyz", k=random.randint(1,8)))
            tests.append({"input": s, "output": s[::-1]})

    elif pid == "ve10":
        names = ["Alice","Bob","Sam","Eve","John"]
        for _ in range(3):
            n = random.choice(names)
            tests.append({"input": n, "output": f"Hello {n}"})

    # ---- EASY ----

    elif pid == "e1":  # max
        for _ in range(3):
            N = random.randint(1,8)
            arr = [random.randint(-100,100) for _ in range(N)]
            tests.append({"input": f"{N}\n{' '.join(map(str,arr))}", "output": str(max(arr))})

    elif pid == "e2":  # min
        for _ in range(3):
            N = random.randint(1,8)
            arr = [random.randint(-50,50) for _ in range(N)]
            tests.append({"input": f"{N}\n{' '.join(map(str,arr))}", "output": str(min(arr))})

    elif pid == "e3":  # sum
        for _ in range(3):
            N = random.randint(1,8)
            arr = [random.randint(-20,20) for _ in range(N)]
            tests.append({"input": f"{N}\n{' '.join(map(str,arr))}", "output": str(sum(arr))})

    elif pid == "e4":  # count vowels
        for _ in range(3):
            s = "".join(random.choices("aeiouxyz ", k=random.randint(3,12))).strip()
            c = sum(1 for ch in s.lower() if ch in "aeiou")
            tests.append({"input": s, "output": str(c)})

    elif pid == "e5":  # palindrome
        for _ in range(3):
            s = "".join(random.choices("abc", k=random.randint(1,7)))
            tests.append({"input": s, "output": ("YES" if s==s[::-1] else "NO")})

    elif pid == "e6":  # digit count
        for _ in range(3):
            n = random.randint(0,10**8)
            tests.append({"input": str(n), "output": str(len(str(abs(n))))})

    elif pid == "e7":  # product digits
        for _ in range(3):
            n = random.randint(0,9999)
            p = 1
            for ch in str(abs(n)):
                if ch == "0":
                    p = 0
                    break
                p *= int(ch)
            tests.append({"input": str(n), "output": str(p)})

    elif pid == "e8":  # factorial (test fixed)
        import math
        for n in [0,1,5]:
            tests.append({"input": str(n), "output": str(math.factorial(n))})

    elif pid == "e9":  # fibonacci
        for n in [1,2,6]:
            a,b = 1,1
            for _ in range(n-1):
                a,b = b,a+b
            tests.append({"input": str(n), "output": str(a)})

    elif pid == "e10":
        for _ in range(3):
            N = random.randint(1,8)
            arr = [random.randint(-50,50) for _ in range(N)]
            tests.append({"input": f"{N}\n{' '.join(map(str,arr))}", "output": " ".join(map(str,sorted(arr)))})

    elif pid == "e11":
        for _ in range(3):
            words = random.randint(1,6)
            s = " ".join("".join(random.choices("abcxyz", k=random.randint(1,6))) for _ in range(words))
            tests.append({"input": s, "output": str(len(s.split()))})

    elif pid == "e12":
        for N in [2,5,10]:
            tests.append({"input": str(N), "output": str(sum(i for i in range(1,N+1) if i%2==0))})

    elif pid == "e13":
        for _ in range(3):
            s = "".join(random.choices("abcdabc", k=random.randint(1,10)))
            tests.append({"input": s, "output": str(len(set(s)))})

    elif pid == "e14":  # prime check
        def isprime(x):
            if x < 2: return False
            for i in range(2,int(x**0.5)+1):
                if x % i == 0: return False
            return True
        for n in [2,3,4,16,17]:
            tests.append({"input": str(n), "output": ("YES" if isprime(n) else "NO")})

    elif pid == "e15":  # second largest
        for _ in range(3):
            arr = random.sample(range(-50,50), k=random.randint(2,8))
            s = sorted(arr)
            tests.append({"input": f"{len(arr)}\n{' '.join(map(str,arr))}", "output": str(s[-2])})

    # ---- MEDIUM ----

    elif pid == "m1":
        for _ in range(3):
            N = random.randint(1,4)
            mat = [[random.randint(-10,10) for _ in range(N)] for __ in range(N)]
            total = sum(sum(r) for r in mat)
            body = "\n".join(" ".join(map(str,row)) for row in mat)
            tests.append({"input": f"{N}\n{body}", "output": str(total)})

    elif pid == "m2":
        import math
        for a,b in [(12,18),(7,13),(100,25)]:
            tests.append({"input": f"{a} {b}", "output": str(math.gcd(a,b))})

    elif pid == "m3":
        import math
        for a,b in [(4,6),(7,5),(21,6)]:
            tests.append({"input": f"{a} {b}", "output": str(a*b//math.gcd(a,b))})

    elif pid == "m4":
        for _ in range(3):
            N = random.randint(1,7)
            K = random.randint(0, N)
            arr = [random.randint(-20,20) for _ in range(N)]
            K %= N
            rotated = arr[-K:] + arr[:-K]
            tests.append({"input": f"{N} {K}\n{' '.join(map(str,arr))}", "output": " ".join(map(str,rotated))})

    elif pid == "m5":
        for _ in range(3):
            s = "".join(random.choices("dbca", k=random.randint(1,8)))
            tests.append({"input": s, "output": "".join(sorted(s))})

    elif pid == "m6":
        def count_primes(N):
            if N < 2: return 0
            sieve=[True]*(N+1)
            sieve[0]=sieve[1]=False
            import math
            for i in range(2,int(math.sqrt(N))+1):
                if sieve[i]:
                    for j in range(i*i,N+1,i):
                        sieve[j]=False
            return sum(sieve)
        for N in [10,20,2]:
            tests.append({"input": str(N), "output": str(count_primes(N))})

    elif pid == "m7":
        for _ in range(3):
            N = random.randint(1,8)
            arr = sorted(random.sample(range(0,50), k=N))
            target = random.choice(arr + [-1])
            idx = arr.index(target) if target in arr else -1
            tests.append({
                "input": f"{N}\n{' '.join(map(str,arr))}\n{target}",
                "output": str(idx)
            })

    elif pid == "m8":
        for _ in range(3):
            N = random.randint(1,8)
            arr = [random.randint(1,5) for _ in range(N)]
            from collections import Counter
            c = Counter(arr)
            mx = max(c.values())
            cand = [k for k,v in c.items() if v == mx]
            tests.append({
                "input": f"{N}\n{' '.join(map(str,arr))}",
                "output": str(min(cand))
            })

    elif pid == "m9":
        for _ in range(3):
            words = ["".join(random.choices("abcd", k=random.randint(1,7))) for _ in range(random.randint(1,6))]
            s = " ".join(words)
            longest = max(words, key=len)
            tests.append({"input": s, "output": longest})

    elif pid == "m10":
        for _ in range(3):
            a = random.sample(range(0,10), k=random.randint(1,6))
            b = random.sample(range(0,10), k=random.randint(1,6))
            inter = sorted(set(a).intersection(b))
            tests.append({
                "input": f"{len(a)} {len(b)}\n{' '.join(map(str,a))}\n{' '.join(map(str,b))}",
                "output": " ".join(map(str,inter)) if inter else ""
            })

    elif pid == "m11":
        for n in [123,9,1001]:
            s = sum(int(ch) for ch in str(abs(n)))
            tests.append({"input": str(n), "output": str(s)})

    elif pid == "m12":
        def balanced(s):
            st=[]
            pairs={')':'(',']':'[','}':'{'}
            for ch in s:
                if ch in "([{":
                    st.append(ch)
                elif ch in ")]}":
                    if not st or st[-1]!=pairs[ch]: return False
                    st.pop()
            return not st
        for s in ["()", "(]", "([{}])"]:
            tests.append({"input": s, "output": ("YES" if balanced(s) else "NO")})

    elif pid == "m13":
        for _ in range(3):
            N = random.randint(1,8)
            arr = [random.randint(-20,20) for _ in range(N)]
            tests.append({"input": f"{N}\n{' '.join(map(str,arr))}", "output": " ".join(map(str,sorted(arr)))})

    elif pid == "m14":
        for _ in range(3):
            N = random.randint(2,8)
            full = list(range(1,N+1))
            missing = random.choice(full)
            arr = [x for x in full if x != missing]
            random.shuffle(arr)
            tests.append({"input": f"{N-1}\n{' '.join(map(str,arr))}", "output": str(missing)})

    elif pid == "m15":
        for _ in range(3):
            N = random.randint(1,8)
            arr = [random.randint(-5,10) for _ in range(N)]
            best = max_sub = arr[0]
            for x in arr[1:]:
                max_sub = max(x, max_sub + x)
                best = max(best, max_sub)
            tests.append({
                "input": f"{N}\n{' '.join(map(str,arr))}",
                "output": str(best)
            })

    else:
        # fallback
        for _ in range(3):
            a = random.randint(1,10)
            b = random.randint(1,10)
            tests.append({"input": f"{a} {b}", "output": str(a+b)})

    return tests


#
# --- End of placeholder area ---
# (Replace the above two blocks with your full original PROBLEMS and gen_tests_for_problem)
# ===============================

# --------------------------
# Helpers
# --------------------------
def normalize_text(s: str) -> str:
    if s is None:
        return ""
    return s.replace("\r", "").strip()

def compare_output(actual: str, expected: str, case_insensitive=True) -> bool:
    a = normalize_text(actual)
    e = normalize_text(expected)
    if case_insensitive:
        return a.lower() == e.lower()
    return a == e

# --------------------------
# Judge0 runner (single execution)
# --------------------------
async def judge_run(lang: str, code: str, stdin: str):
    async with httpx.AsyncClient(timeout=30.0) as client:
        payload = {"source_code": code, "language_id": LANG_TO_ID.get(lang, 71), "stdin": stdin}
        try:
            r = await client.post(JUDGE0_URL, json=payload, headers={"Content-Type":"application/json"})
            data = r.json()
            return data.get("stdout") or data.get("stderr") or data.get("compile_output") or ""
        except Exception as e:
            return f"[Judge0 error] {e}"

# --------------------------
# Difficulty selection
# --------------------------
def get_difficulty_for_xp(xp):
    if xp < 50: return "Very Easy"
    if xp < 200: return "Easy"
    return "Medium"

# --------------------------
# Socket Events
# --------------------------
@sio.event
async def connect(sid, environ):
    print("[sio] connect", sid)

@sio.event
async def disconnect(sid):
    print("[sio] disconnect", sid)
    # auto-forfeit if in match
    for room, match in list(matches.items()):
        if sid in match["players"]:
            opponent = match["players"][0] if match["players"][1] == sid else match["players"][1]
            await finalize_match(room, winner_sid=opponent, loser_sid=sid)
            break

@sio.event
async def join_queue(sid, data):
    global waiting_player
    print("[JOIN_QUEUE]", sid, data)

    uid = data.get("uid")
    name = data.get("name", "Player")

    # Load XP
    try:
        snap = db.collection("users").document(uid).get()
        xp = snap.to_dict().get("xp", 0) if snap.exists else 0
    except Exception:
        xp = 0

    # CASE 1: No waiting player -> set waiting
    if not waiting_player:
        waiting_player = {"sid": sid, "uid": uid, "name": name, "xp": xp}
        await sio.emit("waiting", {"msg": "Waiting for opponent..."}, to=sid)
        print("[QUEUE] placed:", waiting_player)
        return

    # CASE 2: Waiting player exists → check if SID still alive
    p1 = waiting_player
    
    

    # check if old player is disconnected
    active_sids = sio.manager.rooms.get("/", {}).keys()

    if p1["sid"] not in active_sids:
        print("[QUEUE] old waiting player disconnected. Replacing with new player.")
        waiting_player = {"sid": sid, "uid": uid, "name": name, "xp": xp}
        await sio.emit("waiting", {"msg": "Waiting for opponent..."}, to=sid)
        return


    # NOW WE HAVE TWO REAL ACTIVE PLAYERS
    p2 = {"sid": sid, "uid": uid, "name": name, "xp": xp}
    waiting_player = None

    difficulty = get_difficulty_for_xp((p1["xp"] + p2["xp"]) // 2)
    problem = random.choice(PROBLEMS[difficulty])
    tests = gen_tests_for_problem(problem["id"], problem["title"])

    room = f"room_{p1['uid']}_{p2['uid']}"
    start_time = int(time.time())

    matches[room] = {
        "players": [p1["sid"], p2["sid"]],
        "uids": [p1["uid"], p2["uid"]],
        "names": [p1["name"], p2["name"]],
        "problem": {**problem, "difficulty": difficulty},
        "tests": tests,
        "best": {},
        "startTime": start_time,
        "timeLimit": 600 if difficulty == "Medium" else 300
    }
    import asyncio
    asyncio.create_task(match_timeout_watch(room))

    print("[MATCH CREATED]", room, "difficulty:", difficulty, "problem:", problem["title"])

    await sio.enter_room(p1["sid"], room)
    await sio.enter_room(p2["sid"], room)

    payload = {
        "room": room,
        "problem": problem,
        "timeLimit": matches[room]["timeLimit"],
        "testsCount": len(tests),
        "startTime": start_time
    }

    await sio.emit("match_found", {**payload, "opponent": {"name": p2["name"], "uid": p2["uid"]}}, to=p1["sid"])
    await sio.emit("match_found", {**payload, "opponent": {"name": p1["name"], "uid": p1["uid"]}}, to=p2["sid"])




# --------------------------
# run_code (custom stdin)
# --------------------------
@sio.event
async def run_code(sid, data):
    """
    data: { room, language, source_code, stdin }
    Returns run_result to caller only.
    """
    lang = data.get("language","python")
    code = data.get("source_code","")
    stdin = data.get("stdin","")
    out = await judge_run(lang, code, stdin)
    await sio.emit("run_result", {"stdout": out or ""}, to=sid)

# --------------------------
# submit_code (hidden tests) — wait for both players
# --------------------------
@sio.event
async def submit_code(sid, data):
    """
    data: { language, source_code }
    """
    lang = data.get("language","python")
    code = data.get("source_code","")

    # find match for sid
    room = None
    for r,m in matches.items():
        if sid in m["players"]:
            room = r
            match = m
            break
    if not room:
        await sio.emit("error", {"msg":"Not in match"}, to=sid)
        return

    passed = 0
    total = len(match["tests"])

    # run hidden tests sequentially
    for t in match["tests"]:
        stdin = t.get("input","")
        out_raw = await judge_run(lang, code, stdin)
        out = out_raw or ""
        if compare_output(out, t.get("output","")):
            passed += 1

    match["best"][sid] = {"passed": passed, "total": total, "ts": time.time()}

    # send submission_result back to player
    await sio.emit("submission_result", {"passed": passed, "total": total}, to=sid)

    # If both have submitted, decide winner (2s delay for "calculating")
    p1, p2 = match["players"]
    if p1 in match["best"] and p2 in match["best"]:
        # 2-second "calculating" delay
        await sio.sleep(2.0)

        r1 = match["best"][p1]
        r2 = match["best"][p2]

        # Compare passed counts
        if r1["passed"] > r2["passed"]:
            await finalize_match(room, winner_sid=p1, loser_sid=p2)
        elif r2["passed"] > r1["passed"]:
            await finalize_match(room, winner_sid=p2, loser_sid=p1)
        else:
            # tie -> earlier submission wins
            if r1["ts"] < r2["ts"]:
                await finalize_match(room, winner_sid=p1, loser_sid=p2)
            elif r2["ts"] < r1["ts"]:
                await finalize_match(room, winner_sid=p2, loser_sid=p1)
            else:
                # exact tie -> random
                winner_sid = random.choice([p1, p2])
                loser_sid = p2 if winner_sid == p1 else p1
                await finalize_match(room, winner_sid=winner_sid, loser_sid=loser_sid)

# --------------------------
# forfeit
# --------------------------
@sio.event
async def forfeit(sid, data=None):
    for room, match in list(matches.items()):
        if sid in match["players"]:
            opp = match["players"][1] if match["players"][0] == sid else match["players"][0]
            await finalize_match(room, winner_sid=opp, loser_sid=sid)
            break

# --------------------------
# finalize_match
# --------------------------
async def finalize_match(room, winner_sid, loser_sid):
    if room not in matches:
        return
    match = matches[room]
    try:
        w_idx = match["players"].index(winner_sid)
        l_idx = match["players"].index(loser_sid)
    except ValueError:
        del matches[room]
        return

    winner_uid = match["uids"][w_idx]
    loser_uid = match["uids"][l_idx]
    problem = match["problem"]
    now = datetime.datetime.utcnow()

    

    

    # Update XP and W/L in Firestore
    try:
        db.collection("users").document(winner_uid).set({
            "wins": firestore.Increment(1),
            "xp": firestore.Increment(WIN_XP),
            "updatedAt": now
        }, merge=True)
        db.collection("users").document(loser_uid).set({
            "losses": firestore.Increment(1),
            "xp": firestore.Increment(LOSS_XP),
            "updatedAt": now
        }, merge=True)
    except Exception as e:
        print("[ERROR] Firestore update:", e)

    # Save match records to each player's subcollection
    for idx, uid in enumerate(match["uids"]):
        passed = match["best"].get(match["players"][idx], {}).get("passed", 0)
        total = match["best"].get(match["players"][idx], {}).get("total", len(match["tests"]))
        try:
            db.collection("users").document(uid).collection("matches").add({
                "winnerId": winner_uid,
                "problem": problem.get("title"),
                "difficulty": problem.get("difficulty", "Unknown"),
                "passed": passed,
                "total": total,
                "endedAt": now
            })
        except Exception as e:
            print("[ERROR] saving match:", e)

    # Emit battle_result to room (frontend shows summary)
    summary = f"🏆 Winner: {match['names'][w_idx]}"
    analytics = {
        "winner": winner_uid,
        "players": [
            {"name": match["names"][w_idx], "passed": match['best'].get(match['players'][w_idx], {}).get("passed", 0)},
            {"name": match["names"][l_idx], "passed": match['best'].get(match['players'][l_idx], {}).get("passed", 0)}
        ],
        "problem": {"title": problem.get("title"), "difficulty": problem.get("difficulty", "Unknown")}
    }

    await sio.emit("battle_result", {"summary": summary, "analytics": analytics}, room=room)

    # cleanup
    try:
        del matches[room]
    except KeyError:
        pass

    # ======================================================
# ⏳ AUTO TIMEOUT WATCHER — triggers when time expires
# ======================================================
async def match_timeout_watch(room):
    await sio.sleep(2)

    if room not in matches:
        return

    match = matches[room]
    start_time = match.get("startTime", int(time.time()))
    time_limit = match.get("timeLimit", 300)

    now = int(time.time())
    remaining = max(0, start_time + time_limit - now)
    await sio.sleep(remaining)

    if room not in matches:
        return

    p1, p2 = match["players"]
    best = match.get("best", {})

    # CASE 1 — both submitted
    if p1 in best and p2 in best:
        return

    # CASE 2 — only one submitted
    if p1 in best and p2 not in best:
        await finalize_match(room, winner_sid=p1, loser_sid=p2)
        return

    if p2 in best and p1 not in best:
        await finalize_match(room, winner_sid=p2, loser_sid=p1)
        return

    # CASE 3 — none submitted → DRAW
    await finalize_draw(room)

    # ======================================================
# 🤝 FINALIZE DRAW — no winner, no XP
# ======================================================
async def finalize_draw(room):
    if room not in matches:
        return

    match = matches[room]
    problem = match["problem"]
    uids = match["uids"]
    names = match["names"]
    now = datetime.datetime.utcnow()

    # Save match record with DRAW
    for uid in uids:
        try:
            db.collection("users").document(uid).collection("matches").add({
                "winnerId": None,
                "problem": problem.get("title"),
                "difficulty": problem.get("difficulty", "Unknown"),
                "passed": 0,
                "total": len(match["tests"]),
                "endedAt": now,
                "result": "draw"
            })
        except Exception as e:
            print("[ERROR] saving draw:", e)

    # Send draw event to frontend
    await sio.emit("battle_result", {
        "summary": "🤝 Draw — Time Expired",
        "analytics": {
            "winner": None,
            "players": [
                {"name": names[0], "passed": 0},
                {"name": names[1], "passed": 0}
            ],
            "problem": {
                "title": problem.get("title"),
                "difficulty": problem.get("difficulty")
            }
        }
    }, room=room)

    # Cleanup match
    try:
        del matches[room]
    except:
        pass

 
