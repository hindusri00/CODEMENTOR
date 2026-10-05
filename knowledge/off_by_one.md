# Off-by-One Errors and Array Bounds
Arrays in Java are zero-indexed: valid indexes go from 0 to length - 1. Using i <= array.length in a loop causes ArrayIndexOutOfBoundsException.
Check loop boundaries: should the condition be < or <=? Test the first, last, and empty-input cases by hand.
