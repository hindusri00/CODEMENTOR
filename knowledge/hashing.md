# Hashing and HashMap
A HashMap stores key-value pairs and finds a key in about constant time, O(1) on average, because a hash function turns the key into an array position.
A HashSet only stores keys and answers "have I seen this value before?" in O(1) average time.
Use a HashMap or HashSet to replace a nested loop that searches for a matching value: store each value as you go, then look up what you need instead of scanning the whole array again.
Example idea for two-sum: for each number x, check if (target - x) is already in the set; if not, add x to the set. This turns O(n^2) into O(n) with extra memory.
Keys need correct equals() and hashCode() methods.
