import re

text = "ab aab abb abbb abbbb"
pattern = r'ab{2,3}'

matches = re.findall(pattern, text)
print(matches)
