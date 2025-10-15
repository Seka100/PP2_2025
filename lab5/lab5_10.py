import re

def upper_to_lower(text):
    text = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', text)
    return text.lower()

print(upper_to_lower("thisisSerikSapakov"))
