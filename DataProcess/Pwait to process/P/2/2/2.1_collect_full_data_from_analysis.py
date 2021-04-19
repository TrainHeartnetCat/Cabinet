# coding:utf-8
# 请用python2.7
# 从running_result文件夹中，获取不同温度，不同RMSE文件夹中的coverage，DRC，path，rate文件夹中提取数据，加上对应RMSE的能量
# 输出结果并存储成pkl文件。
# Key: (t,RMSE_low,RMSE_high)
# Value: [[correct_energy], [errored_energy],[path],[drc],[coverage],[rate]]
# correct_energy: 从正确energyTXT中提取的正确能量
# errored_energy: 能量的字典，key为序号，value为能量list。使用energy_extraction函数获取
# coverage: 覆盖度的字典，key为序号，value为物种。使用order_coverage_extraction函数获取
# DRC: DRC的字典，key为速率序号， value为步骤。使用order_DRC_extraction函数获取
# path: hash值与路径的字典，key为物种，value为hash。使用order_path_extraction函数获取
# rate: rate和序号的字典，key为序号，value为rate。


# dic_outputpkl = {(t, low, high):[[correct_energy], {order_int:[errored_energy]}, {order:path_hash}, {order_int:(species_str, coverage_str)}, {order_int:(step_str, drc_rate_str)}, {order:rate}, {rate_rmse:rmse}], ...}
# 每个RMSE下的formation energy == 每个dic_outputpkl中的{order_int:[errored_energy]}，也就是dic_outputpkl[x][1]，温度取任何一个都可以

import os
import pickle
import json
from mpmath import mp

print('Please run in python2.7')

input_energy_path = r'D:\Works\backup\Project01_ErrorEstimate_DRM_on_Ni111\0_raw_data\All_error_simulated_formation_energy_on_Ni\raw_txt\2000sizeN'
input_analysis_path = r'D:\Works\backup\Project01_ErrorEstimate_DRM_on_Ni111\1_ouput_data\Raw_output\size2000N'
correct_energy_path = r'D:\Works\backup\Project01_ErrorEstimate_DRM_on_Ni111\1_ouput_data\energies_true.txt'
output_path = "./"# change

coverfix_path = ''
drcfix_path = ''
pathfix_path = ''
ratefix_path = '\\1_rate'

correct_rate = {823:-2.26973000311378, 873:-0.440814732687624, 923:0.799418429845564, 973:1.53150188283413, 1023:1.92911193854381}
file_num = 2000
tmp = [923, 973, 1023]# change
# tmp = [823, 873]
# tmp = [923]
RMSE = [(0.1, 0.12), (0.12, 0.14), (0.14, 0.16), (0.16, 0.18), (0.18, 0.2), (0.2, 0.22), (0.22, 0.24), (0.24, 0.26), (0.26, 0.28), (0.28, 0.3)]# change
size = '2000sizeN'
# RMSE = [(0.1, 0.12), (0.12, 0.14)]
# RMSE = [(0.1, 0.12)]
collection_dic = {}

for t in tmp:
    for i in RMSE:
        working_path = []
        RMSE_low = i[0]
        RMSE_high = i[1]
        key = (t, RMSE_low, RMSE_high)
        energyfile_path = input_energy_path + '/output_RMSE_%s_%s_%s' % (RMSE_low, RMSE_high, size)# energy的路径
        analysis_path = input_analysis_path + '\\%s\\RMSE_%s_%s_%s' % (t, RMSE_low, RMSE_high, size)

        coverageanal = analysis_path + coverfix_path + '\\1_coverage.pklmax_coverage.pkl'#保留最大覆盖度物种
        drcanal = analysis_path + drcfix_path + '\\1_drc.pklmax_DRC.pkl'#
        pathanal = analysis_path + pathfix_path + '\\1hash_index_dict.pkl'#找两个字典
        rateanal = analysis_path + ratefix_path + '\\rx_rate_collection_result.pkl'#直接用

        correct_energy = correct_energy_path
        working_path.append(energyfile_path)
        working_path.append(coverageanal)
        working_path.append(drcanal)
        working_path.append(pathanal)
        working_path.append(rateanal)
        working_path.append(correct_energy)
        collection_dic[key] = working_path

# class json_mpfEncoder(json.JSONEncoder):
#     def default(self, item):
#         if isinstance(item, mp.mpf):
#             return item.__new__()
#         return json.JSONEncoder.default(self, item)

def correct_energy_extraction(file_path):
    with open(file_path) as f:
        data = f.read().split("\n")
        title = data[0].split("\t")
        output_data = []
        for i in data[1:]:
            _data = i.split("\t")
            # FIXME：这里需要排除气态的能量
            if _data[title.index("site_name")] == "gas": continue
            output_data.append(float(_data[title.index("formation_energy")]))
    return output_data


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

