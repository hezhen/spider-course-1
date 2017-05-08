from simhash import Simhash

f = open('sample_doc_1.txt', 'rb')
str1 = f.read()
f.close()

f = open('sample_doc_2.txt', 'rb')
str2 = f.read()
f.close()

sh0 = Simhash(str1.decode('utf-8'))
sh1 = Simhash(str2.decode('utf-8'))

print bin(sh0.value)
print bin(sh1.value)

print sh0.distance(sh1)