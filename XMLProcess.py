import xml.etree.ElementTree as ET
import os
import shutil

class XML:
    def __init__(self,annpath,filename):
        """
        构造函数
        :param annpath:输出目标文件夹路径
        :param filename: 图像文件名称
        """
        self.__annPath=annpath
        self.__fileName=filename
        self.__fileNameWithoutExt=filename.split(".")[0]
        self.__fullPath=""
        self.__outFlodar=""
        self.__outIndex=0           # 输出文件夹的序号，同时也是输出文件的名字
        self.__xmlFileName=""       # 输出的xml文件名
        self.__outImageNameWithoutExt=""    # 输出图片名称，不带扩展名
        self.__imageFlag=-1              # 标记True时候，表明该图像为正样本，-1为背景
        self.__textPath=""
        self.___setFileName()

    def setPath(self,path):
        """
        设置输出路径
        :param path:
        :return:
        """
        self.__annPath=path

    def setPicFileName(self,filename):
        """
        设置图像文件名称
        :param filename:
        :return:
        """
        self.__fileName=filename

    def ___setFileName(self):
        """
        设置输出文件名称
        :return:
        """
        self.__fullPath=self.__annPath+"/"+self.__fileName

        #读取配置文件中的目的路径
        with open("annotation.cfg", "r") as f:
            self.__outFlodar = f.readline()
            self.__outIndex = len(os.listdir(self.__outFlodar+"/VOC/Annotations/"))
            self.__xmlFileName = self.__outFlodar+"/VOC/Annotations/"+self.__fileNameWithoutExt+".xml"
            self.__outImageNameWithoutExt=self.__outFlodar+"/VOC/JPEGImages/"+self.__fileNameWithoutExt








    def StoreInfo(self,posinfo=[],picinfo=[]):
        """
        读取标记信息
        :param posinfo:
        :param picinfo:
        :return:
        """


        root = ET.Element("annotation")
        folder = ET.SubElement(root, "floder")
        folder.text = "VOC2012"
        source = ET.SubElement(root, "source")

        database = ET.SubElement(source, "database")
        database.text = "LUT,Haiyan Chen's works"
        sann = ET.SubElement(source, "annotation")
        sann.text = "LUT,Haiyan Chen's team"
        video = ET.SubElement(source, "video")
        video.text = ""  # 标记是否属于视频，若是属于一个视频，则写视频的名称
        frameNo = ET.SubElement(source, "frameIndex")
        frameNo.text = "0" # 如果是属于视频的，则在这里写上FrameNumber。

        self.__imageFlag=None   # 默认为负样本，只要图片中出现了属兔，则为正样本，

        for i in range(len(posinfo)):
            obj = ET.SubElement(root, "object")

            pos=posinfo[i]
            inf=picinfo[i]

            name=ET.SubElement(obj,"name")      #name
            name.text=inf[0]
            #标记样本为正负样本，-1为背景
            if inf[0]=="rats":
                self.__imageFlag=True
            elif inf[0]=="non":
                self.__imageFlag=-1


            trunc = ET.SubElement(obj, "truncated")
            if inf[1]==1:
                trunc.text='1'
            else:
                trunc.text='0'

            pose=ET.SubElement(obj,"pose")
            if inf[3]==0:
                pose.text="frontal"
            elif inf[3]==1:
                pose.text="side"
            elif inf[3]==2:
                pose.text="tail"
            else:
                pose.text="Unspecified"

            difficult=ET.SubElement(obj,"difficult")
            if inf[2]==-1:
                difficult.text='0'
            else:
                difficult.text='1'


            bndbox=ET.SubElement(obj,"bndbox")
            xmin=ET.SubElement(bndbox,"xmin")
            ymin=ET.SubElement(bndbox,"ymin")
            xmax=ET.SubElement(bndbox,"xmax")
            ymax=ET.SubElement(bndbox,"ymax")

            #Pascal 数据集中翻转了x,y
            xmin.text=str(int(pos[1]))
            ymin.text=str(int(pos[0]))
            xmax.text=str(int(pos[3]))
            ymax.text=str(int(pos[2]))



        tree = ET.ElementTree(root)
        #print(self.__xmlFileName)
        tree.write(self.__xmlFileName,encoding="utf-8",xml_declaration=True)
        # xml文件操作完毕
        self.__dealtext()

    def __dealtext(self):
        """
        追加 正负样本写入
        :return:
        """
        self.__textPath=self.__outFlodar+"/VOC/ImageSets/Main/rats_trainval.txt"
        with open(self.__textPath, "a") as f:
            if self.__imageFlag==True:
                flag=1
            elif self.__imageFlag==False:
                flag=-1
            else:
                flag=0
            f.write(self.__fileNameWithoutExt+"\t\t"+str(flag)+"\n")

    def savePic(self,image):
        """

        :return:
        """
        image.save(self.__outFlodar+"/VOC/JPEGImages/"+self.__fileNameWithoutExt+".jpg","JPG",100)

        shutil.move(self.__fullPath,self.__outFlodar+"/VOC/OriginalImages/"+self.__fileName)
