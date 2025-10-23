import os

a = input("enter : ")

if os.path.exists(a):
    print("exists")
    print("folder:", os.path.dirname(a))
    print("file:", os.path.basename(a))
else:
    print("doesn't exist")
