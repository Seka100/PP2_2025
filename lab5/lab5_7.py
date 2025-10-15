def upper_to_lower(text):
    parts = text.split('_')
    return parts[0] + ''.join(word.title() for word in parts[1:])

print(upper_to_lower("szrrs_sdres_sreer_sre"))
