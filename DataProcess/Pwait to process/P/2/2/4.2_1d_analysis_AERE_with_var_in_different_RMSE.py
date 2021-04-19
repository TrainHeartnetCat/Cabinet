# coding:utf-8

import os
import pickle
import numpy as np
import xlwt
import matplotlib.pyplot as plt
# 目标：制作不同RMSE下，AE/RE的RMSE与var/bias的图，AE/RE_file中数据格式为{(T, low, high):{(mean, var):RMSE,...}}
# 作图方式：
# 先用excel作初判断，因此需要将某个low对应的数据导出来，为了方便起见，直接使用具体特例
# 然后使用matplotlib绘制散点图，不同RMSE使用不同颜色的点，将22000个点放进同一张图
# 另外，注意input数据使用pickle保存的，并不是json

print('Please run in python3')
plt.rc('font',family='Arial')
plt.rc('font',weight="bold")

AE_file = r'D:\Works\backup\Project01_ErrorEstimate_DRM_on_Ni111\1_ouput_data\Raw_output\AE_RMSE_var_mean_with_lowRMSE_923_1023_2000sizeN.pkl'
RE_file = r'D:\Works\backup\Project01_ErrorEstimate_DRM_on_Ni111\1_ouput_data\Raw_output\RE_RMSE_var_mean_with_lowRMSE_923_1023_2000sizeN.pkl'

output_path = './'

with open(AE_file,'rb') as f:
    AE_dic = pickle.load(f)
with open(RE_file,'rb') as f:
    RE_dic = pickle.load(f)
# {(T, low, high):{(RMSE, var, bias, bias square):low, ....}}
specific_example = 'off'# 如果采用特例进行初判断，设置为'on'，否则设置为'off'
denoise = 'off'# 选择是否降噪，是则为'on'，否则为'off'
mode = 'x'# 对x轴降噪，请将mode设置为'x'; 对y轴降噪，请将mode设置为'y'
energy = 'AE'# 为'AE'时作AE的图，为'RE'时作RE的图
x_type = 'var'# 为'var'时设置横轴为variance，为'bias'时设置横轴为bias
label_dic = {0.1:'0.1~0.12 eV', 0.12:'0.12~0.14 eV', 0.14:'0.14~0.16 eV', 0.16:'0.16~0.18 eV', 0.18:'0.18~0.2 eV', 0.2:'0.2~0.22 eV', 0.22:'0.22~0.24 eV', 0.24:'0.24~0.26 eV', 0.26:'0.26~0.28 eV', 0.28:'0.28~0.3 eV', 0.3:'0.3~0.31 eV'}

