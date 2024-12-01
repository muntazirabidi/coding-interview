# String Operations - Complete Interview Guide

## Table of Contents
- [String Fundamentals](#string-fundamentals)
- [Common String Patterns](#common-string-patterns)
- [String Manipulation](#string-manipulation)
- [String Algorithms](#string-algorithms)
- [Common Problems with Solutions](#common-problems-with-solutions)
- [Time Complexity Analysis](#time-complexity-analysis)
- [Best Practices](#best-practices)

## String Fundamentals

### Basic Operations
```python
# String creation
s = "hello"
s = 'hello'
s = str(123)

# String properties
length = len(s)               # Get length
char = s[0]                  # Access character
last_char = s[-1]            # Last character
substring = s[1:4]           # Slicing

# String immutability
s = "hello"
s = s + " world"             # Creates new string
s = s.replace('l', 'L')      # Creates new string
```

### String Methods
```python
s = "Hello World"

# Case operations
s.lower()           # Convert to lowercase
s.upper()           # Convert to uppercase
s.title()           # Title case
s.capitalize()      # Capitalize first letter

# Checking string properties
s.isalpha()         # Only alphabetic characters
s.isdigit()         # Only digits
s.isalnum()         # Alphanumeric
s.isspace()         # Only whitespace
s.isupper()         # All uppercase
s.islower()         # All lowercase

# Finding and counting
s.count('l')        # Count occurrences
s.find('o')         # First occurrence (returns -1 if not found)
s.index('o')        # First occurrence (raises ValueError if not found)
s.rfind('o')        # Last occurrence
```

## Common String Patterns

### 1. Character Count/Frequency
```python
def get_char_frequency(s):
    # Using dictionary
    freq = {}
    for char in s:
        freq[char] = freq.get(char, 0) + 1
    return freq

    # Using Counter
    from collections import Counter
    return Counter(s)
```

### 2. Palindrome Check
```python
def is_palindrome(s):
    # Simple palindrome check
    s = ''.join(c.lower() for c in s if c.isalnum())
    return s == s[::-1]

def is_palindrome_two_pointer(s):
    # Two pointer approach
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True
```

### 3. String Building
```python
def build_string_efficiently(chars):
    # Bad practice (creates new string each time)
    result = ""
    for char in chars:
        result += char
    
    # Good practice (list join)
    return ''.join(chars)

    # Using StringBuilder pattern
    from io import StringIO
    builder = StringIO()
    for char in chars:
        builder.write(char)
    return builder.getvalue()
```

## String Manipulation

### 1. String Reversal
```python
def reverse_string(s):
    # Using slicing
    return s[::-1]

    # Using reversed
    return ''.join(reversed(s))

def reverse_words(s):
    # Reverse individual words
    return ' '.join(word[::-1] for word in s.split())

    # Reverse word order
    return ' '.join(s.split()[::-1])
```

### 2. String Replacement
```python
def replace_substring(s, old, new):
    # Using replace method
    return s.replace(old, new)

    # Manual replacement
    result = []
    i = 0
    while i < len(s):
        if s[i:i+len(old)] == old:
            result.append(new)
            i += len(old)
        else:
            result.append(s[i])
            i += 1
    return ''.join(result)
```

## String Algorithms

### 1. Pattern Matching (KMP Algorithm)
```python
def build_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1
    
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text, pattern):
    if not pattern:
        return 0
        
    lps = build_lps(pattern)
    i = j = 0
    matches = []
    
    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1
        else:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
                
        if j == len(pattern):
            matches.append(i - j)
            j = lps[j - 1]
            
    return matches
```

### 2. String Hashing (Rolling Hash)
```python
def calculate_rolling_hash(s, base=26, mod=10**9 + 7):
    hash_value = 0
    for char in s:
        hash_value = (hash_value * base + (ord(char) - ord('a'))) % mod
    return hash_value

def rabin_karp(text, pattern):
    pattern_hash = calculate_rolling_hash(pattern)
    pattern_len = len(pattern)
    current_hash = calculate_rolling_hash(text[:pattern_len])
    
    if pattern_hash == current_hash and text[:pattern_len] == pattern:
        yield 0
    
    # Calculate power of base
    base = 26
    power = 1
    for _ in range(pattern_len - 1):
        power = (power * base) % (10**9 + 7)
    
    for i in range(len(text) - pattern_len):
        # Remove first character
        current_hash = (current_hash - (ord(text[i]) - ord('a')) * power) % (10**9 + 7)
        # Add new character
        current_hash = (current_hash * base + (ord(text[i + pattern_len]) - ord('a'))) % (10**9 + 7)
        
        if pattern_hash == current_hash and text[i+1:i+1+pattern_len] == pattern:
            yield i + 1
```

## Common Problems with Solutions

### 1. Longest Palindromic Substring
```python
def longest_palindromic_substring(s):
    if not s:
        return ""
        
    start = 0
    max_length = 1
    
    def expand_around_center(left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return right - left - 1
    
    for i in range(len(s)):
        len1 = expand_around_center(i, i)
        len2 = expand_around_center(i, i + 1)
        length = max(len1, len2)
        
        if length > max_length:
            max_length = length
            start = i - (length - 1) // 2
            
    return s[start:start + max_length]
```

### 2. String Compression
```python
def compress_string(s):
    if not s:
        return ""
        
    result = []
    count = 1
    current_char = s[0]
    
    for i in range(1, len(s)):
        if s[i] == current_char:
            count += 1
        else:
            result.append(current_char + str(count))
            current_char = s[i]
            count = 1
    
    result.append(current_char + str(count))
    compressed = ''.join(result)
    
    return compressed if len(compressed) < len(s) else s
```

### 3. Valid Anagrams
```python
def are_anagrams(s1, s2):
    # Using sorted strings
    return sorted(s1) == sorted(s2)

    # Using character count
    if len(s1) != len(s2):
        return False
        
    char_count = {}
    for c1, c2 in zip(s1, s2):
        char_count[c1] = char_count.get(c1, 0) + 1
        char_count[c2] = char_count.get(c2, 0) - 1
    
    return all(count == 0 for count in char_count.values())
```

## Time Complexity Analysis

Operation | Time Complexity | Space Complexity
----------|----------------|------------------
Access    | O(1)           | -
Search    | O(n)           | O(1)
Replace   | O(n)           | O(n)
Concatenate| O(n)          | O(n)
Split     | O(n)           | O(n)
Join      | O(n)           | O(n)
KMP Search| O(n + m)       | O(m)
Rabin-Karp| O(n + m)       | O(1)

## Best Practices

1. String Manipulation:
   - Use join() instead of + for concatenation
   - Consider using list for building strings
   - Be careful with string immutability
   - Use appropriate string methods

2. Performance Tips:
   - Avoid unnecessary string concatenations
   - Use string slicing carefully with large strings
   - Consider memory usage with large strings
   - Use appropriate algorithms for pattern matching

3. Interview Tips:
   - Always check for empty strings
   - Consider case sensitivity
   - Handle special characters appropriately
   - Think about space optimization
   - Test edge cases

4. Common Optimizations:
   - Use hash tables for character counting
   - Consider two-pointer technique
   - Use sliding window when applicable
   - Implement in-place modifications when possible
   - Use string builders for multiple concatenations
