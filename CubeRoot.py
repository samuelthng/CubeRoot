# Author:       Thng Zhe Yu Samuel
# Updated:      17 September 2017
# Course:       EE4483 AI & Data Mining
# Project:      Individual Project 1
# Description:  Cube Root Search Demo with 4 search methods
# Comments:     - My first threaded python scrip.
#               - I'm proud of it. :D
#               - Sections are marked with three "#"
#               - Apologies for verbosity, I enjoyed the project!
#               - Search Functions: Line 21-158.
#               - Main Program: Line 165 onward.
################################################

### Multi-threading Stuff for Performance ###
import multiprocessing
from multiprocessing.pool import ThreadPool

cores = multiprocessing.cpu_count()
pool = ThreadPool(processes=cores)

### Declare Functions ###
# Incrementing Search O(log n)


def incrementalSearch(x, accuracyFactor):
    # Options
    rootPower = 3
    incrementFactor = 2
    searchIteration = 0

    # Other conditionals.
    hi = (-1.0, 1.0)[x > 0]  # Negative Numbers
    hi = (hi, x / 2)[abs(x) < 1.0]  # < 1 values

    # If magnitude power is lesser, increment.
    while abs(pow(hi, rootPower)) < abs(x):
        searchIteration += 1
        hi *= incrementFactor
    lo = hi / incrementFactor

    # Check difference is within accuracy requirement
    while abs(hi - lo) > pow(10, -(accuracyFactor + 1)):
        searchIteration += 1
        mid = (lo + hi) / incrementFactor
        midCube = pow(mid, rootPower)
        if abs(midCube) < abs(x):
            lo = mid  # Too low, cut again.
        elif abs(x) < abs(midCube):
            hi = mid  # Too high. Take mid as new high.
        else:
            return mid, searchIteration  # Mid is exactly X now.

    # Found exact root
    if pow(hi, rootPower) == x:
        return hi, searchIteration
    else:
        # Didn't find, returning closest lower bound.
        return lo, searchIteration

# Binary Search O(log n)


def binarySearch(x, accuracyFactor):
    # Gonna use this often.
    def getMid(low, high):
        return (low + high) / 2.0

    # Options: Power of the root.
    rootPower = 3

    # Initialize
    hi = x
    lo = (-1.0, 1.0)[x > 0]  # Negative Numbers
    # Hacky fix for < 1 Numbers
    if x == 0:
        return 0, 0

    if abs(x) < 1.0:
        tmp = lo
        lo = hi
        hi = tmp
    mid = getMid(lo, hi)
    searchIteration = 0

    # Termination clause
    while abs(pow(mid, rootPower) - x) > pow(10, -(accuracyFactor + 1)):
        searchIteration += 1  # Increment Iteration

        if abs(pow(mid, rootPower)) > abs(x):  # Too high, search lower.
            hi = mid
            mid = getMid(lo, hi)
        elif abs(pow(mid, rootPower)) < abs(x):  # Too low, shift up.
            lo = mid
            mid = getMid(lo, hi)

        # Fix bug where the floats accuracy causes algorithm to fall through.
        # The fix works by comparing numbers in consideration
        # If numbers are in tolerance of each other, results are achieved.
        if abs(hi - lo) < pow(10, -(accuracyFactor + 1)):
            return mid, searchIteration

    return mid, searchIteration  # Return mid.

# Newthon-Rhapson Method O( f(n) * log n)


