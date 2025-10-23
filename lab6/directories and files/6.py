for c in range(65, 91):  
    filename = chr(c) + ".txt"
    n = open(filename, 'w')
    n.close()

print("created")
