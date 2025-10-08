from datetime import datetime

now = datetime.now()

no_microseconds = now.replace(microsecond=0)

print("Original datetime:", now)
print("Without microseconds:", no_microseconds)
