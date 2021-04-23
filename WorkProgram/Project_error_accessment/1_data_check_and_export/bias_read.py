import ordered_bias2

bias2 = ordered_bias2.bias2

work = []
length = 2000
div = len(bias2)//length

for i in range(div):
    work.append([])

position = 1
while position != div+1:
    for j in range(((position-1)*length), position*length):
        work[position-1].append(bias2[j])
    position += 1

# for i in work[1]:
#   print(i)

for i in range(2000):
    print(str(work[0][i]) + ',' + str(work[1][i])   + ',' + str(work[2][i]) + ',' + str(work[3][i]) + ',' + str(work[4][i]) + ',' + str(work[5][i]) + ',' + str(work[6][i]) + ',' + str(work[7][i]) + ',' + str(work[8][i]) + ',' + str(work[9][i]) + ',')
