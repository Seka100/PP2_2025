import re

text = "ab abb a abbb acb"
pattern = r'ab*'

matches = re.findall(pattern, text)
print(matches)
