import cv2
import os


# 此次图片常规规格(从外到内)：
# 左x：600~681~685~689
# 下y：718~688~684~681
# 右x：1281~1278
# 上y：89~94

dir_path = r'D:\Works\backup\Project01_ErrorEstimate_DRM_on_Ni111\4_others\pic\org\3d\raw'
output = r'D:\Works\backup\Project01_ErrorEstimate_DRM_on_Ni111\4_others\pic\org\3d'
for i in os.listdir(dir_path):
    if 'spsp' in i:# 单独裁剪用的，特定目标
        img = cv2.imread(dir_path+'/'+i,1)
        dst = img[:281, :267]
        cv2.imwrite(output+'/'+'cut_'+i,dst)
    if 'cut_' in i:# 如果裁剪范围超过图片自身像素，IMwrite的时候会报错
        continue
    else:
        img = cv2.imread(dir_path+'/'+i,1)
        if 'LR' in i:
            dst = img[91:682, 139:1384]
        if 'LA' in i:
            dst = img[91:715, 139:1384]

        # 裁剪坐标为[y0:y1, x0:x1]
        if 'RE' in i:
            dst = img[89:718, 628:1281]# RE保留全部轴以及坐标
        if 'AE' in i:
            dst = img[89:688, 716:1281]# AE保留上轴、右轴、下坐标
        if 'variance' in i:
            if 'ax' in i:
                dst = img[691:718, 698:1196]# 加上下轴的坐标轴
            # else:
            #     dst = img[691:718, 667:1260]# 截取横轴坐标数字
        if 'bias' in i:
            pass
        if 'bar' in i:
            if 'REAE' in i:
                dst = img[91:684, 1328:1414]# 截取color_bar
            if 'accuracy' in i:
                dst = img[78:696, 1328:1414]
            if 'rate' in i:
                dst = img[91:684, 1328:1414]
        if 'c1' in i:
            if 'r4' in i:
                dst = img[89:718,629:1278]# 截取f2图中第一列最后一行所需图，保留左坐标、下坐标和上轴
            else:
                dst = img[89:681,629:1278]# 截取f2图中第一列其他行所需图，保留左坐标和上轴
        if 'c2' in i:
            if 'r4' in i:
                dst = img[89:688,713:1278]# 截取f2图中第二列最后一行所需图，保留下坐标和上轴、左轴
            else:
                dst = img[89:681,713:1278]# 截取f2图中第二列其他行所需图，保留上轴、左轴
        if 'c3' in i:
            if 'r4' in i:
                dst = img[89:688,713:1281]# 截取f2图中第二列最后一行所需图，保留下坐标和上轴、左轴、右轴
            else:
                dst = img[89:681,713:1281]# 截取f2图中第二列其他行所需图，保留左坐标和上轴、左轴、右轴


        # dst = img[89:681, 694:1281]# 保留左坐标、上轴、右轴
        # dst = img[89:681, 701:1281]# 保留上轴、右轴

        cv2.imwrite(output+'/'+'cut_'+i,dst)



'''
for i in os.listdir(dir_path):
    if 'spsp' in i:# 单独裁剪用的，特定目标
        img = cv2.imread(dir_path+'/'+i,1)
        dst = img[:281, :267]
        cv2.imwrite(output+'/'+'cut_'+i,dst)
    if 'cut_' in i:# 如果裁剪范围超过图片自身像素，IMwrite的时候会报错
        continue
    else:
        img = cv2.imread(dir_path+'/'+i,1)

        # 裁剪坐标为[y0:y1, x0:x1]
        if 'RE' in i:
            dst = img[89:718, 600:1281]# RE保留全部轴以及坐标
        if 'AE' in i:
            dst = img[89:688, 689:1281]# AE保留上轴、右轴、下坐标
        if 'variance' in i:
            if 'ax' in i:
                dst = img[681:688, 684:1281]# 加上下轴的坐标轴
            else:
                dst = img[691:718, 667:1260]# 截取横轴坐标数字
        if 'bias' in i:
            pass
        if 'bar' in i:
            if 'REAE' in i:
                dst = img[91:684, 1328:1414]# 截取color_bar
            if 'accuracy' in i:
                dst = img[78:696, 1328:1414]
            if 'rate' in i:
                dst = img[91:684, 1328:1414]
        if 'c1' in i:
            if 'r4' in i:
                dst = img[89:718,600:1278]# 截取f2图中第一列最后一行所需图，保留左坐标、下坐标和上轴
            else:
                dst = img[89:681,600:1278]# 截取f2图中第一列其他行所需图，保留左坐标和上轴
        if 'c2' in i:
            if 'r4' in i:
                dst = img[89:688,685:1278]# 截取f2图中第二列最后一行所需图，保留下坐标和上轴、左轴
            else:
                dst = img[89:681,685:1278]# 截取f2图中第二列其他行所需图，保留左坐标和上轴、左轴
        if 'c3' in i:
            if 'r4' in i:
                dst = img[89:688,685:1281]# 截取f2图中第二列最后一行所需图，保留下坐标和上轴、左轴、右轴
            else:
                dst = img[89:681,685:1281]# 截取f2图中第二列其他行所需图，保留左坐标和上轴、左轴、右轴


        # dst = img[89:681, 694:1281]# 保留左坐标、上轴、右轴
        # dst = img[89:681, 701:1281]# 保留上轴、右轴


'''