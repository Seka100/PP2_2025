n = input("enter: ")

m = tuple(map(int, n.split()))

print("true:", all(m))
