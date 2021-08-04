# coding:utf-8
# please run in python3

import pickle
import json
import get_activation_and_reaction_energy_from_formation_energy as gARfF
import copy

# with open(r'D:\Works\backup\ErrorEstimate\Running_analysis\data_collect\All_RMSE_formation_energy_collect.pkl','rb') as f:
#     data = pickle.load(f)
# 由于py2 py3在pickle模块上的问题，而pkl文件是py2生成的（需要用py2跑）、get from formation energy模块使用了py3语法，为了避免问题，暂时不使用pickle，直接用json。
# 注意json中的key都是string形式,因此要小心空格等容易忽略的字符
# data中的格式为：{'(RMSE_low, RMSE_high, order)':{'species':formation energy}, ....}，留意key是string还是tuple

print('please run in python3')

with open(r'D:\Works\backup\Project01_ErrorEstimate_DRM_on_Ni111\1_ouput_data\Raw_output\All_RMSE_formation_energy_collect2000sizeN.json', "r") as f:# change
    data = json.load(f)

output_path = "./"# change


# print(data['(0, 0, 0)'])
# print(data['(0.1, 0.12, 0)'])

DFT_formation_pair = data['(0, 0, 0)']
test_group = data['(0.1, 0.12, 0)']

running_dic = copy.deepcopy(data)
del running_dic['(0, 0, 0)']

# get_activation_and_reaction_energy_from_formation_energy(A,B)中
# 第一个变量为 物种名称到预测值的映射字典
# 第二个变量为 物种名称到DFT计算值的映射字典

# get RMSE of activation and reaction energy
# test
# run_test = gARfF.get_activation_and_reaction_energy_from_formation_energy(data['(0.1, 0.12, 0)'], data['(0, 0, 0)'])

# print(len(run_test[2])) #(rmse of reaction energy, rmse of activation energy)

# formal
# 原本的gARfF是返回AE和RE的RMSE，现在gARfF返回的是AE和RE的error_list
# reaction_energy_RMSE_dic = {}
# activation_energy_RMSE_dic = {}
# reaction_work = {}
# activation_work = {}
# for i in running_dic:
#     RMSE_low = eval(i)[0]
#     RMSE_high = eval(i)[1]
#     order = eval(i)[2]
#     run_formal = gARfF.get_activation_and_reaction_energy_from_formation_energy(running_dic[i], data['(0, 0, 0)'])
#     reaction_work[order] = run_formal[0]
#     activation_work[order] = run_formal[1]
#     for j in [923, 973, 1023]:
#         new_key = (j, RMSE_low, RMSE_high)
#         # print(run_formal[0])
#         reaction_energy_RMSE_dic[str(new_key)] = reaction_work
#         activation_energy_RMSE_dic[str(new_key)] = activation_work

# 由于现在gARfF返回的是AE和RE的error_list，根据之前的数据收集，整合结果
# data中的格式为：{'(RMSE_low, RMSE_high, order)':{'species':formation energy}, ....}，留意key是string还是tuple
# run_formal格式：(error_of_reaction_energy, error_of_activation_energy, pred_activation_energy, true_activation_energy, pred_reaction_energy, true_reaction_energy)
reaction_energy_error_dic = {}
activation_energy_error_dic = {}
reaction_error_work = {}
activation_error_work = {}
pred_AE = {}
true_AE = {}
pred_RE = {}
true_RE = {}
pred_activation_energy = {}
true_activation_energy = {}
pred_reaction_energy = {}
true_reaction_energy = {}
# exit(0)
for i in running_dic:
    RMSE_low = eval(i)[0]
    RMSE_high = eval(i)[1]
    order = eval(i)[2]
    run_formal = gARfF.get_activation_and_reaction_energy_from_formation_energy(running_dic[i], data['(0, 0, 0)'])
    new_key = eval(i)
    reaction_error_work[order] = run_formal[0]
    activation_error_work[order] = run_formal[1]
    pred_activation_energy[order] = run_formal[2]
    true_activation_energy[order] = run_formal[3]
    pred_reaction_energy[order] = run_formal[4]
    true_reaction_energy[order] = run_formal[5]
    for j in [923, 973, 1023]:
        new_key = (j, RMSE_low, RMSE_high)
        try:
            reaction_energy_error_dic[str(new_key)].update(reaction_error_work)
            activation_energy_error_dic[str(new_key)].update(activation_error_work)
            pred_AE[str(new_key)].update(pred_activation_energy) 
            true_AE[str(new_key)].update(true_activation_energy)
            pred_RE[str(new_key)].update(pred_reaction_energy)
            true_RE[str(new_key)].update(true_reaction_energy)
        except KeyError:
            reaction_energy_error_dic[str(new_key)] = reaction_error_work
            activation_energy_error_dic[str(new_key)] = activation_error_work
            pred_AE[str(new_key)] = pred_activation_energy
            true_AE[str(new_key)] = true_activation_energy
            pred_RE[str(new_key)] = pred_reaction_energy
            true_RE[str(new_key)] = true_reaction_energy
    reaction_error_work = {}
    activation_error_work = {}
    pred_activation_energy = {}
    true_activation_energy = {}
    pred_reaction_energy = {}
    true_reaction_energy = {}



