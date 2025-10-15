import re

text = "srsers_swraaw_ewarara_se"
pattern = r'[a-z]+_[a-z]+'

matches = re.findall(pattern, text)
print(matches)
