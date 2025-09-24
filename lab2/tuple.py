thistuple = ("apple", "banana", "cherry")
print(thistuple)

tuple1 = ("abc", 34, True, 40, "male")

tuple2= ("apple", "banana", "cherry")
y = list(tuple2)
y.append("orange")
tuple2 = tuple(y)


fruits = ("apple", "mango", "papaya", "pineapple", "cherry")

(green, *tropic, red) = fruits

print(green)
print(tropic)
print(red)


thistuple = ("apple", "banana", "cherry")
for i in range(len(thistuple)):
  print(thistuple[i])


  