def order_path_extraction(file_path):
    dic = {}
    with open(file_path,'rb') as f:
        data = pickle.load(f)
    for i in data:
        for j in data[i]:
            dic[j] = i
    return dic

def order_coverage_extraction(file_path):
    dic = {}
    with open(file_path,'rb') as f:
        data = pickle.load(f)
    for i in data:
        dic[int(i)] = data[i][0]
    return dic


def order_DRC_extraction(file_path, file_num):
    dic = {}
    with open(file_path,'rb') as f:
        data = pickle.load(f)
    for i in data:
        dic[int(i)] = data[i]
    if len(data) < file_num:
        for j in range(file_num):
            if j not in dic:
                dic[j] = None
    return dic

def order_rate_extraction(file_path):
    with open(file_path,'rb') as f:
        data = pickle.load(f)
    return data

def rate_process_log(rate_dic):
    dic = {}
    for i in rate_dic:
        if rate_dic[i] != None:
            dic[i] = mp.log(rate_dic[i],10)
        else:
            dic[i] = None
    return dic

def rate_process_RMSE(rate_log_dic, correct_rate, size):
    l = []
    dic = {}
    correct_rate_mpf = mp.mpf(correct_rate)
    for i in rate_log_dic:
        if rate_log_dic[i] == None:
            continue
        else:
            element = mp.fsub(rate_log_dic[i], correct_rate_mpf)
            l.append(element)
    square = mp.fsum(l, squared=True)
    mean = mp.fdiv(square, size)
    root = mp.sqrt(mean)
    dic['rate_RMSE'] = root
    return dic

def rate_mpf2float(dic):
    for i in dic:
        if dic[i] == None:
            continue
        else:
            dic[i] = float(dic[i])
    return dic


final = {}
final_json = {}
formation_energy_dic = {}
for i in collection_dic:
    l = []
    l_json = []
    Keys = i
    Values = collection_dic[i]
    print(Keys)
    print(Values)
    ord_energy = energy_extraction(Values[0])
    coverage_data = order_coverage_extraction(Values[1])
    DRC_data = order_DRC_extraction(Values[2], file_num)
    path_data = order_path_extraction(Values[3])
    rate_data = order_rate_extraction(Values[4])
    processed_rate_log = rate_process_log(rate_data)
    processed_rate_RMSE = rate_process_RMSE(processed_rate_log, correct_rate[Keys[0]], file_num)
    correct_energy_data = correct_energy_extraction(Values[5])
    l.append(correct_energy_data)
    l.append(ord_energy)
    l.append(path_data)
    l.append(coverage_data)
    l.append(DRC_data)
    # l.append(rate_data)
    l.append(processed_rate_log)
    l.append(processed_rate_RMSE)

    l_json.append(correct_energy_data)
    l_json.append(ord_energy)
    l_json.append(path_data)
    l_json.append(coverage_data)
    l_json.append(DRC_data)
    # l_json.append(rate_data)
    l_json.append(rate_mpf2float(processed_rate_log))
    l_json.append(rate_mpf2float(processed_rate_RMSE))
    final[Keys] = l
    final_json[str(Keys)] = l_json
    formation_energy_dic[Keys] = final[Keys][1]



# print(final_json['(973, 0.1, 0.12)'][-1])
# print(final[(973, 0.1, 0.12)][-1])
# print(final[(923, 0.1, 0.12)][1])
# print(len(formation_energy_dic))

print('deal with ' + str(len(final)) + ' groups data')

try:    
    os.makedirs(output_path)        
except:
    pass
filename_pkl = output_path + '/' + 'All_data_with_order_collect_%s_%s_%s.pkl' % (tmp[0], tmp[-1], size)
filename_json = output_path + '/' + 'All_data_with_order_collect_%s_%s_%s.json' % (tmp[0], tmp[-1], size)
filename_txt = output_path + '/' + 'All_data_with_order_collect_%s_%s_%s.txt' % (tmp[0], tmp[-1], size)

# formation_energy_pkl = output_path + '/' + 'All_RMSE_formation_energy_collect.pkl'
# formation_energy_json = output_path + '/' + 'All_RMSE_formation_energy_collect.json'
# formation_energy_txt = output_path + '/' + 'All_RMSE_formation_energy_collect.txt'

with open(filename_pkl, "wb") as f:
    pickle.dump(final, f)
with open(filename_json, "w") as f:
    json.dump(final_json, f)
with open(filename_txt, "w") as f:
    f.write(str(final))

# with open(formation_energy_pkl, "wb") as f:
#     pickle.dump(formation_energy_dic, f)
# with open(formation_energy_json, "w") as f:
#     json.dump(formation_energy_dic_json, f)
# with open(formation_energy_txt, "w") as f:
#     f.write(str(formation_energy_dic))

print('work complete!')