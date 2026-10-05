# Time Complexity
Time complexity describes how the running time of code grows as the input size n grows. It is written in Big-O notation.
O(1) is constant, O(log n) grows slowly (binary search), O(n) grows in proportion to input (one loop), O(n^2) grows with the square (nested loops over the same data).
To estimate it, count how many times the innermost statement runs relative to n. Nested loops that each go over n items multiply: n * n = n^2.
Doubling the input of an O(n^2) algorithm makes it about four times slower. Improving complexity usually means doing less repeated work, often by remembering things in a better data structure.
