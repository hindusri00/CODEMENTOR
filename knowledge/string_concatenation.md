# String Concatenation in Loops
Strings in Java are immutable. Each time you write s += "x", Java creates a brand new String and copies the old characters, so building a string in a loop of n steps costs O(n^2).
Use StringBuilder instead: call append() inside the loop and toString() at the end. This is O(n).
A single concatenation outside a loop is fine.
