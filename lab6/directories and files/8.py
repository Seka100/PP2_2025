import os

a = input("enter : ")

if os.path.exists(a):
    if os.access(a, os.W_OK):
        os.remove(a)
        print("deleted")
    else:
        print("cannot delete")
else:
    print("not found.")
