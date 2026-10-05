# ArrayList vs LinkedList
ArrayList stores items in an array: get(i) is O(1), adding at the end is O(1) amortized, inserting or removing in the middle is O(n).
LinkedList stores nodes: get(i) is O(n) because it must walk from the start, but inserting at a known node is O(1).
In practice ArrayList is the right default for beginners. Calling get(i) in a loop over a LinkedList is a common hidden O(n^2).
