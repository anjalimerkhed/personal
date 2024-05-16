def is_palindrome(string):
    # Convert the string to lowercase for case-insensitive comparison
    string = string.lower()
    
    # Initialize pointers for the beginning and end of the string
    start = 0
    end = len(string) - 1
    
    # Continue until the pointers meet or cross each other
    while start < end:
        # Ignore non-alphanumeric characters from the beginning
        if not string[start].isalnum():
            start += 1
            continue
        
        # Ignore non-alphanumeric characters from the end
        if not string[end].isalnum():
            end -= 1
            continue
        
        # Compare characters at the current positions
        if string[start] != string[end]:
            return False
        
        # Move pointers towards each other
        start += 1
        end -= 1
    
    # If the loop completes without returning False, the string is a palindrome
    return True

# Test the function
print(is_palindrome("MADAM"))  # Output: True
