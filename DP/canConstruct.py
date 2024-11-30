from typing import List, Dict

def can_construct(target: str, word_bank: List[str], memo: Dict[str, bool] = None) -> bool:
    """
    Determines if the `target` string can be constructed by concatenating 
    elements of the `word_bank` array. Words in `word_bank` can be reused 
    as many times as needed.
    
    This function uses memoization to optimize repeated computations.

    Args:
        target (str): The string we want to construct.
        word_bank (List[str]): List of strings available for constructing the target.
        memo (Dict[str, bool], optional): A dictionary used for memoization to store 
                                           already computed results for subproblems.
                                           Defaults to None.

    Returns:
        bool: True if the `target` can be constructed from `word_bank`, False otherwise.

    Examples:
        >>> can_construct("abcdef", ["ab", "abc", "cd", "def", "abcd"])
        True
        >>> can_construct("skateboard", ["bo", "rd", "ate", "t", "ska", "sk", "boar"])
        False
        >>> can_construct("", ["cat", "dog", "mouse"])
        True
    """
    if memo is None:
        memo = {}
    
    # Check if the result is already computed
    if target in memo:
        return memo[target]
    
    # Base case: If the target is an empty string, it can be constructed
    if target == '':
        return True
    
    # Try each word in the word bank
    for word in word_bank:
        # Check if the target starts with the current word
        if target.startswith(word):
            suffix = target[len(word):]  # Remove the prefix
            # Recursively check if the suffix can be constructed
            if can_construct(suffix, word_bank, memo):
                memo[target] = True  # Store the result in the memo
                return True
    
    # If no solution is found, store the result as False
    memo[target] = False
    return False

# Example usage:
print(can_construct("abcdef", ["ab", "abc", "cd", "def", "abcd"]))  # True
print(can_construct("skateboard", ["bo", "rd", "ate", "t",
