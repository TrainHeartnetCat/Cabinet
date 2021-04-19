# coding:utf-8
'''
pickle文件数据：
# dic_outputpkl = {
(t, low, high):
[
{order_int:[energy]},
{order:path_hash},
{order_int:(species_str, coverage_str)},
{order_int:(step_str, drc_rate_str)},
{order:rate}, # 注意rate是log后的值
{rate_rmse:rmse}]
, ...}

'''
import warnings
import pickle
import json
import numpy as np
import tqdm
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import pandas as pd
from matplotlib.pyplot import MultipleLocator
from matplotlib.ticker import FuncFormatter


plt.rc('font',family='Arial')
plt.rc('font',weight="bold")


# 这里设置各个温度下的正确的路径hash，DRC，coverage以及正确的rate
with open('./All_data_with_order_collect_923_1023_2000sizeN.json', "r") as f:
    data = json.load(f)

ENSEMBLE_NUM = 2000  # 一个温度和误差条件下的样本数目
CORRECT_PATH = {
    923: 8970982363099074994,
    973: 8970982363099074994,
    1023: 8970982363099074994
}
CORRECT_DRC = {
    923: "dCH4_g/dCH-O_s",
    973: "dCH4_g/dCO-O_s",
    1023: "dCH4_g/dCO-O_s"
}
CORRECT_COVERAGE = {
    923: "CO_s",
    973: "CO_s",
    1023: "CO_s"
}
CORRECT_RATE = {
    923: 0.79941843,
    973: 1.531501883,
    1023: 1.929111939
}
# 收集各个温度，RMSE下，以error的mean和var为key，结果作为value
error_mv_to_path = {}
error_mv_to_drc = {}
error_mv_to_coverage = {}
error_mv_to_rate = {}

for key in data:

    tuple_key = eval(key)  # 通过eval把tuple字符串转成tuple
    temperature, RMSE_min, RMSE_max = tuple_key
    correct_energy, \
    order_to_energy, \
    order_to_path, \
    order_to_species_str_and_coverage, \
    order_to_rxn_str_and_drc, \
    order_to_log_rate, \
    rmse = data[key]

    correct_energy = np.array(correct_energy)

    # 这里面以mean和var作为key，以原来的预测结果作为value
    error_mv_to_path[tuple_key] = dict()
    error_mv_to_drc[tuple_key] = dict()
    error_mv_to_coverage[tuple_key] = dict()
    error_mv_to_rate[tuple_key] = dict()

    invalid_num = 0
    for i in range(2000):
        try:
            i = str(i)
            target_path = order_to_path[i]
            target_drc = order_to_rxn_str_and_drc[i][0][0]
            target_coverage = order_to_species_str_and_coverage[i][0]
            target_rate = order_to_log_rate[i]
            target_energy = order_to_energy[i]
        except TypeError:
            invalid_num += 1
            continue
        except KeyError:
            invalid_num += 1
            continue
        if target_path is None or target_drc is None or target_coverage is None or target_rate is None:
            invalid_num += 1
            continue

        error = np.array(target_energy) - correct_energy
        mean = float(np.mean(error))
        var = float(np.var(error))
        error_mv_to_path[tuple_key][(mean, var)] = target_path
        error_mv_to_drc[tuple_key][(mean, var)] = target_drc
        error_mv_to_coverage[tuple_key][(mean, var)] = target_coverage
        error_mv_to_rate[tuple_key][(mean, var)] = target_rate


# 然后进行2d plot

