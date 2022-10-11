from array import array
from cProfile import label
from multiprocessing.dummy import current_process
from turtle import clear
from Utility import Util


lineList = []
labelLineList = []
labelList = []
fileWords = []
arrayR = []
arrayI = []
arrayJ = []
binSave = []
currentLine = 0

#checar os registradores para cada comando que tem 3 registradores como padrão
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

#checar os registradores e a constante sa
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

#checar os registradores e se tem label ou uma constante na operação
def registrarChecker3(array, index):
  destinations = []
  i = 0
  labelAddress = 0
  while array[index] != 'bk':
    for x in util.registers:
      if x == array[index]:
        x = x.replace("$", "")
        x = int(x)
        destinations.append(x) 
        immediate = array[index+1] 
    index += 1
  while (len(labelList) - 1) >= i:
    if labelList[i][0] == immediate:
      labelAddress = labelList[i][1]
      #calculando immediate quando se tem uma label na operação
      immediate = (labelAddress + 1) - currentLine - 1
      destinations.append(immediate)
      return destinations
    i+=1

  destinations.append(int(immediate))
  return destinations

#checando registradores LW e SW 
def registrarCheckerLW_SW(array, index):
  destinations = []

  while array[index] != 'bk':
    for x in util.registers:
      if x == array[index]:
        x = x.replace("$", "")
        x = int(x)
        destinations.append(x) 
        rsAddress = array[index+1]
    index += 1
  
  rsAddress = rsAddress.split('(')
  destinations.append(int(rsAddress[0])) 
  rsAddress = rsAddress[1].split('$')
  rsAddress = rsAddress[1].replace(')', "")
  destinations.append(int(rsAddress[0]))

  return destinations

#função que retorna a codificação de j e jal
def toJump(array, index):
  destinations = []
  i = 0

  while array[index] != 'bk':
    label = array[index]
    index += 1

  while (len(labelList) - 1) >= i:
    if labelList[i][0] == label:
      labelAddress = labelList[i][1]
      labelAddress = (0x00400000 + (labelAddress * 4))/4
      destinations.append(labelAddress)
      return destinations
    i+=1
  
#formata o binário para 32 bits  
def format32(bin):
    r = len(bin)
    a = 32 - r
    return ("0"*a)+bin

#caso o binário seja negativo irá precisar realizar a formatação de outra forma
def negativeBin(n, bits):
  s = bin(n & int("1"*bits, 2))[2:]

  return ("{0:0>%s}" %(bits)).format(s)

#faz um array da codificação para instruções do tipo R    
def TypeR(id, array, index):
  if array[index] == "mul":
    arrayR.append(28)
    destinations = registrarChecker(array, index)
    arrayR.append(destinations[1])
    arrayR.append(destinations[2])
    arrayR.append(destinations[0]) 
    arrayR.append(0)
    arrayR.append(id)
    #transforma em binário
    binValue = bin((arrayR[0] << 26 | arrayR[1] << 21 | arrayR[2] << 16 | arrayR[3] << 11 | arrayR[4] << 6 | arrayR[5]))
    binValue = format32(binValue[2:])
    binSave.append(binValue) #array de binário da codificação
    arrayR.clear()
    
  elif id == 0 or id == 2:
    arrayR.append(0)
    arrayR.append(0)
    destinations = registrarChecker2(array, index)
    arrayR.append(destinations[1])
    arrayR.append(destinations[0])
    arrayR.append(destinations[2])
    arrayR.append(id)
    binValue = bin((arrayR[0] << 26 | arrayR[1] << 21 | arrayR[2] << 16 | arrayR[3] << 11 | arrayR[4] << 6 | arrayR[5]))
    binValue = format32(binValue[2:])
    binSave.append(binValue)
    arrayR.clear()
  elif id == 8:
    arrayR.append(0)
    destinations = registrarChecker(array, index)
    arrayR.append(destinations[0])
    arrayR.append(0)
    arrayR.append(0)
    arrayR.append(0)
    arrayR.append(id)
    binValue = bin((arrayR[0] << 26 | arrayR[1] << 21 | arrayR[2] << 16 | arrayR[3] << 11 | arrayR[4] << 6 | arrayR[5]))
    binValue = format32(binValue[2:])
    binSave.append(binValue)
    arrayR.clear()
  elif id == 16 or id == 18:
    arrayR.append(0)
    arrayR.append(0)
    arrayR.append(0)
    destinations = registrarChecker(array, index)
    arrayR.append(destinations[0])
    arrayR.append(0)
    arrayR.append(id)
    binValue = bin((arrayR[0] << 26 | arrayR[1] << 21 | arrayR[2] << 16 | arrayR[3] << 11 | arrayR[4] << 6 | arrayR[5]))
    binValue = format32(binValue[2:])
    binSave.append(binValue)
    arrayR.clear()
  elif id == 24 or id == 25 or id == 26 or id == 27:
    arrayR.append(0)
    destinations = registrarChecker(array, index)
    arrayR.append(destinations[0])
    arrayR.append(destinations[1])
    arrayR.append(0)
    arrayR.append(0)
    arrayR.append(id)
    binValue = bin((arrayR[0] << 26 | arrayR[1] << 21 | arrayR[2] << 16 | arrayR[3] << 11 | arrayR[4] << 6 | arrayR[5]))
    binValue = format32(binValue[2:])
    binSave.append(binValue)
    arrayR.clear()

  else:
    arrayR.append(0)
    destinations = registrarChecker(array, index)
    arrayR.append(destinations[1])
    arrayR.append(destinations[2])
    arrayR.append(destinations[0]) 
    arrayR.append(0)
    arrayR.append(id)
    binValue = bin((arrayR[0] << 26 | arrayR[1] << 21 | arrayR[2] << 16 | arrayR[3] << 11 | arrayR[4] << 6 | arrayR[5]))
    binValue = format32(binValue[2:])
    binSave.append(binValue)
    arrayR.clear()

  
 #faz um array da codificação para instruções do tipo I 
