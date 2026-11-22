
# PYTHON PROGRAMMING ASSIGNMENT 2
# Name: ARJUN A B
# Register Number: 1911260006

import time
from functools import lru_cache


# ==================================================
# Q1 - DECISIONS WITH MANY BOUNDARIES
# ==================================================

def subsidy_separate(units, ration_card, member_over_80):
    results = []

    if 0 <= units <= 100:
        results.append("Full subsidy")

    if 101 <= units <= 200 and ration_card:
        results.append("Partial subsidy")

    if units > 200 and member_over_80:
        results.append("Elderly-exception subsidy")

    if not results:
        results.append("No subsidy")

    return results


def subsidy_chain(units, ration_card, member_over_80):
    if 0 <= units <= 100:
        return "Full subsidy"

    elif 101 <= units <= 200:
        if ration_card:
            return "Partial subsidy"
        else:
            return "No subsidy"

    elif units > 200:
        if member_over_80:
            return "Elderly-exception subsidy"
        else:
            return "No subsidy"

    else:
        return "Invalid consumption"


def subsidy_match(units, ration_card, member_over_80):
    slab = ("low" if 0 <= units <= 100 else
            "middle" if 101 <= units <= 200 else
            "high" if units > 200 else "invalid")

    match slab:
        case "low":
            return "Full subsidy"
        case "middle" if ration_card:
            return "Partial subsidy"
        case "middle":
            return "No subsidy"
        case "high" if member_over_80:
            return "Elderly-exception subsidy"
        case "high":
            return "No subsidy"
        case _:
            return "Invalid consumption"


def subsidy_lookup(units, ration_card, member_over_80):
    slabs = [(100, "low"), (200, "middle"),
             (float("inf"), "high")]

    for upper, label in slabs:
        if units <= upper:
            if label == "low":
                return "Full subsidy"
            if label == "middle":
                return "Partial subsidy" if ration_card else "No subsidy"
            return ("Elderly-exception subsidy"
                    if member_over_80 else "No subsidy")

    return "Invalid consumption"


households = [
    (100, False, False),
    (101, True, False),
    (200, False, False),
    (201, False, True),
    (99, True, False),
    (150, False, True),
    (250, True, False),
    (180, True, True)
]

print("\n========== Q1: SUBSIDY CALCULATION ==========")

for household in households:
    print(household, "=>", subsidy_chain(*household))


# ==================================================
# Q2 - LOOPS THAT COUNT ATTEMPTS
# ==================================================

def verify_while(correct_otp):
    attempts = 0

    while attempts < 3:
        entered = input("Enter OTP: ").strip()

        if entered == "":
            print("Blank entry: not counted.")
            continue

        if entered == correct_otp:
            print("Verified.")
            break

        attempts += 1
        print("Incorrect OTP.")

    else:
        print("Account locked for 30 minutes.")


def verify_for(correct_otp):
    for attempt in range(3):
        entered = input("Enter OTP: ").strip()

        while entered == "":
            print("Blank entry: not counted.")
            entered = input("Enter a nonblank OTP: ").strip()

        if entered == correct_otp:
            print("Verified.")
            break

        print("Incorrect OTP.")

    else:
        print("Account locked for 30 minutes.")


def verify_with_security(correct_otp, security_ok):
    limit = 5 if security_ok else 3
    wrong = 0

    while wrong < limit:
        entered = input("Enter OTP: ").strip()

        if entered == "":
            print("Blank entry: not counted.")
            continue

        if entered == correct_otp:
            print("Verified.")
            break

        wrong += 1
        print("Incorrect OTP.")

    else:
        print("Account locked for 30 minutes.")


def verify_recursive(correct_otp, remaining):
    if remaining == 0:
        print("Account locked for 30 minutes.")
        return

    entered = input("Enter OTP: ").strip()

    if entered == "":
        print("Blank entry: not counted.")
        return verify_recursive(correct_otp, remaining)

    if entered == correct_otp:
        print("Verified.")
        return

    print("Incorrect OTP.")
    return verify_recursive(correct_otp, remaining - 1)


# Uncomment to test OTP verification:
# verify_while("1234")
# verify_for("1234")
# verify_with_security("1234", True)
# verify_recursive("1234", 3)


# ==================================================
# Q3 - VEHICLE REGISTRATION NUMBER VALIDATOR
# ==================================================

def normalise(text):
    return text.replace(" ", "").replace("-", "").upper()


def is_valid(reg):
    if len(reg) not in (9, 10):
        return False

    if not reg[0:2].isalpha() or not reg[2:4].isdigit():
        return False

    if len(reg) == 9:
        return reg[4:5].isalpha() and reg[5:9].isdigit()

    return reg[4:6].isalpha() and reg[6:10].isdigit()


def format_reg(reg):
    if not is_valid(reg):
        raise ValueError("Invalid registration number")

    series_end = len(reg) - 4

    return (reg[0:2] + " " + reg[2:4] + " " +
            reg[4:series_end] + " " + reg[-4:])


print("\n========== Q3: VEHICLE VALIDATOR ==========")

samples = [
    "tn 09 ab 1234",
    "KA-01-M-0007",
    "Tn09Ab1234",
    "TN9AB1234",
    "TN 22 1234 AB",
    "MH 12 XY 9876"
]

