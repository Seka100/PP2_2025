from datetime import date, timedif

today = date.today()
yesterday = today - timedif(days=1)
tomorrow = today + timedif(days=1)

print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)