def TypeI(id, array, index):
  if id == 4 or id == 5:
    destinations = registrarChecker3(array, index)
    arrayI.append(id)
    arrayI.append(destinations[0])
    arrayI.append(destinations[1])
    arrayI.append(destinations[2])
    arrayI[3] = negativeBin(arrayI[3], 16) #binário do número negativo em 16 bits
    binValue = bin((arrayI[0] << 26 | arrayI[1] << 21 | arrayI[2] << 16)) #binário do restante da codificação em 16 bits
    binValue = binValue[2:15]+ arrayI[3] #soma dos binários de 16 bits
    binValue = format32(binValue)
    binSave.append(binValue)
    arrayI.clear()

  elif id == 8 or id == 9 or id == 10 or id == 11 or id == 12 or id == 13:
    arrayI.append(id)
    destinations = registrarChecker3(array, index)
    arrayI.append(destinations[1])
    arrayI.append(destinations[0])
    arrayI.append(destinations[2])
    binValue = bin((arrayI[0] << 26 | arrayI[1] << 21 | arrayI[2] << 16 | arrayI[3]))
    binValue = format32(binValue[2:])
    binSave.append(binValue)
    arrayI.clear()
  elif id == 15:
    arrayI.append(id)
    arrayI.append(0)
    destinations = registrarChecker3(array, index)
    arrayI.append(destinations[0])
    arrayI.append(destinations[1])
    binValue = bin((arrayI[0] << 26 | arrayI[1] << 21 | arrayI[2] << 16 | arrayI[3]))
    binValue = format32(binValue[2:])
    binSave.append(binValue)
    arrayI.clear()
  elif id == 35 or id == 43:
    arrayI.append(id) 
    destinations = registrarCheckerLW_SW(array, index)
    arrayI.append(destinations[2])
    arrayI.append(destinations[0])
    arrayI.append(destinations[1])
    binValue = bin((arrayI[0] << 26 | arrayI[1] << 21 | arrayI[2] << 16 | arrayI[3]))
    binValue = format32(binValue[2:])
    binSave.append(binValue)
    arrayI.clear()

#faz um array da codificação para instruções do tipo J
def TypeJ(id, array, index):
   arrayJ.append(id)
   destinations = toJump(array, index)
   arrayJ.append(destinations[0])
   binValue = bin((arrayJ[0] << 26 | int(arrayJ[1])))
   binValue = format32(binValue[2:])
   binSave.append(binValue)
   arrayJ.clear()
   

if __name__ == '__main__':  
  util = Util()
  L = 0
  #faz a primeira leitura do meu arquivo identificando a label e em qual endereço ela se encontra
  fileName = input("Nome do arquivo .asm: ")
  fileContent = open(fileName, 'r')
  for index, line in enumerate(fileContent):
    for word in line.split():
      word = word.replace(",", "")
      fileWords.append(word)
      for i in range(len(word)):
        if word[i] == ":":
          word = word.replace(":", "")
          labelList.append([word, L])
    L+= 1
    fileWords.append("bk")
  
  #checa qual o tipo de operação e chama a função do tipo que  ela pertence
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
      TypeJ(2, fileWords, index)
    elif x == "jal":
      currentLine += 1
      TypeJ(3, fileWords, index)

  #cria e escreve o arquivo binário                
  binaryFile = open("binResponse.bin", "w")
  for line in binSave:
    binaryFile.write(line + "\n") 
  binaryFile.close()


               
      




   

