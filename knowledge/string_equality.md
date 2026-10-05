# Comparing Strings: == vs equals()
In Java, == compares whether two variables point to the same object in memory, not whether the text is the same. Two Strings with identical text can still be different objects.
Use s1.equals(s2) to compare text. To avoid NullPointerException when s1 might be null, write "literal".equals(s1).
Use equalsIgnoreCase() when case should not matter.
