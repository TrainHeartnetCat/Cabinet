import os

# 请按实际需求修改内容
# 展示xx, xx, xx形式txt中的所有xx，并写成一个tuple
# 可以根据需求增加展示内容
target_txt = ''

with open(target_txt, encoding = 'utf8') as f:
	all_species = f.readlines()


all_species_list = []
for item in all_species:
	item = item.replace('*','')
	a = item.split(',')
	if '' in a:
		a.remove('')
	for i in a:
		i = i.strip()
		all_species_list.append(i)

for i in all_species_list:
	print(i + '_111')

print(tuple(all_species_list))