for raw in samples:
    reg = normalise(raw)

    print(raw, "->", reg,
          "Valid" if is_valid(reg) else "INVALID")

    if is_valid(reg):
        print("Receipt:", format_reg(reg))


# ==================================================
# Q4 - BUILDING LONG TEXT: + OR JOIN()
# ==================================================

def build_plus(parts):
    text = ""

    for p in parts:
        text += p + ";"

    return text


def build_join(parts):
    return "".join(p + ";" for p in parts)


def build_fstring(parts):
    lines = [f"{p};" for p in parts]
    return "".join(lines)


def measure(func, parts, repeats=3):
    samples = []

    for _ in range(repeats):
        start = time.perf_counter()
        result = func(parts)
        samples.append(time.perf_counter() - start)

    return result, sum(samples) / len(samples)


print("\n========== Q4: STRING PERFORMANCE ==========")

for size in [1000, 10000, 200000]:
    parts = [f"Line {i}" for i in range(size)]

    plus_result, plus_time = measure(build_plus, parts)
    join_result, join_time = measure(build_join, parts)
    fstring_result, fstring_time = measure(build_fstring, parts)

    print("\nNumber of lines:", size)
    print("Plus time:", round(plus_time, 6), "seconds")
    print("Join time:", round(join_time, 6), "seconds")
    print("F-string time:", round(fstring_time, 6), "seconds")
    print("Output characters:", len(join_result))


def write_statement(path, parts):
    with open(path, "w", encoding="utf-8") as f:
        for p in parts:
            f.write(p)
            f.write(";")


from io import StringIO


def build_stringio(parts):
    buffer = StringIO()

    for p in parts:
        buffer.write(p)
        buffer.write(";")

    return buffer.getvalue()


# ==================================================
# Q5 - FUNCTIONS, PARAMETERS AND SCOPE
# ==================================================

def add_item_buggy(item, order=[]):
    order.append(item)
    return order


def add_item(item, order=None):
    if order is None:
        order = []

    order.append(item)
    return order


def bill(subtotal, gst_rate=0.05):
    gst = subtotal * gst_rate
    total = subtotal + gst

    return total, gst


count = 10


def local_demo():
    count = 3
    return count


def global_demo():
    global count
    count += 1


def make_counter():
    value = 0

    def increment():
        nonlocal value
        value += 1
        return value

    return increment


def create_order(items):
    order = []

    for item in items:
        add_item(item, order)

    return order


print("\n========== Q5: FUNCTIONS AND SCOPE ==========")

print("Buggy:", add_item_buggy("Tea"),
      add_item_buggy("Vada"))

print("Correct:", add_item("Tea"),
      add_item("Vada"))

print("Stored default:", add_item_buggy.__defaults__)

total, gst = bill(200, gst_rate=0.05)
print("Bill total:", total, "GST:", gst)

print("Local and global:", local_demo(), count)

global_demo()
print("Updated global:", count)

counter = make_counter()
print("Counter:", counter(), counter())

customers = [
    create_order(["Tea", "Vada"]),
    create_order(["Coffee"]),
    create_order(["Idli", "Dosa", "Chutney"])
]

for number, order in enumerate(customers, start=1):
    print(f"Customer {number}: {order}")


# ==================================================
# Q6 - RECURSION AND ITS LIMITS
# ==================================================

def ways_naive(n):
    if n <= 1:
        return 1

    return ways_naive(n - 1) + ways_naive(n - 2)


@lru_cache(maxsize=None)
def ways_memo(n):
    if n <= 1:
        return 1

    return ways_memo(n - 1) + ways_memo(n - 2)


def ways_iterative(n):
    if n < 0:
        raise ValueError("n must be non-negative")

    if n <= 1:
        return 1

    previous, current = 1, 1

    for _ in range(2, n + 1):
        previous, current = current, previous + current

    return current


print("\n========== Q6: RECURSION ==========")

for n in range(1, 7):
    print("Steps:", n,
          "Ways:", ways_iterative(n))

print("\nNaive result for 10:", ways_naive(10))
print("Memoised result for 25:", ways_memo(25))
print("Iterative result for 25:", ways_iterative(25))

print("Recursion limit investigation:")
import sys
print(sys.getrecursionlimit())

result = ways_iterative(1000)
print("Ways for 1000 steps calculated.")
print("Number of digits:", len(str(result)))


# ==================================================
# Q7 - DIAGNOSE, REDESIGN AND VALIDATE
# ==================================================

def ways_redesigned(n):
    if n < 0:
        raise ValueError("n must be non-negative")

    if n <= 1:
        return 1

    two_back, one_back = 1, 1

    for step in range(2, n + 1):
        current = two_back + one_back
        two_back, one_back = one_back, current

    return one_back


print("\n========== Q7: REDESIGNED PROGRAM ==========")

# Validate results for n = 1 to 6
for n in range(1, 7):
    assert ways_redesigned(n) == ways_memo(n)
    print(n, ways_redesigned(n))

# Validate n = 25
assert ways_redesigned(25) == 121393

print("\nValidation successful!")
print("Result for n=25:", ways_redesigned(25))

# Test n = 1000
result_1000 = ways_redesigned(1000)

print("n=1000 computed successfully.")
print("Number of digits:", len(str(result_1000)))

print("\nAll assignment programs executed successfully.")
