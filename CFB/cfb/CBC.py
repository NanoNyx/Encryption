import array
pt = raw_input("Введіть повідомлення: ")
size = 3 #Block size for CBC mode
print ('Розмір блока: ',size)
count=size-len(str(pt))%size
p=""
if count != size:
    for i in range(0,count):
        p+='x'

pt = pt+p
IV=["a","b","c"]

temp=["a","b","c"]

print ("Введення з пробілами відповідно до розміру блоку: ",pt)
key = input("Введіть ключ для шифрування: ")
NumPT=[]
for i in range(0, len(pt)):
    NumPT.append(0)
for j in range(0,len(pt)):
    NumPT[j] = (ord(pt[j])-97)

def shift_encryption(key,low,high):
    for i in range (low,high):
        NumPT[i]= (ord(IV[i-low])-97)^(NumPT[i])
        NumPT[i]= (NumPT[i]+ord(key) -48 +26)%26
        IV[i-low]=chr(NumPT[i]+97)
        print chr(NumPT[i]+97),

def shift_decryption(key,low,high):
    for i in range(low,high):
        temp[i-low]=chr(NumPT[i]+97)
        NumPT[i]= (NumPT[i] - (ord(key) -48) +26)%26
        NumPT[i]=(ord(IV[i-low])-97)^(NumPT[i])
        IV[i-low]=temp[i-low]
        print chr(NumPT[i]+97),

print ("Зашифрований текст має вигляд: ")
for i in range(0,len(pt),size):
    shift_encryption(str(key),i,i+size)
print ("")

IV=["a","b","c"]

print ("Розшифрований текст має вигляд: ")
for i in range(0,len(pt),size):
    shift_decryption(str(key),i,i+size)
print ("")
