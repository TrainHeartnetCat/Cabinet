# coding:utf-8

import os
import pickle
import json
import numpy as np
import xlwt
from sklearn import linear_model#表示，可以调用sklearn中的linear_model模块进行线性回归。


print('Please run in python3')

output_path = './'


with open(r"D:\Works\backup\Project01_ErrorEstimate_DRM_on_Ni111\1_ouput_data\Raw_output\All_data_with_order_collect_923_1023_2000sizeN.json", "r") as f:
    data = json.load(f)

# error不需要，暂时不要了
# with open(r"D:\Works\backup\ErrorEstimate\Running_analysis\data_collect\AE_error_with_order_923_1023.json", "r") as f:
#     AE_error_data = json.load(f)
# with open(r"D:\Works\backup\ErrorEstimate\Running_analysis\data_collect\RE_error_with_order_923_1023.json", "r") as f:
#     RE_error_data = json.load(f)

# 加入pred的AE，RE和true的AE，RE
with open(r"D:\Works\backup\Project01_ErrorEstimate_DRM_on_Ni111\1_ouput_data\Raw_output\AE_pred_923_1023.json", "r") as f:
    AE_pred_data = json.load(f)
with open(r"D:\Works\backup\Project01_ErrorEstimate_DRM_on_Ni111\1_ouput_data\Raw_output\AE_true_923_1023.json", "r") as f:
    AE_true_data = json.load(f)
with open(r"D:\Works\backup\Project01_ErrorEstimate_DRM_on_Ni111\1_ouput_data\Raw_output\RE_pred_923_1023.json", "r") as f:
    RE_pred_data = json.load(f)
with open(r"D:\Works\backup\Project01_ErrorEstimate_DRM_on_Ni111\1_ouput_data\Raw_output\RE_true_923_1023.json", "r") as f:
    RE_true_data = json.load(f)

# for key in data:
#     data[key].append(AE_error_data[key])
#     data[key].append(RE_error_data[key])

for key in data:
    data[key].append(AE_pred_data[key])
    data[key].append(AE_true_data[key])
    data[key].append(RE_pred_data[key])
    data[key].append(RE_true_data[key])

worklist2 = []
worklist2_AE_true_pred = []
worklist2_RE_true_pred = []
# 敲定组4v
# key = '(923, 0.2, 0.22)'
# resolution = '173'
# rank = '_R=0.210603876884215_b=0.156525571853453_v=0.0198537383146109_'
# 敲定组1v
# key = '(923, 0.2, 0.22)'
# resolution = '1719'
# rank = '_R=0.21062550584696_b=0.210280375473401_v=0.00014526740405369_'
# 敲定组2v
# key = '(923, 0.2, 0.22)'
# resolution = '1717'
# rank = '_R=0.210640163966547_b=-0.19425_v=0.006636_'
# 敲定组1v
key = '(923, 0.2, 0.22)'
resolution = '126'
rank = '_R=0.210642_b=0.186458_v=0.009603_'

# key = '(923, 0.2, 0.22)'
# resolution = '91'
# rank = '_b=-0.178232739_v=0.013907766_'

# key = '(923, 0.26, 0.28)'
# resolution = '282'
# rank = 'high_var'

# print(data['(923, 0.3, 0.31)'])
# resolution = '622'
# rank = 'min'
# resolution = '600'
# rank = 'med'
#使用特例时，记得修改下方worklist的append

# '''


tuple_key = eval(key)  # 通过eval把tuple字符串转成tuple
temperature, RMSE_min, RMSE_max = tuple_key
correct_energy, \
order_to_energy, \
order_to_path, \
order_to_species_str_and_coverage, \
order_to_rxn_str_and_drc, \
order_to_log_rate, \
rmse, \
order_to_pred_AE, \
order_to_true_AE, \
order_to_pred_RE, \
order_to_true_RE = data[key]



worklist2.append(correct_energy)
worklist2.append(order_to_energy[resolution])

