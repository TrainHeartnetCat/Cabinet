# coding:utf-8
# 请用python2.7
# 收集正确的，以及不同RMSE下的物种对应formation energy(排除了气态)
# 格式暂定： {(rmse_low, rmse_high, order):{species:energy}}, rmse = 0时即为正确能量

import os
import pickle
import json

correct_energy_path = r'D:\Works\backup\Project01_ErrorEstimate_DRM_on_Ni111\1_ouput_data\energies_true.txt'# change, 是txt文件
RMSE_energy_path = r'D:\Works\backup\Project01_ErrorEstimate_DRM_on_Ni111\0_raw_data\All_error_simulated_formation_energy_on_Ni\raw_txt\2000sizeN'# change, 是文件夹路径
output_path = "./"# change

size = '2000sizeN'

def energy_read(catmap_input_file):  # 创建一个species对formation energy的dictionary
    with open(catmap_input_file) as f:
        data = f.read().split("\n")
        title = data[0].split("\t")
        species_name = []
        output_data = {}
        for i in data[1:]:
            _data = i.split("\t")
            # FIXME：这里需要排除气态的能量
            if _data[title.index("site_name")] == "gas": continue
            output_data[_data[title.index("species_name")]] = float(_data[title.index("formation_energy")])
    return output_data

dic = {}
dic_json = {}

dic[(0, 0, 0)] = energy_read(correct_energy_path)
dic_json['(0, 0, 0)'] = energy_read(correct_energy_path)

# print(dic[(0,0,0)])
# for i in dic[(0,0,0)]:
#     print(i + ','+str(dic[(0,0,0)][i]))
# exit(0)

RMSE_dir = os.listdir(RMSE_energy_path)
for i in RMSE_dir:
    print(i)
    key_word = i.replace('output_RMSE_','')
    key_word = key_word.replace('_',',')
    key_word = '(' + key_word + ')'
    if size:
        key_word = key_word.replace((',' + size),'')
        key = eval(key_word)
    else:
        key = eval(key_word)
    RMSE_low = key[0]
    RMSE_high = key[1]
    RMSE_dir_path = RMSE_energy_path + '/' + i
    RMSE_file = os.listdir(RMSE_dir_path)
    for j in RMSE_file:
        order = eval(j.replace('energies','').replace('.txt',''))
        file_path = RMSE_dir_path + '/' + j
        # print((RMSE_low, RMSE_high, order))
        dic[(RMSE_low, RMSE_high, order)] = energy_read(file_path)
        dic_json[str((RMSE_low, RMSE_high, order))] = energy_read(file_path)


# print(dic[(0.12, 0.14, 0)])
# exit(0)
print('deal with ' + str(len(dic)) + ' groups data')

try:    
    os.makedirs(output_path)        
except:
    pass
formation_energy_pkl = output_path + '/' + 'All_RMSE_formation_energy_collect' + size + '.pkl'
formation_energy_json = output_path + '/' + 'All_RMSE_formation_energy_collect' + size + '.json'
formation_energy_txt = output_path + '/' + 'All_RMSE_formation_energy_collect' + size + '.txt'

with open(formation_energy_pkl, "wb") as f:
    pickle.dump(dic, f)
with open(formation_energy_json, "w") as f:
    json.dump(dic_json, f)
with open(formation_energy_txt, "w") as f:
    f.write(str(dic))

print('work complete!')