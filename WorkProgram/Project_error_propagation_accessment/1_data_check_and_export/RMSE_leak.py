import os
import copy

path = r'D:\Works\backup\Project01_ErrorEstimate_DRM_on_Ni111\1_ouput_data/range-RMSE.txt'
with open(path,encoding = 'utf8') as f:
    data = f.readlines()

work = {}
for i in data:
    i = '(' + i
    i = i.replace('\n','').replace('_',',').replace('eV',')')
    i = i.split('\t')
    try:
        work[eval(i[0] + ')')].extend([eval(i[1])])
    except KeyError:
        work[eval(i[0] + ')')] = [eval(i[1])]

count = {}
for i in work.keys():
    for j in work[i]:
        if j > i[1] or j < i[0]:
            try:
                count[i] += 1
            except KeyError:
                count[i] = 0

print(count)



