import random
import os
import xml.etree.ElementTree as ET
import collections
import numpy as np


def test_picture(thresh_list,weight_list,num_picture,path):
    image_dir=os.listdir(path)
    image_list=[]
    file = open('./test-log/'+"input-"+str(num_picture)+".txt",'w')
    for image in image_dir:
        image_list.append(image[:-4])
    image_list.sort(key=int)
    
    for image_new in image_list:
        #print(image_new)
        file.write(path+image_new+'.jpg\n')
    file.close()
        
    for thresh in thresh_list:
        for weight in weight_list:
            #print(thresh)
            if not os.path.exists("/home/disk_4t/meiling/meiling-237/tobacco_data/%s_%s_%s"%(num_picture,weight,thresh)):
                os.makedirs('/home/disk_4t/meiling/meiling-237/tobacco_data/%s_%s_%s'%(num_picture,weight,thresh))
            out_path = "/home/disk_4t/meiling/meiling-237/tobacco_data/"+str(num_picture)+'_'+str(weight)+"_"+str(thresh)
            #print('11111111',out_path)
            ord = "./imagebbox detect cfg/tobacco.cfg backup/tobacco_"+ str(weight)+".weights -thresh " \
            + str(thresh) + " ./test-log/input-"+str(num_picture)+".txt "+"-out " + str(out_path)+" |tee ./test-log/log_"+str(num_picture)+'_'+str(thresh)+'_'+str(weight)+".txt"
            print(ord)
            print('model loading success!!!')
            os.system(ord)
            #+"-out " + str(out_path)
def log_flag(keywords,thresh_list,weight_list,num_picture):
    
    flag_list=[]
    for weight in weight_list:
        for thresh in thresh_list:
            #print('thresh',thresh)
            flag=[]
            f = open('./test-log/'+"log_"+str(num_picture)+'_'+str(thresh)+'_'+str(weight)+".txt",'r')
            for line in f.readlines():
                if keywords in line:
                    line=line.strip().split(":")
                    #print(line[-1])
                    flag.append(line[-1])
                #print(flag)
            flag_list.append(flag)
        
    return flag_list

def match(num_picture,weight_list,key_value,flag_list,thresh_list):
    
    import csv
    for weight in weight_list:
        csvfile=open('./test-log/'+str(num_picture)+'_'+str(weight)+'.csv','w')
    writer=csv.writer(csvfile)
    writer.writerow(['thresh','precision','tp','tn','fn','fp','P','R','TPR','FPR','TNP','F','MA','FA'])
    csv_list=[]
    file_list=[]
    
    pre_list={}
    num=0
    #print('len(thresh_list)',len(thresh_list))
    #print('lenxxxxxxxxxx',len(key_value))
    for thresh in thresh_list:
        pre=[]
        tp=0
        tn=0
        fn=0
        fp=0
        
        for i in range(len(key_value)):
            if int(key_value[i])==0:
                if int(key_value[i])==int(flag_list[num][i]):
                    tp+=1
                else:
                    fn+=1
            else:
                if int(key_value[i])==int(flag_list[num][i]):
                    tn+=1
                else:
                    fp+=1
        num+=1
        precision=(tp+tn)/(len(key_value))
        
        P=tp/(tp+fp)
        R=tp/(tp+fn)
        TPR=tp/(tp+fn)
        FPR=fp/(fp+tn)
        TNP=fn/(fp+tn)
        F=2*P*R/(P+R)
        MA=fn/(tp+fn)
        FA=fp/(tp+fp)
        pre.extend([precision,tp,tn,fn,fp,P,R,TPR,FPR,TNP,F,MA,FA])
        
        pre_list[thresh]=pre
        file_list=[thresh,precision,tp,tn,fn,fp,P,R,TPR,FPR,TNP,F,MA,FA]
        csv_list.append(file_list)
    print('csv_list',csv_list)
    writer.writerows(csv_list)
    return pre_list



if __name__=="__main__":

    #######参数配置
    thresh_list=[0.04]
    weight_list = [148000]
    num_picture=209
    
    imgfilepath='/home/disk_4t/meiling/meiling-237/tobacco_test_picture/test-209/'
    ########测试模型 生成log文件
    test_picture(thresh_list,weight_list,num_picture,imgfilepath)
    #########209张第二次武汉测试图
    key_value=[1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,1,1,1,0,1,1,0,1,0,0,0,0,0,0,0,0,0,1,0,1,1,1,0,1,0,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,0,1,1,1,0,1,0,1,0,0,1,1,1,0,1,1,1,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,1,0,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,1,1,0,0,0,0,1,0,1,0,0,1,1,0,1,1,0,0,0,1,0,1,1,0]
    #key_value=[1,0,0,0,1,1,0,0,0,0,1,0,1,0,0,1,1,0,1,1,0,0,0,1,1,1,1,0]
    #########提取log文件内容
    keywords = "dirty_flag"
    flag_list=log_flag(keywords,thresh_list,weight_list,num_picture)
    #####与真值表进行匹配，计算准确率
    pre = match(num_picture,weight_list,key_value,flag_list,thresh_list)
    
    
    
    





