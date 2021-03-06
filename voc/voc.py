from __future__ import division
import os
from PIL import Image
import xml.dom.minidom
import numpy as np
import math
import concurrent.futures


# 未处理图片的存放路径
JpgPath = r'C:/Users/ouyuming/Desktop/voc_tool/VOCdevkit/VOC2012/JPEGImages/'
# 处理后图片的存放路径
ProcessedPath = r'C:/Users/ouyuming/Desktop/exercise/'
#xml的存放路径
AnnoPath = r'C:/Users/ouyuming/Desktop/voc_tool/VOCdevkit/VOC2012/Annotations/'


#获取图片
def get_image(file_name):
    image_name, ext = os.path.splitext(file_name) #分割路径中的文件名与拓展名
    imgfile = JpgPath + file_name #拼接图片的路径，找到指定路径
    print('正在处理图像:'+ imgfile)
    xmlfile = AnnoPath + image_name + '.xml' #找到待拼接图片的xml存储路径
    print('正在处理XML:' + xmlfile)
    DomTree = xml.dom.minidom.parse(xmlfile) #将所有元素保存在树结构里
    annotation = DomTree.documentElement
    objectlist = annotation.getElementsByTagName('object')
    return objectlist,imgfile,image_name

#切割图片
def cut_img(objectlist,imgfile,image_name):
    i = 0
    for objects in objectlist:
        namelist = objects.getElementsByTagName('name')
        objectname = namelist[0].childNodes[0].data #获取类型名称
        savepath = ProcessedPath + objectname #分类保存路径
        if not os.path.exists(savepath): #路径不存在则创建路径
            os.makedirs(savepath)
        bndboxs = objects.getElementsByTagName('bndbox') #通过bndbox标签获取切割四个坐标
        x1_list = bndboxs[0].getElementsByTagName('xmin')
        x1 = math.ceil(float(x1_list[0].childNodes[0].data)) #获取x轴最小坐标
        y1_list = bndboxs[0].getElementsByTagName('ymin')
        y1 = math.ceil(float(y1_list[0].childNodes[0].data)) #获取y轴最小坐标
        x2_list = bndboxs[0].getElementsByTagName('xmax')
        x2 = math.ceil(float(x2_list[0].childNodes[0].data)) #获取x轴最大坐标
        y2_list = bndboxs[0].getElementsByTagName('ymax')
        y2 = math.ceil(float(y2_list[0].childNodes[0].data)) #获取y轴最大坐标
        crop_box = np.array([x1, y1, x2, y2]) #获取坐标数组
        img = Image.open(imgfile) #打开图片
        cropedimg = img.crop(crop_box) #根据数组坐标裁剪图片(pillow模块Image.crop()函数切割图片)
        i += 1 #每张图片里面，对象的个数
        print(str(i))
        cropedimg.save(savepath + '/' + image_name + '_' + str(i) + '.jpg') #保存在给定文件名下的该图像



if __name__ == '__main__':
    image_list = os.listdir(JpgPath)  # 拿到JpgPath路径下的所有图片
    #with concurrent.futures.ProcessPoolExecutor() as executor: #多线程执行
       # executor.map(get_image, image_list)
    objectlist, imgfile, image_name = get_image(image_list)
    cut_img(objectlist, imgfile, image_name)
    print('图片获取完成 。。。！')




