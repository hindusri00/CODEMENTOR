# Recursion
Recursion is when a method calls itself to solve a smaller version of the same problem. Every recursive method needs a base case (when to stop) and a recursive case that moves toward the base case.
Missing or unreachable base cases cause StackOverflowError. Naive recursion like fibonacci(n-1) + fibonacci(n-2) repeats work and is O(2^n); memoization (storing results in a HashMap or array) or a loop fixes this.
