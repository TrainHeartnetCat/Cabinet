# coding:utf-8
# 请用python2.7
# 从running_result文件夹中，获取不同温度，不同RMSE文件夹中的coverage，DRC，path，rate文件夹中提取数据，加上对应RMSE的能量
# 输出结果并存储成pkl文件。
# Key: (t,RMSE_low,RMSE_high)
# Value: [[energy],[path],[drc],[coverage],[rate]]
# energy: 能量的字典，key为序号，value为能量list。使用energy_extraction函数获取
# coverage: 覆盖度的字典，key为物种，value为数量。使用coverage_extraction函数获取
# DRC: DRC的字典，key为速率步骤， value为数量。使用DRC_extraction函数获取
# path: hash值与路径的字典，key为hash，value为数量。使用path_extraction函数获取
# rate: rate的array。


import os
import pickle
import json
import numpy as np
import xlrd


print('Please run in python2.7')

# dic_outputpkl = {(t, low, high):[{order:[energy]}, {'species':number}, {'species':number}, {hash:number}, array([mpf])]. ...}

output_path = "./"# change

tmp = [923]# change
# tmp = [823, 873]
RMSE = [(0.1, 0.12), (0.12, 0.14), (0.14, 0.16), (0.16, 0.18), (0.18, 0.2), (0.2, 0.22), (0.22, 0.24), (0.24, 0.26), (0.26, 0.28), (0.28, 0.3)]# change
size = '3000sizeN1'
tee = '923'
# RMSE = [(0.1, 0.12), (0.12, 0.14)]
collection_dic = {}

for t in tmp:
    for i in RMSE:
        working_path = []
        RMSE_low = i[0]
        RMSE_high = i[1]
        key = (t, RMSE_low, RMSE_high)
        energyfile_path = 'D:\\Works\\backup\\Project01_ErrorEstimate_DRM_on_Ni111\\0_raw_data\\All_error_simulated_formation_energy_on_Ni\\raw_txt\\3000sizeN\\output_RMSE_%s_%s_%s' % (RMSE_low, RMSE_high, size)# energy的路径
        analysis_path = 'D:\\Works\\backup\\Project01_ErrorEstimate_DRM_on_Ni111\\1_ouput_data\\Raw_output\\size3000N\\%s\\1\\RMSE_%s_%s_%s' % (t, RMSE_low, RMSE_high, size)
        coverageanal = analysis_path + '\\1_coverage\\print_out'#找count在的最后一行
        drcanal = analysis_path + '\\1_DRC\\DRC_results_positive.xls'#找excel数据
        pathanal = analysis_path + '\\1_path\\print_out'#找两个字典
        rateanal = analysis_path + '\\1_rate\\rx_rate_collection_result.pkl'#直接用
        working_path.append(energyfile_path)
        working_path.append(coverageanal)
        working_path.append(drcanal)
        working_path.append(pathanal)
        working_path.append(rateanal)
        collection_dic[key] = working_path


def energy_extraction(dic_path):#从一个文件夹下的txt中获得能量，并返回一个文件编号对应能量list的dic
    dic = {}
    items = os.listdir(dic_path)
    for i in items:
        energies = []
        if 'energies' in i:
            if os.path.splitext(dic_path+'\\'+i)[1] == '.txt':
                orders = eval(i.replace('energies','').replace('.txt',''))
                with open(dic_path+'\\'+i) as f:
                    data = f.read().split("\n")
                    title = data[0].split("\t")
                    for j in data[1:]:
                        _data = j.split("\t")
                        if _data[title.index("site_name")] == "gas": continue
                        energies.append(float(_data[title.index("formation_energy")]))
                        dic[orders] = energies
    return dic 

def coverage_extraction(file_path):
    with open(file_path, 'r') as f:
        context = f.readlines()
    for i in context:
        if 'Counter(' in i:
            j = i.replace('\n','').replace('Counter(','').replace(')','')
            dic = eval(j)
    return dic

def DRC_extraction(file_path):
    dic = {}
    target_xls = xlrd.open_workbook(file_path)
    sheet = target_xls.sheet_by_name('sheet1')
    max_rows = sheet.nrows# 行
    max_cols = sheet.ncols# 列
    for i in range(max_rows):# 行
        l = []
        for j in range(max_cols):# 列
            l.append(sheet.cell(i,j).value)# 行在前，列在后
        dic[l[0]] = int(l[1])

    del dic['']
    return dic

def path_extraction(file_path):
    l = []
    with open(file_path, 'r') as f:
        context = f.readlines()
    for i in context:
        if '{' in i:
            j = i.replace('\n','')
            l.append(eval(j))
    return l[1]

def rate_extraction(file_path):
    with open(file_path,'rb') as f:
        data = pickle.load(f)
    for i in data.keys():
        if data[i] == None:
            continue
        else:
            data[i] = float(data[i])
    return data

final = {}
final_json = {}
for i in collection_dic:
    l = []
    Keys = i
    Values = collection_dic[i]
    print(Keys)
    print(Values)
    ord_energy = energy_extraction(Values[0])
    coverage_accuracy = coverage_extraction(Values[1])
    DRC_accuracy = DRC_extraction(Values[2])
    path_analysis = path_extraction(Values[3])
    rate_collect = rate_extraction(Values[4])
    l.append(ord_energy)
    l.append(coverage_accuracy)
    l.append(DRC_accuracy)
    l.append(path_analysis)
    l.append(rate_collect)
    final[Keys] = l
    final_json[str(Keys)] = l

# print(len(ord_energy))
# print(coverage_accuracy[correct_coverage])
# print(DRC_accuracy[correct_DRC])
# print(path_analysis[correct_path_hash])
# print(len(rate_collect))
# print(final)

# sorted(final)

print('deal with ' + str(len(final)) + ' groups data')

try:    
    os.makedirs(output_path)        
except:
    pass
filename_pkl = output_path + '/' + size + tee + 'Some_data_collect.pkl'
filename_txt = output_path + '/' + size + tee + 'Some_data_collect.txt'
filename_json = output_path + '/' + size + tee + 'Some_data_collect.json'

with open(filename_pkl, "wb") as f:
    pickle.dump(final, f)

with open(filename_txt, "w") as f:
    f.write(str(final))

with open(filename_json, "w") as f:
    json.dump(final_json, f)

print('work complete!')