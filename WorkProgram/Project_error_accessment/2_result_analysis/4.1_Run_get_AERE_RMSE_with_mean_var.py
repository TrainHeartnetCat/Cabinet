# coding:utf-8
# please run in python3

import pickle
import json
import get_activation_and_reaction_energy_from_formation_energy as gARfF
import copy
import numpy as np


# 此脚本主要分为两步
# 第一步：通过formation energy获得相应AE/RE的RMSE
# 第二步：从full_data中获得正确能量与对应加了误差的能量，计算出相应的(mean, var)
# 然后将两者对应起来，获得{(T, low, high):{(RMSE, var):low},....}

# 另外注意，该脚本相当于缝合了两个（分别是第一步和第二步）脚本的功能，运行时长较长

# 注意json中的key都是string形式,因此要小心空格等容易忽略的字符
# data中的格式为：{'(RMSE_low, RMSE_high, order)':{'species':formation energy}, ....}，留意key是string还是tuple
# gARfF返回的格式为error_of_reaction_energy, error_of_activation_energy, pred_activation_energy_work, true_activation_energy_work, pred_reaction_energy_work, true_reaction_energy_work, RMSE_of_reaction_energy, RMSE_of_activation_energy
# get_activation_and_reaction_energy_from_formation_energy(A,B)中
# 第一个变量为 物种名称到预测值的映射字典
# 第二个变量为 物种名称到DFT计算值的映射字典
print('please run in python3')

# 各RMSE和正确的formation energy，用来获取相应的AE/RE的RMSE
with open(r'D:\Works\backup\Project01_ErrorEstimate_DRM_on_Ni111\1_ouput_data\Raw_output\All_RMSE_formation_energy_collect2000sizeN.json', "r") as f:
    data = json.load(f)

# 分析后的full_data
with open(r"D:\Works\backup\Project01_ErrorEstimate_DRM_on_Ni111\1_ouput_data\Raw_output\All_data_with_order_collect_923_1023_2000sizeN.json", "r") as f:
    full_data = json.load(f)

output_path = "./"# change
size = '2000sizeN'

running_dic = copy.deepcopy(data)
del running_dic['(0, 0, 0)']

# calculation test
# test = gARfF.get_activation_and_reaction_energy_from_formation_energy(running_dic['(0.3, 0.31, 1620)'], data['(0, 0, 0)'])
# print(test[2])
# print(test[7])
# exit(0)

# get RMSE of activation and reaction energy(or other data)
reaction_energy_error_dic = {}
activation_energy_error_dic = {}
reaction_error_work = {}
activation_error_work = {}
pred_AE_dic = {}
true_AE_dic = {}
pred_RE_dic = {}
true_RE_dic = {}
pred_activation_energy_work = {}
true_activation_energy_work = {}
pred_reaction_energy_work = {}
true_reaction_energy_work = {}
AE_RMSE_dic = {}
RE_RMSE_dic = {}
AE_RMSE_work = {}
RE_RMSE_work = {}
for i in running_dic:
    RMSE_low = eval(i)[0]
    RMSE_high = eval(i)[1]
    order = eval(i)[2]
    run_formal = gARfF.get_activation_and_reaction_energy_from_formation_energy(running_dic[i], data['(0, 0, 0)'])
    reaction_error_work[order] = run_formal[0]
    activation_error_work[order] = run_formal[1]
    pred_activation_energy_work[order] = run_formal[2]
    true_activation_energy_work[order] = run_formal[3]
    pred_reaction_energy_work[order] = run_formal[4]
    true_reaction_energy_work[order] = run_formal[5]
    RE_RMSE_work[order] = run_formal[6]
    AE_RMSE_work[order] = run_formal[7]
    for j in [923, 973, 1023]:
        new_key = (j, RMSE_low, RMSE_high)
        try:
            reaction_energy_error_dic[new_key].update(reaction_error_work)
            activation_energy_error_dic[new_key].update(activation_error_work)
            pred_AE_dic[new_key].update(pred_activation_energy_work) 
            true_AE_dic[new_key].update(true_activation_energy_work)
            pred_RE_dic[new_key].update(pred_reaction_energy_work)
            true_RE_dic[new_key].update(true_reaction_energy_work)
            AE_RMSE_dic[new_key].update(AE_RMSE_work)
            RE_RMSE_dic[new_key].update(RE_RMSE_work)
        except KeyError:
            reaction_energy_error_dic[new_key] = reaction_error_work
            activation_energy_error_dic[new_key] = activation_error_work
            pred_AE_dic[new_key] = pred_activation_energy_work
            true_AE_dic[new_key] = true_activation_energy_work
            pred_RE_dic[new_key] = pred_reaction_energy_work
            true_RE_dic[new_key] = true_reaction_energy_work
            AE_RMSE_dic[new_key] = AE_RMSE_work
            RE_RMSE_dic[new_key] = RE_RMSE_work
    reaction_error_work = {}
    activation_error_work = {}
    pred_activation_energy_work = {}
    true_activation_energy_work = {}
    pred_reaction_energy_work = {}
    true_reaction_energy_work = {}
    AE_RMSE_work = {}
    RE_RMSE_work = {}


