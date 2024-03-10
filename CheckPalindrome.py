import StringReverse


def CheckPalindrome(string):
    if len(string)%2 == 0:
        n = int(len(string)  / 2)
    else:
        n = int((len(string) - 1) / 2)
    left = ""
    right = ""
    for i in range(0, n):
        left += string[i]
    
    for i in range(1, n+1):
        right += string[-i]
    
    if left == right:
        return True
    else:
        return False


def CheckPalindromeAlt(string):
    if string == StringReverse.ReverseStringIteration(string):
        return True
    else:
        return False
    

if __name__ == "__main__":
    palindromes = ["level", "madam", "radar", "deified", "racecar", "rotator", "redder", "noon", "civic", "refer", "repaper"]
    non_palindromes = ["hello", "world", "python", "programming", "algorithm", "openai", "machine", "learning", "palindrome", "reverse", "example"]
    
    for string in palindromes:
        print("Should be True, is: " + str(CheckPalindromeAlt(string)))
    
    for string in non_palindromes:
        print("Should be False, is: " + str(CheckPalindromeAlt(string)))
        