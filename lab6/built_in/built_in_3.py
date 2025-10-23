s = input("enter: ")

c= ''.join(s.split()).lower()

palindrome = c== c[::-1]

print("palindrome:", palindrome)
