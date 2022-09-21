
from array import array
from cProfile import label
from Utility import Util
from bitarray import bitarray


lineList = []
labelLineList = {}
labelList = []
fileRows = []
fileWords = []
arrayR = []

def TypeR(id, array, index):
  if id == 2:
    arrayR.append([0, 1, 1, 1, 0, 0 ])
  else:
    arrayR.append([0, 0, 0, 0, 0, 0 ])

  i=0
  
 #Adiciona todos os zeros que faltarem  
  def format32(bin):
    r = len(bin)
    a = 32 - r
    return ("0"*a)+bin

#chamada, passando para a função e tirando o 0b que fica aparecendo
  format32(arrayR[2:])
  format32(arrayR[2:])
      


def TypeI(id, array, index):
  print("aq")
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
      fileWords.append(word)
      for i in range(len(word)):
        if word[i] == ":": 
          labelList.append(word)
          labelLineList[word] = [L] 
    L+= 1
    fileWords.append("bk")
    
  print(fileWords)
  for index, x in enumerate(fileWords):
    if x == "add":
      TypeR(32, fileWords, index)
    elif x == "sll":
      TypeR(0, fileWords, index)
    elif x == "srl":
      TypeR(2, fileWords, index)
    elif x == "jr":
      TypeR(8, fileWords, index)
    elif x == "mfhi":
      TypeR(16, fileWords, index)
    elif x == "mflo":
      TypeR(18, fileWords, index)
    elif x == "mult":
      TypeR(24, fileWords, index)
    elif x == "multu":
      TypeR(25, fileWords, index)
    elif x == "div":
      TypeR(26, fileWords, index)    
    elif x == "divu":
      TypeR(27, fileWords, index)
    elif x == "addu":
      TypeR(33, fileWords, index)   
    elif x == "sub":
      TypeR(34, fileWords, index)
    elif x == "subu":
      TypeR(35, fileWords, index) 
    elif x == "and":
      TypeR(36, fileWords, index)
    elif x == "or":
      TypeR(37, fileWords, index) 
    elif x == "slt":
      TypeR(42, fileWords, index)  
    elif x == "sltu":
      TypeR(43, fileWords, index)   
    elif x == "mul":
      TypeR(2, fileWords, index) 
    elif x == "beq":
      TypeI(4, fileWords, index)  
    elif x == "bne":
      TypeI(5, fileWords, index) 
    elif x == "addi":
      TypeI(8, fileWords, index)   
    elif x == "addiu":
      TypeI(9, fileWords, index)
    elif x == "slti":
      TypeI(10, fileWords, index)
    elif x == "andi":
      TypeI(12, fileWords, index)  
    elif x == "ori":
      TypeI(13, fileWords, index)     
    elif x == "lui":
      TypeI(15, fileWords, index)
    elif x == "lw":
      TypeI(35, fileWords, index)  
    elif x == "sw":
      TypeI(43, fileWords, index)
    elif x == "j":
      Typej(2, fileWords, index)
    elif x == "jal":
      Typej(3, fileWords, index)
                   
        


               
      




   

