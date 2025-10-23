import os

a = input("enter: ")

n = os.listdir(a)

dirs = []
files = []

for i in n:
    full = os.path.join(a, i)
    if os.path.isdir(full):
        dirs.append(i)
    elif os.path.isfile(full):
        files.append(i)

print("directories:", dirs)
print("files:", files)
print("all:", n)
