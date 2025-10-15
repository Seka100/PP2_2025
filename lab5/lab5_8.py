import re

text = "ColePalmerBestPlayerInPremierLeague"
pattern = r'(?=[A-Z])'

result = re.split(pattern, text)
print(result)
