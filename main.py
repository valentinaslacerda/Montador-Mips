from cProfile import label
labelLineList = {}
labelList = []
L = 0
fileName = input("Nome do arquivo .asm: ")

fileName = open(fileName, 'r')

for line in fileName: 
  L+= 1
  for word in line.split(): 
    for i in range(len(word)):
      if word[i] == ":": 
        labelList.append(word)
        labelLineList[word] = [L] 

print(labelLineList)