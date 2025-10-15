import re

text = "acb,axyzb ab a123b"
pattern = r'a.*b'

matches = re.findall(pattern, text)
print(matches)
