import os

# 主要两个功能，可以理解为正向操作，反向操作
# 可以从制作好的数据txt，提取物种和对应属性，并按generate_input中的形式print出来，方便复制黏贴
# 可以从energy.txt中读取数据，制作成{'species':property}，并按generate_input中的形式print出来，方便复制黏贴

# 功能一
energy_property_path = 'species_and_energy.txt'

with open(energy_property_path, encoding = 'utf-8') as f:
    content = f.readlines()

energy_property_dic = {}
# 由于txt内容是由excel导出，因此分割符号是\t，而不是空格
for i in content:
    i = i.replace('\n','')
    if i == '':
        continue
    else:
        i = i.split('\t')
        energy_property_dic[i[0]] = i[1]

print('There is ' + str(len(energy_property_dic.keys())) + ' species here, please check whether it is matched with source data!')
print('')

for gas in energy_property_dic.keys():
    if '_gas' in gas:
        print("'" + gas + "'" + ":" + energy_property_dic[gas] + ',')

print('')
for state in energy_property_dic.keys():
    if 'slab' in state:
        continue
    else:
        if '_111' in state:
            print("'" + state + "'" + ":" + energy_property_dic[state] + ',')

print('')
for slab in energy_property_dic.keys():
    if 'slab' in slab:
        print("'" + slab + "'" + ":" + energy_property_dic[slab] + ',')