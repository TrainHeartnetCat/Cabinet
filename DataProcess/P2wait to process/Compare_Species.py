import os

# 查缺补漏比较数据库导出的物种与已知目标物种
# 需要把物种做成txt，一行一个物种
# 如果物种有特定格式，比如表示吸附态的*，则需要对脚本进行一定修改，默认情况下两批物种格式需要相同
# 最后结果分开展示批次1中缺少的物种(对于批次2)，批次2中缺少的物种(对于批次1)
# 要放到txt所在文件夹下运行

# 由于fpaper是作为所需物种的标准，因此要确定fpaper中物种一定是自己所需物种，没有缺少，也没有多出来
# 如果fdatabase出现losts，说明有需要的物种在数据库中没有
# 不能依靠fpaper的losts作为物种缺失的检查，其losts只能反应出数据库有的，但fpaper中没有的（可能是因为不需要，也可能是因为fpaper没检查好导致缺失）
# 最后根据losts的提示，对数据库导出的结果进行修改，使用之即可

# 已知目标物种
target_txt_1 = 'fpaper.txt'
# 数据库物种
target_txt_2 = 'fdatabase.txt'
# target_txt_2 = 'fdatabase_Pt111SRE.txt'
# target_txt_2 = 'fdatabase_Pd111SRE.txt'


with open(target_txt_1, encoding = 'utf-8') as f:
	content1 = f.readlines()

new1 = []
for i in content1:
	i = i.replace('\n','')
	if i == '':
		pass
	else:
		new1.append(i)


with open(target_txt_2, encoding = 'utf-8') as f:
	content2 = f.readlines()

new2 = []
for i in content2:
	i = i.replace('\n','')
	if i == '':
		pass
	else:
		new2.append(i)

print(target_txt_1 + ' has ' + str(len(new1)) + ' species!')
print(target_txt_2 + ' has ' + str(len(new2)) + ' species!')

# 已知目标物种中没有的物种
print('')
print('')
print(target_txt_1 + ' losts:')
for i in new2:
	if i not in new1:
		print(i)

# 数据库导出物种中缺少的物种
print('')
print('')
print(target_txt_2 + ' losts:')
for i in new1:
	if i not in new2:
		print(i)
print('')
print('--------------------------------------keep-out------------------------------------')
print("if species number doesn't match with losts, there might be repetitions.")

print('')
print('Repetitions in ' + target_txt_2 + '. Blank means no repetitions')
for i in range(len(new2)):
	for j in range(len(new2)):
		if i == j:
			continue
		else:
			if new2[i] == new2[j]:
				print('line: ' + i + ' species name: ' + new2[i])