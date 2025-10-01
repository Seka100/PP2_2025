def grams_to_ounces(grams):
    return 28.3495231 * grams

def is_palindrome(s):
    s = s.lower().replace(" ", "")
    return s == s[::-1]

def unique_elements(lst):
    result = []
    for item in lst:
        if item not in result:
            result.append(item)
    return result
