
from array import array
from cProfile import label
from multiprocessing.dummy import current_process
from Utility import Util
from bitarray import bitarray


lineList = []
labelLineList = []
labelList = []
fileRows = []
fileWords = []
arrayR = []
arrayI = []
currentLine = 0

def registrarChecker(array, index):
  destinations = []
  while array[index] != 'bk':
      for x in util.registers:
        if x == array[index]:
          x = x.replace("$", "")
          x = int(x)
          destinations.append(x)  
      index += 1
  return destinations

def registrarChecker2(array, index):
  destinations = []
  while array[index] != 'bk':
      for x in util.registers:
        if x == array[index]:
          x = x.replace("$", "")
          x = int(x)
          destinations.append(x) 
          sa = array[index+1] 
      index += 1
  destinations.append(int(sa))
  return destinations 

def registrarChecker3(array, index):
  destinations = []
  i = 0
  labelAddress = 0
  while array[index] != 'bk':
    for x in util.registers:
      print(array[index])
      if x == array[index]:
        x = x.replace("$", "")
        x = int(x)
        destinations.append(x) 
        immediate = array[index+1] 
    index += 1
  while (len(labelList) - 1) >= i:
    print(immediate)
    print(labelList[i][0])
    if labelList[i][0] == immediate:
      labelAddress = labelList[i][1]
      print('currentLine', currentLine)
      print('labelAddress', labelAddress)
      immediate = labelAddress - currentLine - 1
      destinations.append(immediate)
      return destinations
    i+=1

  destinations.append(int(immediate))
  return destinations
   
  
    
def TypeR(id, array, index):
  
  if array[index] == "mul":
    arrayR.append(28)
    destinations = registrarChecker(array, index)
    arrayR.append(destinations[1])
    arrayR.append(destinations[2])
    arrayR.append(destinations[0]) 
    arrayR.append(0)
    arrayR.append(id)
  elif id == 0 or id == 2:
    arrayR.append(0)
    destinations = registrarChecker2(array, index)
    arrayR.append(destinations[1])
    arrayR.append(0)
    arrayR.append(destinations[0])
    arrayR.append(destinations[2])
    arrayR.append(id)
  elif id == 8:
    arrayR.append(0)
    destinations = registrarChecker(array, index)
    arrayR.append(destinations[0])
    arrayR.append(0)
    arrayR.append(0)
    arrayR.append(0)
    arrayR.append(id)
  elif id == 16 or id == 18:
    arrayR.append(0)
    arrayR.append(0)
    arrayR.append(0)
    destinations = registrarChecker(array, index)
    arrayR.append(destinations[0])
    arrayR.append(0)
    arrayR.append(id)
  elif id == 24 or id == 25 or id == 26 or id == 27:
    arrayR.append(0)
    destinations = registrarChecker(array, index)
    arrayR.append(destinations[0])
    arrayR.append(destinations[1])
    arrayR.append(0)
    arrayR.append(0)
    arrayR.append(id)

  else:
    arrayR.append(0)
    destinations = registrarChecker(array, index)
    print(destinations)
    arrayR.append(destinations[1])
    arrayR.append(destinations[2])
    arrayR.append(destinations[0]) 
    arrayR.append(0)
    arrayR.append(id)
  

  
  
def TypeI(id, array, index):
  if id == 4 or id == 5:
    destinations = registrarChecker3(array, index)
    arrayI.append(id)
    arrayI.append(destinations[0])
    arrayI.append(destinations[1])
    arrayI.append(destinations[2])
    print(arrayI)

def Typej(id, array, index):
  print("aq")  

if __name__ == '__main__':  
  util = Util()
  L = 0
  fileName = input("Nome do arquivo .asm: ")
  fileContent = open(fileName, 'r')
  for index, line in enumerate(fileContent):
    fileRows.append(line)
    for word in line.split():
      word = word.replace(",", "")
      fileWords.append(word)
      for i in range(len(word)):
        if word[i] == ":":
          word = word.replace(":", "")
          labelList.append([word, L])
    L+= 1
    fileWords.append("bk")
  
    
  print(labelList[1][0])
  
  for index, x in enumerate(fileWords):
    if x == "add":
      currentLine += 1
      TypeR(32, fileWords, index)
    elif x == "sll":
      currentLine += 1
      TypeR(0, fileWords, index)
    elif x == "srl":
      currentLine += 1
      TypeR(2, fileWords, index)
    elif x == "jr":
      currentLine += 1
      TypeR(8, fileWords, index)
    elif x == "mfhi":
      currentLine += 1
      TypeR(16, fileWords, index)
    elif x == "mflo":
      currentLine += 1
      TypeR(18, fileWords, index)
    elif x == "mult":
      currentLine += 1
      TypeR(24, fileWords, index)
    elif x == "multu":
      currentLine += 1
      TypeR(25, fileWords, index)
    elif x == "div":
      currentLine += 1
      TypeR(26, fileWords, index)    
    elif x == "divu":
      currentLine += 1
      TypeR(27, fileWords, index)
    elif x == "addu":
      currentLine += 1
      TypeR(33, fileWords, index)   
    elif x == "sub":
      currentLine += 1
      TypeR(34, fileWords, index)
    elif x == "subu":
      currentLine += 1
      TypeR(35, fileWords, index) 
    elif x == "and":
      currentLine += 1
      TypeR(36, fileWords, index)
    elif x == "or":
      currentLine += 1
      TypeR(37, fileWords, index) 
    elif x == "slt":
      currentLine += 1
      TypeR(42, fileWords, index)  
    elif x == "sltu":
      currentLine += 1
      TypeR(43, fileWords, index)   
    elif x == "mul":
      currentLine += 1
      TypeR(2, fileWords, index) 
    elif x == "beq":
      currentLine += 1
      TypeI(4, fileWords, index)  
    elif x == "bne":
      currentLine += 1
      TypeI(5, fileWords, index) 
    elif x == "addi":
      currentLine += 1
      TypeI(8, fileWords, index)   
    elif x == "addiu":
      currentLine += 1
      TypeI(9, fileWords, index)
    elif x == "slti":
      currentLine += 1
      TypeI(10, fileWords, index)
    elif x == "andi":
      currentLine += 1
      TypeI(12, fileWords, index)  
    elif x == "ori":
      currentLine += 1
      TypeI(13, fileWords, index)     
    elif x == "lui":
      currentLine += 1
      TypeI(15, fileWords, index)
    elif x == "lw":
      currentLine += 1
      TypeI(35, fileWords, index)  
    elif x == "sw":
      currentLine += 1
      TypeI(43, fileWords, index)
    elif x == "j":
      currentLine += 1
      Typej(2, fileWords, index)
    elif x == "jal":
      currentLine += 1
      Typej(3, fileWords, index)
                   
        


               
      




   

