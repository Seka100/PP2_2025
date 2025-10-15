import re

text = "Chelsea Is THE best Club In The World"
pattern = r'[A-Z][a-z]+'

matches = re.findall(pattern, text)
print(matches)
