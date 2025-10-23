def count(s):
    upper = 0
    lower = 0

    for ch in s:
        if ch.isupper():
            upper += 1
        elif ch.islower():
            lower += 1

    print("upper:", upper)
    print("lower:", lower)

text = input("enter: ")
count(text)
