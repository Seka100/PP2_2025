m = ['Palmer', 'Neto', 'Caicedo']

n = open('file.txt', 'w')

for i in m:
    n.write(i + '\n')

n.close()

print("Saved!")