# print(len(pred_AE),len(true_AE),len(pred_RE),len(true_RE))
# print(len(reaction_energy_RMSE_dic))
# print(len(reaction_energy_RMSE_dic['(923, 0.1, 0.12)']))
# print(len(activation_energy_RMSE_dic))
# print(len(activation_energy_RMSE_dic['(923, 0.1, 0.12)']))

# print('deal with ' + str(len(energy_RMSE_dic)) + ' groups data')



try:    
    os.makedirs(output_path)        
except:
    pass
# # energy_RMSE_pkl = output_path + '/' + 'activation_and_reaction_energy_RMSE.pkl'
# # energy_RMSE_json = output_path + '/' + 'activation_and_reaction_energy_RMSE.json'
# # energy_RMSE_txt = output_path + '/' + 'activation_and_reaction_energy_RMSE.txt'

# exit(0)

# reaction_energy_order_pkl = output_path + '/' + 'reaction_energy_with_order_923_1023.pkl'
# reaction_energy_order_json = output_path + '/' + 'reaction_energy_with_order_923_1023.json'
# reaction_energy_order_txt = output_path + '/' + 'reaction_energy_with_order_923_1023.txt'

# activation_energy_order_pkl = output_path + '/' + 'activation_energy_with_order_923_1023.pkl'
# activation_energy_order_json = output_path + '/' + 'activation_energy_with_order_923_1023.json'
# activation_energy_order_txt = output_path + '/' + 'activation_energy_with_order_923_1023.txt'

# with open(reaction_energy_order_pkl, "wb") as f:
#     pickle.dump(reaction_energy_RMSE_dic, f)
# with open(reaction_energy_order_json, "w") as f:
#     json.dump(reaction_energy_RMSE_dic, f)
# with open(reaction_energy_order_txt, "w") as f:
#     f.write(str(reaction_energy_RMSE_dic))

# with open(activation_energy_order_pkl, "wb") as f:
#     pickle.dump(activation_energy_RMSE_dic, f)
# with open(activation_energy_order_json, "w") as f:
#     json.dump(activation_energy_RMSE_dic, f)
# with open(activation_energy_order_txt, "w") as f:
#     f.write(str(activation_energy_RMSE_dic))

AE和RE的error
RE_error_order_pkl = output_path + '/' + 'RE_error_with_order_923_1023.pkl'
RE_error_order_json = output_path + '/' + 'RE_error_with_order_923_1023.json'
RE_error_order_txt = output_path + '/' + 'RE_error_with_order_923_1023.txt'

AE_error_order_pkl = output_path + '/' + 'AE_error_with_order_923_1023.pkl'
AE_error_order_json = output_path + '/' + 'AE_error_with_order_923_1023.json'
AE_error_order_txt = output_path + '/' + 'AE_error_with_order_923_1023.txt'

with open(RE_error_order_pkl, "wb") as f:
    pickle.dump(reaction_energy_error_dic, f)
with open(RE_error_order_json, "w") as f:
    json.dump(reaction_energy_error_dic, f)
with open(RE_error_order_txt, "w") as f:
    f.write(str(reaction_energy_error_dic))

with open(AE_error_order_pkl, "wb") as f:
    pickle.dump(activation_energy_error_dic, f)
with open(AE_error_order_json, "w") as f:
    json.dump(activation_energy_error_dic, f)
with open(AE_error_order_txt, "w") as f:
    f.write(str(activation_energy_error_dic))


# AE和RE的能量
RE_pred_pkl = output_path + '/' +  'RE_pred_923_1023.pkl'
RE_pred_json = output_path + '/' + 'RE_pred_923_1023.json'
RE_pred_txt = output_path + '/' +  'RE_pred_923_1023.txt'

RE_true_pkl = output_path + '/' +  'RE_true_923_1023.pkl'
RE_true_json = output_path + '/' + 'RE_true_923_1023.json'
RE_true_txt = output_path + '/' +  'RE_true_923_1023.txt'


AE_pred_pkl = output_path + '/' +  'AE_pred_923_1023.pkl'
AE_pred_json = output_path + '/' + 'AE_pred_923_1023.json'
AE_pred_txt = output_path + '/' +  'AE_pred_923_1023.txt'

AE_true_pkl = output_path + '/' +  'AE_true_923_1023.pkl'
AE_true_json = output_path + '/' + 'AE_true_923_1023.json'
AE_true_txt = output_path + '/' +  'AE_true_923_1023.txt'



with open(RE_pred_pkl, "wb") as f:
    pickle.dump(pred_RE, f)
with open(RE_pred_json, "w") as f:
    json.dump(pred_RE, f)
with open(RE_pred_txt, "w") as f:
    f.write(str(pred_RE))


with open(RE_true_pkl, "wb") as f:
    pickle.dump(true_RE, f)
with open(RE_true_json, "w") as f:
    json.dump(true_RE, f)
with open(RE_true_txt, "w") as f:
    f.write(str(true_RE))


with open(AE_pred_pkl, "wb") as f:
    pickle.dump(pred_AE, f)
with open(AE_pred_json, "w") as f:
    json.dump(pred_AE, f)
with open(AE_pred_txt, "w") as f:
    f.write(str(pred_AE))

with open(AE_true_pkl, "wb") as f:
    pickle.dump(true_AE, f)
with open(AE_true_json, "w") as f:
    json.dump(true_AE, f)
with open(AE_true_txt, "w") as f:
    f.write(str(true_AE))


print('work complete!')