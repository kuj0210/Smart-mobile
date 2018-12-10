
listA = [1,1]
listB = [1,1]
listC = [1,0]

print(listA[1]==listB[1])
print(listA[1]==listC[1])

res=[]
res.append(listA[1]==listB[1])
res.append(listA[1]==listC[1])
print(res)