# Nested Loops
A nested loop is a loop inside another loop. If both loops run over n items, the inner statement runs about n * n times, giving O(n^2) time.
Nested loops are fine for small inputs, 2D grids, or when you truly need every pair. They become a problem when n is large (thousands or more) or when the inner loop is only searching for something.
Ways to reduce them: use a HashSet/HashMap for lookups, sort the data and use two pointers, or break out early when the answer is found.
