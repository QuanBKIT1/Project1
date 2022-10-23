f = open('test_label.txt','r')
line = f.readline()
l = line.split(' ')
a = []
for i in range(len(l)-1):
    a.append(int(l[i]))
acc = 0
for i in range(50):
    for k in range(3):
        if a[i+k*50] == k:
            acc += 1

print(acc/150)
