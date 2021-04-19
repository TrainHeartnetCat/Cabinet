import os

# 按照RMSE范围和范围内样本数建立文件夹，以及其子文件夹1
RMSE_group = [(0.1, 0.12), (0.12, 0.14), (0.14, 0.16), (0.16, 0.18), (0.18, 0.2), (0.2, 0.22), (0.22, 0.24), (0.24, 0.26), (0.26, 0.28), (0.28, 0.3)]# change
size = [2000]

for i in RMSE_group:
    for j in size:
        dir_name = ('RMSE_%s_%s_%ssizeN' % (i[0], i[1], j))
        # 要分开来写，不然一旦某个子文件夹已经建立就不再管其他的了
        try:
            os.makedirs('./' + dir_name + '/1')
        except:
            pass
        try:
            os.makedirs('./' + dir_name + '/1_path')
        except:
            pass
        try:
            os.makedirs('./' + dir_name + '/1_drc')
        except:
            pass
        try:
            os.makedirs('./' + dir_name + '/1_coverage')
        except:
            pass
        try:
            os.makedirs('./' + dir_name + '/1_rate')
        except:
            pass

            
            
            