from functools import reduce

nums = input("enter numbers: ")

num_list = list(map(int, nums.split()))

result = reduce(lambda x, y: x * y, num_list)

print("multiplication of all numbers:", result)