def mv_to_accuracy_plot(mv_to_label_dict,  # mean和var作为key，预测结果作为value
                        correct_label,  # 正确的值
                        resolution=10,  # 绘图的格点数目
                        sample_num_limit=20,  # 样本数目限制：如果某个个点数目低于这个值，直接设置为没有样本，避免小样本导致的大波动
                        plot_sample_num_distrib=False,
                        plot_accuracy_or_RMSE_distrib=True,
                        title="None", colorbar_range=None
                        ):
    '''
    这里面的代码解释详见 old_2d_analysis_mean_and_var_of_error_to_accuracy.py
    :param mv_to_label_dict:
    :param correct_label:
    :param resolution:
    :return:
    '''
    means = []
    vars = []
    for key in mv_to_label_dict:
        mean, var = key
        means.append(mean)
        vars.append(var)
    means_min, means_max = np.min(means), np.max(means)
    means_delta = (means_max - means_min) / resolution

    vars_min, vars_max = np.min(vars), np.max(vars)
    vars_delta = (vars_max - vars_min) / resolution

    pos_data = dict()
    # 每个位置的数据，用dict存储
    for x in range(resolution + 1):
        for y in range(resolution + 1):
            pos_data[(x, y)] = []

    # 用上述方法得到每个位置的hash数据
    for key in mv_to_label_dict:
        mean, var = key
        # 这里使用round，四舍五入，代替int，可以解决不对称问题
        x = round((mean - means_min) / means_delta)
        y = round((var - vars_min) / vars_delta)
        pos_data[x, y].append(mv_to_label_dict[key])

    pos_num = dict()
    for xy in pos_data:
        pos_num[xy] = len(pos_data[xy])
    pos_accuracy = dict()

    # 得到目标hash值的accuracy，或者误差的RMSE
    for xy in pos_data:
        hashs = pos_data[xy]
        if len(hashs) < sample_num_limit:  # 没有数据点，设置成2，因为accuracy不可能超过1，超过可以看成无效
            pos_accuracy[xy] = None
            continue
        if isinstance(correct_label, float):  # 回归任务
            warnings.warn("正确标签为float，按照回归任务处理")
            errors_ = []
            for h in hashs:
                errors_.append(h - correct_label)
            pos_accuracy[xy] = np.sqrt(np.mean(np.square(errors_)))
        else:
            warnings.warn("正确标签为string或int，按照分类任务处理")
            count = 0
            for h in hashs:
                if h == correct_label: count += 1
            pos_accuracy[xy] = count / pos_num[xy]

    def pos_dict_data_to_2d_array(dict_):
        '''
        把位置的dict转成二维矩阵
        :param dict_:
        :return:
        '''
        xs = []
        ys = []
        for xy in dict_:
            xs.append(xy[0])
            ys.append(xy[1])
        matrix = np.zeros(shape=(np.max(xs) + 1, np.max(ys) + 1))
        for xy in dict_:
            matrix[xy[0], xy[1]] = dict_[xy]
        return matrix

    pos_num = pos_dict_data_to_2d_array(pos_num)
    pos_accuracy = pos_dict_data_to_2d_array(pos_accuracy)
    if plot_sample_num_distrib:
        plt.close()
        plt.imshow(pos_num)
        plt.colorbar()
        plt.xlabel("Sample count distribution")
        plt.show()
    if plot_accuracy_or_RMSE_distrib:
        plt.figure(figsize=(10, 10))
        ax = plt.gca()  # 获得坐标轴的句柄
        LW = 3
        tick_font_size = 25
        ax.spines['bottom'].set_linewidth(LW)  ###设置底部坐标轴的粗细
        ax.spines['left'].set_linewidth(LW)  ####设置左边坐标轴的粗细
        ax.spines['right'].set_linewidth(LW)  ###设置右边坐标轴的粗细
        ax.spines['top'].set_linewidth(LW)  ####设置上部坐标轴的粗细
        ax.tick_params(width=LW,
                       labelsize=tick_font_size)
        plt.ylabel("Bias", fontdict={"fontsize": tick_font_size + 5})
        plt.xlabel("Variance", fontdict={"fontsize": tick_font_size + 5})

        # 坐标轴刻度映射
        def changex(temp, position):
            return "%.2f" % (vars_min + temp * vars_delta)

        def changey(temp, position):
            return "%.2f" % (means_min + temp * means_delta)

        ax.xaxis.set_major_formatter(FuncFormatter(changex))
        ax.yaxis.set_major_formatter(FuncFormatter(changey))

        plt.imshow(pos_accuracy, cmap="rainbow")

        cb = plt.colorbar(fraction=0.046, pad=0.04)

        if colorbar_range is not None:
            cb.set_clim(colorbar_range[0], colorbar_range[1])

        cb.ax.tick_params(labelsize=tick_font_size)

        plt.title("%s\nAccuracy distribution\n min var, max var is %.2f %.2f\n min mean, max mean is %.2f %.2f" % (
            title,
            vars_min, vars_max, means_min, means_max
        ), fontdict={"fontsize": 30})



        # 绘制RMSE曲线
        target_RMSE = [0.1,
                       0.12,
                       0.14,
                       0.16,
                       0.18,
                       0.2,
                       0.22,
                       0.24,
                       0.26,
                       0.28,
                       0.3
                       ]
        '''
        曲线方程是
        MSE(x) = var(x) + bias(x)^2
        也就是RMSE^2 = x + y^2
        即 x = RMSE^2 - y^2
        于是先在var min到var max上取点，求出相应的x，然后映射回格点的数目 （也可以覆盖另一图层？）
        '''
        point_num = 100
        for i in range(len(target_RMSE)):
            trmse = target_RMSE[i]
            y = np.linspace(means_min,means_max,point_num)
            x = trmse**2 - y**2
            # 映射回格点坐标系
            y = (y-means_min) / means_delta
            x = (x-vars_min) / vars_delta

            # 中间的标签，采用间隔取点
            line_alpha = 0.5
            LW_ = 2
            if i % 2 == 0:
                if trmse == 0.3:
                    plt.text(x[point_num // 2]-1, # 后面加减的数字是位置微调
                             y[point_num // 2]-0.5,
                             str(trmse),fontdict={"fontsize":25})
                    # print(x[point_num // 2 + break_n:])
                    # print(y[point_num // 2 + break_n:])
                    # exit(0)
                    # 采用线段打断，左右打断break_n
                    break_n = 2
                    plt.plot(np.array([-0.90398, -0.20969298, 0.48469125,  1.19356577,  1.88795001,  2.56784396,  3.23324763,  3.88416102,
  4.52058412,  5.14251694,  5.74995947,  6.34291172,  6.92137369,  7.48534537,
  8.03482677,  8.56981788,  9.09031871,  9.59632926, 10.08784952, 10.5648795,
 11.02741919, 11.4754686 , 11.90902773, 12.32809657, 12.73267513, 13.1227634,
 13.49836139, 13.8594691 , 14.20608652, 14.53821366, 14.85585051, 15.15899708,
 15.44765337, 15.72181937, 15.98149509, 16.22668052, 16.45737567, 16.67358054,
 16.87529512, 17.06251942, 17.23525343, 17.39349717, 17.53725061, 17.66651377,
 17.78128665, 17.88156925, 17.96736156, 18.03866358, 18.09547533, 18.13779678,]),
                             np.array([-0.363636, -0.181818, 0.       ,  0.18181818, 0.36363636, 0.54545455, 0.72727273, 0.90909091,
 1.09090909, 1.27272727, 1.45454545, 1.63636364, 1.81818182, 2.,
 2.18181818, 2.36363636, 2.54545455, 2.72727273, 2.90909091, 3.09090909,
 3.27272727, 3.45454545, 3.63636364, 3.81818182, 4.        , 4.18181818,
 4.36363636, 4.54545455, 4.72727273, 4.90909091, 5.09090909, 5.27272727,
 5.45454545, 5.63636364, 5.81818182, 6.        , 6.18181818, 6.36363636,
 6.54545455, 6.72727273, 6.90909091, 7.09090909, 7.27272727, 7.45454545,
 7.63636364, 7.81818182, 8.        , 8.18181818, 8.36363636, 8.54545455,]), lw=LW_, c="black",alpha=line_alpha)
                    plt.plot(np.array([18.13204982, 18.08742957, 18.02831904, 17.95471823, 17.86662713, 17.76404575,
 17.64697409, 17.51541214, 17.3693599 , 17.20881739, 17.03378458, 16.8442615,
 16.64024813, 16.42174448, 16.18875054, 15.94126632, 15.67929181, 15.40282702,
 15.11187195, 14.80642659, 14.48649095, 14.15206503, 13.80314882, 13.43974233,
 13.06184555, 12.66945849, 12.26258114, 11.84121351, 11.4053556 , 10.9550074,
 10.49016892, 10.01084016,  9.51702111,  9.00871178,  8.48591216,  7.94862226,
  7.39684208,  6.83057161,  6.24981085,  5.65455982,  5.0448185 ,  4.42058689,
  3.781865  ,  3.12865283,  2.46095037,  1.77875763,  1.08207461,  0.3709013 , -0.34027, -1.05144]),
                             np.array([ 9.45454545,  9.63636364,  9.81818182, 10.        , 10.18181818, 10.36363636,
 10.54545455, 10.72727273, 10.90909091, 11.09090909, 11.27272727, 11.45454545,
 11.63636364, 11.81818182, 12.        , 12.18181818, 12.36363636, 12.54545455,
 12.72727273, 12.90909091, 13.09090909, 13.27272727, 13.45454545, 13.63636364,
 13.81818182, 14.        , 14.18181818, 14.36363636, 14.54545455, 14.72727273,
 14.90909091, 15.09090909, 15.27272727, 15.45454545, 15.63636364, 15.81818182,
 16.        , 16.18181818, 16.36363636, 16.54545455, 16.72727273, 16.90909091,
 17.09090909, 17.27272727, 17.45454545, 17.63636364, 17.81818182, 18.        , 18.181819, 18.363637]), lw=LW_, c="black",alpha=line_alpha)
                else:
                    plt.text(x[point_num // 2]-1, # 后面加减的数字是位置微调
                             y[point_num // 2]-0.5,
                             str(trmse),fontdict={"fontsize":25})
                    # 采用线段打断，左右打断break_n
                    break_n = 2
                    plt.plot(x[:point_num//2-break_n],
                             y[:point_num//2-break_n], lw=LW_, c="black",alpha=line_alpha)
                    plt.plot(x[point_num // 2 + break_n:],
                             y[point_num // 2 + break_n:], lw=LW_, c="black",alpha=line_alpha)
            else:
                plt.plot(x, y, lw=LW_,
                         c="black",alpha=line_alpha)
        plt.xlim(-0.5,resolution+1)
        plt.ylim(-1.2,19.2)

        new_ticks = np.linspace(-0.2,18.2, 5)
        plt.yticks(new_ticks)




        plt.savefig("temp.png", dpi=300)
        plt.show()


if __name__ == '__main__':

    '''
    NOTICE:
    resolution只能设置成偶数，因为程序里面还会把resolution+1，如果左边最中间的Mean不等于0.0，就调整resolution，加1或者减去1变成偶数
    注意，虽然colorbar的值域不一样，但是颜色和数值是对应的，使用第一个温度的图的colorbar就行了
    
    作图标准化流程：
    目的：matplotlib有时候做的图需要使用ppt修改横纵坐标等，为了防止替换图片时增加额外工作量
    1 使用专业版pycharm，直接复制SciView里面显示的图片
    2 粘贴进入ppt，使用图片工具-格式-高度，统一所有的图的高度
    3 多张图片尽量无缝排列，一旦完成排列过后，位置不再更改
    4 如果有图需要替换，按照1~3流程作下来不会有额外工作量
    
    '''
    # TODO: 能不能在图中增加RMSE等高线

    # 绘图方式
    # PLOT_WAY = 1  # 第一种方式：每一种温度每一个RMSE都绘制一下，有很多张图
    PLOT_WAY = 2  # 第二种方式：每种温度一个图

    # 绘制目标，也就是DATA_SETTINGS里面的Key
    Target = "Rate"

    # 数据设定，主要是针对不同的需求，一般确定了过后就不修改了
    DATA_SETTINGS = {

        "Path": dict(data_source=error_mv_to_path,  # 数据来源：绘制path的误差，drc的误差还是rate等的
                     correct_label_source=CORRECT_PATH,  # 正确的label数据来源，要和上面的数据来源对应
                     title="Path",
                     colorbar_range=(0.1, 1)  # colorbar的范围，先设置成None来查看各个图的合适范围，最后设置具体范围
                     # 注意虽然colorbar显示的范围不同，但是颜色和数值对应的，只要set clim相同
                     ),
        "DRC": dict(data_source=error_mv_to_drc,
                    correct_label_source=CORRECT_DRC,
                    title="DRC", colorbar_range=(0, 1)
                    ),
        "Coverage": dict(data_source=error_mv_to_coverage,
                         correct_label_source=CORRECT_COVERAGE,
                         title="Coverage", colorbar_range=(0.1, 1)),
        "Rate": dict(data_source=error_mv_to_rate,
                     correct_label_source=CORRECT_RATE,
                     title="Rate", colorbar_range=(0.0, 5.0)),

    }

    DATA_SOURCE = DATA_SETTINGS[Target]["data_source"]
    CORRECT_LABEL_SOURCE = DATA_SETTINGS[Target]["correct_label_source"]

    if PLOT_WAY == 1:
        for key in DATA_SOURCE:
            mv_to_accuracy_plot(DATA_SOURCE[key],
                                CORRECT_LABEL_SOURCE[key[0]],
                                resolution=13,
                                sample_num_limit=5)
    elif PLOT_WAY == 2:
        for t in [923, 973, 1023]:
            total_data = dict()
            for key in DATA_SOURCE:
                if key[0] == t:
                    total_data.update(DATA_SOURCE[key])
            mv_to_accuracy_plot(total_data,
                                CORRECT_LABEL_SOURCE[t],
                                sample_num_limit=1,
                                resolution=18,# path18
                                title=DATA_SETTINGS[Target]["title"],
                                colorbar_range=DATA_SETTINGS[Target]["colorbar_range"])
