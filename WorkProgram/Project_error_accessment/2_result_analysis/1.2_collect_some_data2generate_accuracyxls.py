# coding:utf-8
# 请用python2.7

from __future__ import division
import os
import pickle
import numpy as np
import xlwt
import datetime

print('Please run in python2.7')

data_file = r'D:\Works\backup\Project01_ErrorEstimate_DRM_on_Ni111\1_ouput_data\Raw_output\2000sizeN1023Some_data_collect.pkl'
# dic_outputpkl = {(t, low, high):[{order:[energy]}, {'species':number}, {'species':number}, {hash:number}, array([mpf])]. ...}


size = '2000'
tee = '1023_third'
excel_output_path = './'

tmp = [1023]# change
rmse = [0.1,0.12,0.14,0.16,0.18,0.2,0.22,0.24,0.26,0.28,0.3]# change
energyfile_num = 2000

# # primary
# correct_coverage = 'CO_s'# change
# correct_DRC = 'dCH4_g/dCH-O_s'# change
# # correct_DRC = 'dCH4_g/dCO-O_s'# 973&1023
# correct_path_hash = 8970982363099074994# change

# second
# correct_coverage = 'CH_s'# change
# correct_DRC = 'dCH4_g/dCH-O_s'# 973&1023
# # correct_DRC = 'dCH4_g/dCO-O_s'# 923
# correct_path_hash = -2769364537630630541# change

# third
correct_coverage = 'CH_s'# change
correct_DRC = 'dCH4_g/dCH3-H_s'# 973&1023
# correct_DRC = 'dCH4_g/dCO-O_s'# 923
correct_path_hash = -2769364537630630541# change

def excel_create(data_file, output_dir, tmp, rmse, correct_path_hash, correct_coverage, correct_DRC, energyfile_num):
    xls = xlwt.Workbook(encoding = 'utf-8')
    sheet_path = xls.add_sheet('path_analysis')
    sheet_coverage = xls.add_sheet('coverage_analysis')
    sheet_drc = xls.add_sheet('drc_analysis')

    with open(data_file,'rb') as f:
            data_dic = pickle.load(f)

    print('there is ' + str(len(data_dic)) + ' groups data')

    sheet_path.write(0,0, label = correct_path_hash)# 行 列 值
    sheet_coverage.write(0,0, label = correct_coverage)# 行 列 值
    sheet_drc.write(0,0, label = correct_DRC)# 行 列 值

    for i in range(len(tmp)):
        sheet_path.write(0,i+1, label = tmp[i])# 行 列 值
        sheet_coverage.write(0,i+1, label = tmp[i])# 行 列 值
        sheet_drc.write(0,i+1, label = tmp[i])# 行 列 值
        sheet_path.write(0,i+4, label = str(tmp[i])+'_correct_sample')# 行 列 值
        sheet_coverage.write(0,i+4, label = str(tmp[i])+'_correct_sample')# 行 列 值
        sheet_drc.write(0,i+4, label = str(tmp[i])+'_correct_sample')# 行 列 值
        sheet_path.write(0,i+7, label = str(tmp[i])+'_all_sample')# 行 列 值
        sheet_coverage.write(0,i+7, label = str(tmp[i])+'_all_sample')# 行 列 值
        sheet_drc.write(0,i+7, label = str(tmp[i])+'_all_sample')# 行 列 值

    for i in range(len(rmse)):
        sheet_path.write(i+1,0, label = rmse[i])# 行 列 值
        sheet_coverage.write(i+1,0, label = rmse[i])# 行 列 值
        sheet_drc.write(i+1,0, label = rmse[i])# 行 列 值


    # # 直接除2000
    # for i in data_dic:
    #     for j in range(len(tmp)):
    #         if i[0] == tmp[j]:           
    #             for k in range(len(rmse)):
    #                 if i[1] == rmse[k]:
    #                     sheet_path.write(k+1,j+1, label = data_dic[i][3][correct_path_hash]/energyfile_num)# 行 列 值
    #                     sheet_coverage.write(k+1,j+1, label = data_dic[i][1][correct_coverage]/energyfile_num)# 行 列 值
    #                     sheet_drc.write(k+1,j+1, label = data_dic[i][2][correct_DRC]/energyfile_num)# 行 列 值

    for i in data_dic:
        l_coverage = []
        l_drc = []
        for j in range(len(tmp)):
            if i[0] == tmp[j]:           
                for k in range(len(rmse)):
                    if i[1] == rmse[k]:
                        for every_coverage in data_dic[i][1]:
                            l_coverage.append(data_dic[i][1][every_coverage])
                        coverage_sum = sum(l_coverage)
                        for every_DRC in data_dic[i][2]:
                            l_drc.append(data_dic[i][2][every_DRC])
                        Drc_sum = sum(l_drc)
                        sheet_path.write(k+1,j+1, label = data_dic[i][3][correct_path_hash]/energyfile_num)# 行 列 值
                        sheet_coverage.write(k+1,j+1, label = data_dic[i][1][correct_coverage]/energyfile_num)# 行 列 值
                        sheet_drc.write(k+1,j+1, label = data_dic[i][2][correct_DRC]/energyfile_num)# 行 列 值
                        sheet_path.write(k+1,j+4, label = data_dic[i][3][correct_path_hash])# 行 列 值
                        sheet_coverage.write(k+1,j+4, label = data_dic[i][1][correct_coverage])# 行 列 值
                        sheet_drc.write(k+1,j+4, label = data_dic[i][2][correct_DRC])# 行 列 值
                        sheet_path.write(k+1,j+7, label = energyfile_num)# 行 列 值
                        sheet_coverage.write(k+1,j+7, label = coverage_sum)# 行 列 值
                        sheet_drc.write(k+1,j+7, label = Drc_sum)# 行 列 值

    xls.save(output_dir + '/accuracy_plot_' + size + '_' + tee + '_{0:%Y%m%d%H%M%S}'.format(datetime.datetime.now()) +  '.xls')
    print('excel has been created!')



excel_create(data_file, excel_output_path, tmp, rmse, correct_path_hash, correct_coverage, correct_DRC, energyfile_num)
