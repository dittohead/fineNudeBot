import os
import conf
import shutil


a=os.listdir(conf.imgDir)
sizeOfDir = len(a)
print("number of files:", sizeOfDir)
'''for i in range(sizeOfDir):
    filename = a[i]
    print(filename)'''
filename = a[0]
filepath = conf.imgDir+"/"+a[0]
print("file path", filepath)
print(filename+"step")
shutil.move(filepath, conf.sentImgDir)
sentimgfiles = os.listdir(conf.sentImgDir)
print(sentimgfiles)
