import cv2
import os

# a decline of image quality with no shrink of resolutions of images 
def image_quality_compression_in_batch(input_path, output_path, image_type):
    file_list = os.listdir(input_path)
    for i in file_list:
        if ".py" in i:
            continue
        elif i == "output":
            continue
        else:
            #加一个获取文件后缀检查在不在
            file = input_path + "/" + i
            if os.path.splitext(file)[-1] in image_type:
                output_file = output_path + '/' + i
                print(file)
                img = cv2.imread(file, 1)
                height = img.shape[0]
                width = img.shape[1]
                shrink = cv2.resize(img, (width, height), interpolation = cv2.INTER_AREA)# this step should be kept due to the feature of openCV
                cv2.imwrite(output_file, shrink, [cv2.IMWRITE_JPEG_QUALITY, 50])# default quality is 50, please set your target quality
            


if __name__ == '__main__':
    # input, please check your file type carefully;
    # only image type files contained in your file_path is strongly adviced
    file_path = "."
    output_path = file_path + "/output"
    image_type = [".jpg", ".png"]# please keep an eye on case sensitive matching
    try:
        os.mkdir(output_path)
    except:
        pass
    image_quality_compression_in_batch(file_path, output_path, image_type)


