# Searching in Lists vs Sets
Calling contains() or indexOf() on an ArrayList scans element by element, so each call is O(n). Doing it inside a loop makes the total O(n^2).
HashSet.contains() is O(1) on average. If you repeatedly ask "is this value present?", convert the list to a HashSet first.
Removing from the middle of an ArrayList is also O(n) because elements must shift.
