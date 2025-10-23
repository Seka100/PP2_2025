import time
import math

num = int(input())
ms = int(input())

time.sleep(ms / 1000)

result=math.sqrt(num)

print(f"Sqrt of {num} after {ms} miliseconds is {result}")
