import re

text = "Python. Serik ,Sapakov"
pattern = r'[ ,.]'

result = re.sub(pattern, ":", text)
print(result)