# print(AE_RMSE_dic[(923, 0.3, 0.31)][1620])
# print(AE_RMSE_dic[(923, 0.26, 0.28)][0])
# 出现问题，和我手算的不一样，不过我怀疑是我手算错了= =，测试一下吧
# calculation test完成，手算无误，是我把AE和RE的序号填反了
# 那么现在获得结果AE/RE_RMSE_dic格式为{(T, low, high):{order:RMSE_of_AE/RE, ....}}
# 接下来需要从full data中提取正确能量和加了误差能量，来计算mean和var

# get mean and var of different RMSE
# 收集各个温度，RMSE下，以error的mean和var为key，结果作为value
error_mv_to_path = {}
error_mv_to_drc = {}
error_mv_to_coverage = {}
error_mv_to_rate = {}
error_mv_to_ae_RMSE = {}
error_mv_to_re_RMSE = {}

for key in full_data:
    tuple_key = eval(key)  # 通过eval把tuple字符串转成tuple
    temperature, low, high = tuple_key
    correct_energy, \
    order_to_energy, \
    order_to_path, \
    order_to_species_str_and_coverage, \
    order_to_rxn_str_and_drc, \
    order_to_log_rate, \
    rmse = full_data[key]
# 因为是从其他脚本里直接复制过来的，有些内容其实并不需要，但为了方便起见，只删除并修改了一部分，因此请留意开头的注释，明确此脚本的目的
    correct_energy = np.array(correct_energy)

    # 这里面以mean和var作为key，以原来的预测结果作为value
    error_mv_to_path[tuple_key] = dict()
    error_mv_to_drc[tuple_key] = dict()
    error_mv_to_coverage[tuple_key] = dict()
    error_mv_to_rate[tuple_key] = dict()
    error_mv_to_ae_RMSE[tuple_key] = dict()
    error_mv_to_re_RMSE[tuple_key] = dict()


    for i in range(2000):
        target_energy = order_to_energy[str(i)]
        target_AE_error = AE_RMSE_dic[tuple_key][i]
        target_RE_error = RE_RMSE_dic[tuple_key][i]

        error = np.array(target_energy) - correct_energy
        mean = float(np.mean(error))
        bias2 = np.square(mean)
        var = float(np.var(error))
        # print('mean: ' + str(mean)  + ' ' + str(tuple_key) + ' ' + str(i) + ' ' +  'var:' +  str(var))            

        # 制作成{(T, low, high):{(RMSE, var):low},....}，如有另外需要可以再改
        error_mv_to_ae_RMSE[tuple_key][(target_AE_error, var, mean, bias2)] = low
        error_mv_to_re_RMSE[tuple_key][(target_RE_error, var, mean, bias2)] = low
        # error_mv_to_ae_RMSE[tuple_key][(mean, var)] = target_AE_error
        # error_mv_to_re_RMSE[tuple_key][(mean, var)] = target_RE_error

# exit(0)

try:    
    os.makedirs(output_path)        
except:
    pass
AE_RMSE_var_with_lowRMSE_pkl = output_path + '/' +  'AE_RMSE_var_mean_with_lowRMSE_923_1023' + '_' + size + '.pkl'
AE_RMSE_var_with_lowRMSE_txt = output_path + '/' +  'AE_RMSE_var_mean_with_lowRMSE_923_1023' + '_' + size + '.txt'

RE_RMSE_var_with_lowRMSE_pkl = output_path + '/' +  'RE_RMSE_var_mean_with_lowRMSE_923_1023' + '_' + size + '.pkl'
RE_RMSE_var_with_lowRMSE_txt = output_path + '/' +  'RE_RMSE_var_mean_with_lowRMSE_923_1023' + '_' + size + '.txt'

with open(AE_RMSE_var_with_lowRMSE_pkl, "wb") as f:
    pickle.dump(error_mv_to_ae_RMSE, f)
# with open(AE_RMSE_var_with_lowRMSE_json, "w") as f:
#     json.dump(error_mv_to_ae_RMSE, f)
with open(AE_RMSE_var_with_lowRMSE_txt, "w") as f:
    f.write(str(error_mv_to_ae_RMSE))

with open(RE_RMSE_var_with_lowRMSE_pkl, "wb") as f:
    pickle.dump(error_mv_to_re_RMSE, f)
# with open(RE_RMSE_var_with_lowRMSE_json, "w") as f:
#     json.dump(error_mv_to_re_RMSE, f)
with open(RE_RMSE_var_with_lowRMSE_txt, "w") as f:
    f.write(str(error_mv_to_re_RMSE))


print('work complete!')