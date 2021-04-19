import os

# 输入字符串都是简化后的化学式，并非结构式
print('warning: please use chemical formula')

# 请使用python3
# ************************请设置以下参数************************
# 请输入需要修改的原子与原子个数
change_table = {'C':12, 'H':9, 'N':3, 'O':3}
# 请输入需要添加的原子与个数（原本不存在）(在末尾添加)。若无则设置insert_table = {}
insert_table = {'O':3}
# 请输入文件路径，暂时只支持txt
# TODO 加一个excel的（xls，xlsx）
data_path = r'C:\Users\OldKuroCat\Desktop\group2020/Amine.xlsx'
# 请输入输出文件路径，暂时采用直接复制输出的形式，因此不需要使用
output_path = r''
# 请输入输出文件类型，暂时只支持txt
# 使用txt模式时，可以直接获得输出结果，且不会生成输出文件
# 使用xls或者xlsx模式时，请在output_path下取得输出文件
# TODO 加一个excel的（xlsx）
output_type = '.xlsx'
# ************************请设置以上参数************************


# 问题
# 1. 里头一个带*的过渡态



if os.path.splitext(data_path)[1] == '.txt':
    with open(data_path) as f:
        content = f.readlines()

    worklist = []
    for i in content:
        a = i.replace('\n','')
        worklist.append(a)

# 在找到目标原子后有三种可能：第二位直接是别的原子，也即原子数为1；第二位开始是数字；第二位是小写字母，也即是双字母原子
    final_list = []
    for molecular in worklist:
        if '*' in molecular:
            molecular = molecular.replace('*','')
            Transition = 1
        else:
            Transition = 0
        new_molecular = molecular
        for element in change_table:
            target_position = molecular.find(element)# 目标原子字符位置
            if target_position == -1:# 不存在该原子，跳过
                continue
            else:
                next_position = target_position + 1# 下一位字符
                try:
                    if molecular[next_position].isupper() == False:# 判断后一位字符是否是大写字母（另一种原子），若不是，则只可能数字或者小写的双字母原子。如果是过渡态有-，还不能处理。
                        try:
                            if type(eval(molecular[next_position])) == int:# 是数字，统计有几位数字
                                count = 1
                                final_position = next_position
                                try:
                                    while type(eval(molecular[target_position+count])) == int:
                                        count += 1
                                except NameError:
                                    final_position = target_position + count - 1
                                    element_num = eval(molecular[target_position+1:final_position+1])
                                except IndexError:# 以防目标原子是最后一位原子
                                    final_position = target_position + count - 1
                                    element_num = eval(molecular[target_position+1:final_position+1])
                        except NameError:# 双字母原子跳过，不是目标原子
                            continue
                    if molecular[next_position].isupper() == True:# 目标原子后面直接是别的原子，也即原子数为1
                        final_position = target_position
                        element_num = 1
                except IndexError:# 以防target位置就是最后一位
                    final_position = target_position
                    element_num = 1
            target_piece = molecular[target_position:final_position+1]
            new_piece = element + str(change_table[element] + element_num)
            new_molecular = new_molecular.replace(target_piece,new_piece)
        if insert_table == {}:
            continue
        else:
            for insert_element in insert_table:
                if insert_element in molecular:
                    continue
                else:
                    if insert_table[insert_element] == 1:
                        new_molecular = new_molecular + insert_element
                    else:
                        new_molecular = new_molecular + insert_element + str(insert_table[insert_element])
        if Transition == 1:
            new_molecular = new_molecular + '*'
        final_list.append(new_molecular)
        print(new_molecular)
    print('There are ' + str(len(final_list)) + ' molecules!')


if os.path.splitext(data_path)[1] == '.xls' or os.path.splitext(data_path)[1] == '.xlsx':
	import xlrd
	import xlwt

	data = xlrd.open_workbook(data_path)
	table = data.sheet_by_name('Sheet1')



