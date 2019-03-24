
import random as rnd

seedarray = ["A","B","C","D","E","F","G","H","I","J","K"]
rnd.randrange(0,4)

goalarray = []
temparray = []
temparray.append(seedarray[0])
goalarray.append(temparray)

for n in range(1,10):
    for x in range((2**(n-1))-1,(2**n)-1):
        original = goalarray[x]
        modifier = [seedarray[n]]
        prestr=original+modifier
        poststr=modifier+original
        goalarray.append(prestr)
        goalarray.append(poststr)
for y in goalarray:
    print y


