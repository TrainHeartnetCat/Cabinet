import re
import os
import shutil

dir_path = './'
check_type = '1/finalRunParallel.py'

analysis_subject = ['1', '1_path', '1_coverage', '1_drc', '1_rate']
# analysis_subject = ['1_path', '1_coverage', '1_drc', '1_rate']

# 本来想全部批量替换，但发现这没有必要，直接手动固定tmp, size《 dir等内容，只需要脚本修改dir中的RMSE范围即可,这样可以避免花很长时间建立关系网。
# 如果未来想实现全部对应批量修改，那么需要建立一个非常复杂的关系网，然后在大概50行附近进行修改
# change_dic = {'1':[''],
#               '1_path':['# change tmp', '# change pressure', '# change dir', '# change size and tmp_pressure'], 
#               '1_coverage':[], 
#               '1_drc':[], 
#               '1_rate':[]}
# relationship = {'1_path# change dir':''}


change_dic = {'1':['# change dir'],
              '1_path':['# change dir'], 
              '1_coverage':['# change dir'], 
              '1_drc':['# change dir'], 
              '1_rate':['# change dir']}

dirs = os.listdir(dir_path)
for i in dirs:
    for j in analysis_subject:
        if 'RMSE' in i:
            file_name_parts = i.split('_')
            target_range = file_name_parts[-3] + '_' + file_name_parts[-2]
            subject = dir_path + '/' + i + '/' + j
            script_path = dir_path + '/' + j
            scripts = os.listdir(script_path)
            print(i + '     ' + j)
            for k in scripts:# subject下每个脚本，一般是一个py脚本和一个上传脚本
                if '.py' in k:
                    with open(script_path + '/' + k, 'r') as f:
                        content = f.readlines()
                    work = []
                    for l in content:
                        for o in change_dic[j]:
                            if re.search(o, l):# 找到目标内容，并替换，然后写入list
                                if j == '1':
                                    part = l.split('/')
                                    part_in_part = part[-1].split('_')
                                    origin_range = part_in_part[-3] + '_' + part_in_part[-2]
                                    l = re.sub(origin_range, target_range, l)
                                    work.append(l)
                                else:
                                    part = l.split('/')
                                    part_in_part = part[-2].split('_')
                                    origin_range = part_in_part[-3] + '_' + part_in_part[-2]
                                    l = re.sub(origin_range, target_range, l)
                                    work.append(l)
                            else:# 不需要替换的直接写入list
                                work.append(l)
                    new_content = "".join(work)
                    with open(script_path + '/' + k, 'w') as f:
                        f.write(new_content)
                    source_py = script_path + '/' + k
                    target_py = subject + '/' + k
                    shutil.copy(source_py, target_py)

                if 'SubmitOnHPC' in k:# 这是个需要unix格式的文件
                    with open(script_path + '/' + k, 'rb') as f:
                        content = f.readlines()
                    work = []
                    for l in content:
                        l = str(l, encoding = 'utf-8')
                        if re.search('-N', l):
                            part = l.split('_')
                            origin_range = part[-2] + '_' + part[-1]
                            l = re.sub(origin_range, target_range, l)
                            l = l + '\n'
                            work.append(l)
                        else:
                            work.append(l)
                    new_content = bytes("".join(work), encoding = 'utf-8')
                    with open(script_path + '/' + k, 'wb') as f:
                        f.write(new_content)
                    source_py = script_path + '/' + k
                    target_py = subject + '/' + k
                    shutil.copy(source_py, target_py)
