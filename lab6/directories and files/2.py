import os

a = input("enter : ")

print("path exists:", os.path.exists(a))
print("can read:", os.access(a, os.R_OK))
print("can write:", os.access(a, os.W_OK))
print("can run:", os.access(a, os.X_OK))

