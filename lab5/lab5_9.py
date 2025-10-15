import re

text = "KylianMbappeBestStriker"
result = re.sub(r'(?=[A-Z])', ' ', text).strip()
print(result)