worklist2_AE_true_pred.append(order_to_true_AE[resolution])
worklist2_AE_true_pred.append(order_to_pred_AE[resolution])
worklist2_RE_true_pred.append(order_to_true_RE[resolution])
worklist2_RE_true_pred.append(order_to_pred_RE[resolution])
# print(order_to_true_AE)
# print(order_to_pred_AE[resolution])

# exit(0)
# max_true_AE = [1.2049999999999996, 0.8379999999999999, 0.641, 0.5980000000000001, 1.418, 2.122, 0.9390000000000001, 1.223, 0.6550000000000001, 1.109, 0.9, 0.84, 1.5539999999999998, 1.412, 1.248, 1.381, 1.2990000000000002, 1.419, 1.435, 1.2890000000000001, 1.9300000000000006]
# max_pred_AE = [1.0039999999999998, 0.43699999999999983, 0.44999999999999996, 0.385, 1.097, 1.704, 0.646, 0.986, 0.48100000000000004, 0.884, 0.521, 0.568, 1.208, 1.1749999999999998, 1.051, 1.075, 1.0679999999999998, 1.0570000000000002, 1.2380000000000002, 1.0610000000000002, 1.6610000000000005]
# min_true_AE = [1.2049999999999996, 0.8379999999999999, 0.641, 0.5980000000000001, 1.418, 2.122, 0.9390000000000001, 1.223, 0.6550000000000001, 1.109, 0.9, 0.84, 1.5539999999999998, 1.412, 1.248, 1.381, 1.2990000000000002, 1.419, 1.435, 1.2890000000000001, 1.9300000000000006]
# min_pred_AE = [1.5299999999999998, 1.088, 0.34899999999999987, 0.721, 1.895, 3.003, 1.0710000000000002, 1.5750000000000002, 0.9579999999999999, 1.0899999999999999, 2.005, 1.9169999999999998, 2.331, 1.1919999999999997, 0.2529999999999999, 1.445, 1.2109999999999996, 0.7940000000000002, 1.19, 0.7269999999999999, 2.231]
# # worklist2_AE_true_pred.append(max_true_AE)
# # worklist2_AE_true_pred.append(max_pred_AE)

# worklist2_AE_true_pred.append(min_true_AE)
# worklist2_AE_true_pred.append(min_pred_AE)


# print(worklist2_AE_true_pred)


# X = np.array(worklist2[0])
# X = X.reshape(-1, 1)
# Y = np.array(worklist2[1])
# Y = Y.reshape(-1, 1)
# print(X.shape,Y.shape)
# model = linear_model.LinearRegression()
# model.fit(X, Y)
# print(model.intercept_, model.coef_)




def excel_create(data_list, output_dir, output_file_name, resolution, rank):
    xls = xlwt.Workbook(encoding = 'utf-8')
    sheet = xls.add_sheet('test1')

    count_row = 0
    count_colmun = 0
    for i in data_list:
        for j in range(len(i)):
            sheet.write(j,count_colmun, label = i[j])
        count_row = count_row + 1
        count_colmun = count_colmun + 1

    file_name = output_path + '/' + output_file_name +'_' + str(resolution) + rank + '.xls'
    print(file_name)
    xls.save(file_name)
    print('excel has been created!')


excel_create(worklist2, output_path, 'PE2CE.xls', resolution, rank)

excel_create(worklist2_AE_true_pred, output_path, 'AE_of_pre2tru_0.3.xls', resolution, rank)
excel_create(worklist2_RE_true_pred, output_path, 'RE_of_pre2tru_0.3.xls', resolution, rank)



# for key in data:
#     print(key)
#     tuple_key = eval(key)  # 通过eval把tuple字符串转成tuple
#     temperature, RMSE_min, RMSE_max = tuple_key
#     correct_energy, \
#     order_to_energy, \
#     order_to_path, \
#     order_to_species_str_and_coverage, \
#     order_to_rxn_str_and_drc, \
#     order_to_log_rate, \
#     rmse = data[key]
#     break
# '''