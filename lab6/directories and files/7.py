file1 = input("from: ")
file2 = input("to: ")

f1 = open(file1, 'r')
f2 = open(file2, 'w')

f2.write(f1.read())

f1.close()
f2.close()

print("copied")