def newtonRoot(n, accuracyFactor):
    # Fix bug: Prevent Division by 0
    if n == 0:
        return 0.0, 0.0
    # Newton-Raphson equation for next nearest point for cube root

    def nextEqn(approx, n):
        # f(x) = x^3 - n
        # Therefore, f'(x) = 3x^2
        return (approx - (pow(approx, 3) - n) / (3 * pow(approx, 2)))

    # Initialize Values
    approx = n / 3
    better = nextEqn(approx, n)
    searchIteration = 0

    # Repeat until either Python Float converges or hits error tolerance.
    while better != approx:
        searchIteration += 1
        approx = better
        better = nextEqn(approx, n)
        # Return immediately if satisfies error tolerance.
        if abs(pow(approx, 3) - n) <= pow(10, -(accuracyFactor + 1)):
            return better, searchIteration  # Force a return if in tolerance.

        # Fix bug where the floats accuracy causes algorithm to fall through.
        # The fix works by comparing all 3 numbers in consideration
        # If numbers are in tolerance of each other, results are achieved.
        approxToBetter = abs(approx - better) < pow(10, -(accuracyFactor + 1))
        if approxToBetter:
            return approx, searchIteration

    return approx, searchIteration  # If we happen to hit the answer, return.

# Halley's Method O( g(n) * log n); g(n) < f(n)


def halleyRoot(n, accuracyFactor):
    # Fix bug: Prevent Division by 0
    if n == 0:
        return 0.0, 0.0
    # Halley's equation for next nearest point for cube root

    def halleyEqn(approx, n):
        return approx * ((pow(approx, 3) + 2 * n) / (2 * pow(approx, 3) + n))

    # Initialize Values
    approx = n / 3
    better = halleyEqn(approx, n)
    searchIteration = 0

    # Repeat until either Python Float converges or hits error tolerance.
    while better != approx:
        searchIteration += 1
        approx = better
        better = halleyEqn(approx, n)
        # Return immediately if satisfies error tolerance.
        if abs(pow(approx, 3) - n) <= pow(10, -(accuracyFactor + 1)):
            return better, searchIteration  # Force a return if in tolerance.

        # Fix bug where the floats accuracy causes algorithm to fall through.
        # The fix works by comparing all 3 numbers in consideration
        # If numbers are in tolerance of each other, results are achieved.
        approxToBetter = abs(approx - better) < pow(10, -(accuracyFactor + 1))
        if approxToBetter:
            return approx, searchIteration
    return approx, searchIteration  # If we happen to hit the answer, return.

# Helper function to print my results easily.


def printResult(value, accuracy, (result, iteration), method):
    message = "\t3" + u"\u221A".encode('utf-8') + " %." + str(accuracy) + \
        "f = %." + str(accuracy) + "f, found after %d tries."
    print ("| " + method + message % (value, result, iteration))


### Actual Program Starts Here ###
# User Inputs & Input Control
print("\n\n#=====[ Samuel's Cube Root Search! ]=====#")
print("| -> Found " + str(cores) + " cores for processing.")
print("| -> Multi-thread all the things!\n|")
number = float(raw_input("| Enter a number: "))
try:
    error = abs(int(raw_input("| Enter degree of accuracy (no of decimal place <= 12, default: 9): ")))
except ValueError:
    error = int(9)
    print("| Default to 9 decimal places.")
if abs(error) > 12:
    print("| " + str(error) + " > 12, using 12.")
    error = int(12)
print("#========================================#\n")

# Calculate results in threads, make use of ALL THE CORES!
IS = pool.apply_async(incrementalSearch, (number, error))
NM = pool.apply_async(newtonRoot, (number, error))
HM = pool.apply_async(halleyRoot, (number, error))
BS = pool.apply_async(binarySearch, (number, error))

# Print Legend
print("#=====[ Legend  ]=====#")
print("| [IS]:\tIncremental Search (or Exponential Search)")
print("| [BS]:\tBinary Search")
print("| [NM]:\tNewton-Rhapson's Method with modified Babylonian Equation")
print("| [HM]:\tHalley's Method")
print("#========================================#\n")

# Print Results
print("#=====[ Results ]=====#")
(printResult(number, error, IS.get(), "[IS]"))
(printResult(number, error, NM.get(), "[NM]"))
(printResult(number, error, HM.get(), "[HM]"))
(printResult(number, error, BS.get(), "[BS]"))
print("#========================================#\n")