if specific_example == 'on':
    # 使用特例，用excel进行初判断
    test_key = (923, 0.30, 0.31)
    example = AE_dic[test_key]# 格式为{(RMSE of energy, var):low, ....}
    var_list = []
    for i in example.keys():
        var_list.append(i[1])
    print('Maxmium variance in this group is ' + str(max(var_list)))
    print('Minmium variance in this group is ' + str(min(var_list)))

    # exit(0)

    # 直接散点图效果不理想，尝试降噪
    # var化成比如10个范围，然后每个范围里面的数据点求均值，做成线图再看看
    AE_dic[test_key].keys()
    AE_dic_test_key_sorted_var = sorted(AE_dic[test_key].keys(),key=lambda item:item[1])
    AE_dic_test_key_sorted_RMSE = sorted(AE_dic[test_key].keys(),key=lambda item:item[0])

    # print(AE_dic_test_key_sorted_var)

    # 设置分割值，并对数据进行分割，获得worklist，对其中数据进行求均值降噪，x轴点暂时使用小的值，最终获得worklist2
    if mode == 'x':
        sorted_items_by_var_list = AE_dic_test_key_sorted_var# 数据来源，只需修改working_dic即可
        resolution = 144# change: 分割数，修改分割数可以改变length，即x轴间隔
        # 需注意，如果resolution过大导致length过小，可能会发生分割出来的格点里没有数据的情况
        # 这种情况多数出现在x轴头尾，在worklist中会体现为首尾
        var_min = sorted_items_by_var_list[0][1]
        var_max = sorted_items_by_var_list[-1][1]
        keep_n = 2# change: 因为方差的最大值不超过0.1(比如0.094，0.083)，因此保留方差的两位小数，max向上进位，min向下进位
        correct = 0.1**keep_n / keep_n# 为了根据方差的最大值进行分割，因此需要有一位有效数字的x_max，由于没有简单的保留n位小数，向上或下进位的函数，在这里根据需要保留位数设置correct值
        x_min = round(var_min - correct, 2)# 可能会减成负零，但是是等价于零的
        x_max = round(var_max + correct, 2)
        length = x_max / resolution

        worklist = []
        for i in range(resolution):
            worklist.append([])

        count = 0
        current_position = 0
        while current_position <= x_max:
            for i in sorted_items_by_var_list:
                if current_position <= i[1] <= current_position + length:
                    worklist[count].append(i)
            current_position += length
            count += 1

        # 对worklist中数据求均值降噪，x轴点暂时使用小的值，获得worklist2
        worklist2 = []
        for i in range(resolution):
            worklist2.append([])

        count2 = 0
        current_position2 = 0

        for i in worklist:
            mean_list = []
            if i != []:
                for j in i:
                    mean_list.append(j[0])
                    mean = np.mean(mean_list)            
                position_x = current_position2
                worklist2[count2].append((mean,position_x))
                current_position2 += length
                count2 += 1
            if i == []:
                continue

        if worklist2.count([]) != 0:# 如果有未分配到的区域，敲掉
            for i in range(worklist2.count([])):
                worklist2.remove([])


    if mode == 'y':
        pass

    # exit(0)
    # 需要导出的数据格式为，var作x轴，RMSE作y轴，即第一列为var，第二列为RMSE
    # 变量分别为数据集，输出路径，特例编号，降噪模式，降噪比例
    def excel_create(data, output_dir, feature, mode, resolution):
        xls = xlwt.Workbook(encoding = 'utf-8')
        sheet = xls.add_sheet('test1')
        # 导入[[(mean_RMSE, cutted_var)],[(mean_RMSE, cutted_var)],...]
        if mode != 'original':
            count_row = 0
            for i in data:
                sheet.write(count_row,0, label = i[0][1])
                sheet.write(count_row,1, label = i[0][0])
                count_row += 1

        #直接导入{(RMSE, var):low, ....}数据时的代码
        if mode == 'original':
            count_row = 0
            for i in data:
                sheet.write(count_row,0, label = i[1])
                sheet.write(count_row,1, label = i[0])
                count_row += 1


        file_name = output_dir + '/AERE_RMSE_with_var_test_' + feature + '_mode_' + mode + resolution + '.xls'
        print(file_name)
        xls.save(file_name)
        print('excel has been created!')

    if denoise == 'off':
        excel_create(data = example, output_dir = output_path, feature = str(test_key), mode = 'original', resolution = '')
    if denoise == 'on':
        excel_create(data = worklist2, output_dir = output_path, feature = str(test_key), mode = mode, resolution = str(resolution))


