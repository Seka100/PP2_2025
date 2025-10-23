name = input("File name: ")

n = open(name, 'r')
count = 0

for i in n:
    count += 1

n.close()

print("количество:", count)