if specific_example == 'off':
    # 将所有RMSE下数据绘制在同一张散点图上，每种RMSE一个颜色
    # 将AE和RE各11个RMSE_low的数据整理成{low:[[var/bias],[RMSE]]}
    # 记得确认数据对齐问题，这是dic到list的变化

    if energy == 'AE':
        work_dic = AE_dic# 也许需要降噪，为了方便修改，使用work_dic代替
        # 因为有11个RMSE，因此至少11个color
        color_marker = ['red', 'blue', 'green', 'orange', 'purple', 'maroon', 'navy', 'lime', 'fuchsia', 'aqua', 'goldenrod', ]
        AE_RMSElow_with_varlist_RMSElist = {}# 格式为{low:[[RMSE],[var],[mean],[bias square]]}
        for i in work_dic:
            T, low, high = i
            RMSElist = []
            varlist = []
            meanlist = []
            bias2list = []
            alllist = []
            for j in work_dic[i]:
                RMSElist.append(j[0])
                varlist.append(j[1])
                meanlist.append(j[2])
                bias2list.append(j[3])
            alllist.append(RMSElist)
            alllist.append(varlist)
            alllist.append(meanlist)
            alllist.append(bias2list)
            AE_RMSElow_with_varlist_RMSElist[low] = alllist
        sorted_RMSElist = sorted(AE_RMSElow_with_varlist_RMSElist.keys())
        color_count = 0
        if x_type == 'var':
            plt.xlabel('Vars',fontdict={"fontsize": 30})
            plt.ylabel('RMSE of ' + energy + ' (eV)',fontdict={"fontsize": 30})
            for i in sorted_RMSElist:# 格式为{low:[[RMSE],[var],[bias],[bias square]]}
                plt.scatter(AE_RMSElow_with_varlist_RMSElist[i][1], AE_RMSElow_with_varlist_RMSElist[i][0], marker = 'o', color = color_marker[color_count], s = 15, label = label_dic[i])
                color_count += 1
        if x_type == 'bias':
            plt.xlabel('Bias Square',fontdict={"fontsize": 30})
            plt.ylabel('RMSE of ' + energy + ' (eV)',fontdict={"fontsize": 30})
            for i in sorted_RMSElist:# 格式为{low:[[RMSE],[var],[bias],[bias square]]}
                plt.scatter(AE_RMSElow_with_varlist_RMSElist[i][3], AE_RMSElow_with_varlist_RMSElist[i][0], marker = 'o', color = color_marker[color_count], s = 15, label = label_dic[i])
                color_count += 1
        ax = plt.gca()  # 获得坐标轴的句柄
        LW = 2
        ax.spines['bottom'].set_linewidth(LW)  ###设置底部坐标轴的粗细
        ax.spines['left'].set_linewidth(LW)  ####设置左边坐标轴的粗细
        ax.spines['right'].set_linewidth(LW)  ###设置右边坐标轴的粗细
        ax.spines['top'].set_linewidth(LW)  ####设置上部坐标轴的粗细

        plt.tick_params(labelsize=23)
        font = {'family' : 'Arial',
        'weight' : 'bold',
        'size'   : 14,
}
        # plt.legend(loc = 'best', prop = font, markerscale = 4, ncol = 2, frameon = False)# 图例位置，文字字体属性，图例相对于原来的比例倍数，分n列表示，是否有边框
        plt.show()




    if energy == 'RE':      
        work_dic = RE_dic
        RE_RMSElow_with_varlist_RMSElist = {}
        color_marker = ['red', 'blue', 'green', 'orange', 'purple', 'maroon', 'navy', 'lime', 'fuchsia', 'aqua', 'goldenrod', ]
        for i in work_dic:
            T, low, high = i
            RMSElist = []
            varlist = []
            meanlist = []
            bias2list = []
            alllist = []
            for j in work_dic[i]:
                RMSElist.append(j[0])
                varlist.append(j[1])
                meanlist.append(j[2])
                bias2list.append(j[3])
            alllist.append(RMSElist)
            alllist.append(varlist)
            alllist.append(meanlist)
            alllist.append(bias2list)
            RE_RMSElow_with_varlist_RMSElist[low] = alllist
        sorted_RMSElist = sorted(RE_RMSElow_with_varlist_RMSElist.keys())
        color_count = 0
        if x_type == 'var':
            plt.xlabel('Vars',fontdict={"fontsize": 30})
            plt.ylabel('RMSE of ' + energy + ' (eV)',fontdict={"fontsize": 30})
            for i in sorted_RMSElist:# 格式为{low:[[RMSE],[var],[bias],[bias square]]}
                plt.scatter(RE_RMSElow_with_varlist_RMSElist[i][1], RE_RMSElow_with_varlist_RMSElist[i][0], marker = 'o', color = color_marker[color_count], s = 10, label = label_dic[i])
                color_count += 1
        if x_type == 'bias':
            plt.xlabel('Bias Square',fontdict={"fontsize": 30})
            plt.ylabel('RMSE of ' + energy + ' (eV)',fontdict={"fontsize": 30})
            for i in sorted_RMSElist:# 格式为{low:[[RMSE],[var],[bias],[bias square]]}
                plt.scatter(RE_RMSElow_with_varlist_RMSElist[i][3], RE_RMSElow_with_varlist_RMSElist[i][0], marker = 'o', color = color_marker[color_count], s = 10, label = label_dic[i])
                color_count += 1

        ax = plt.gca()  # 获得坐标轴的句柄
        LW = 2
        ax.spines['bottom'].set_linewidth(LW)  ###设置底部坐标轴的粗细
        ax.spines['left'].set_linewidth(LW)  ####设置左边坐标轴的粗细
        ax.spines['right'].set_linewidth(LW)  ###设置右边坐标轴的粗细
        ax.spines['top'].set_linewidth(LW)  ####设置上部坐标轴的粗细

        plt.tick_params(labelsize=23)
        font = {'family' : 'Arial',
        'weight' : 'bold',
        'size'   : 14,
}
        plt.legend(loc = 'best', prop = font, markerscale = 3.8, ncol = 2, frameon = False)# 图例位置，文字字体属性，图例相对于原来的比例倍数，分n列表示，是否有边框
        plt.show()

'''
x1 = [1, 2, 3, 4]
y1 = [1, 2, 3, 4]     #第一组数据

x2 = [1, 2, 3, 4]
y2 = [2, 3, 4, 5]    #第二组数据

n = 10
x3 = np.random.randint(0, 5, n)
y3 = np.random.randint(0, 5, n)   #使用随机数产生

plt.scatter(x1, y1, marker = 'x',color = 'red', s = 40 ,label = 'First')
#                   记号形状       颜色           点的大小    设置标签
plt.scatter(x2, y2, marker = '+', color = 'blue', s = 40, label = 'Second')
plt.scatter(x3, y3, marker = 'o', color = 'green', s = 40, label = 'Third')
plt.legend(loc = 'best')    # 设置 图例所在的位置 使用推荐位置

plt.show()  

'''