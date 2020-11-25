
import xml.etree.ElementTree as ET
import os

sets=["train"]
classes=["others", "tobacco_dust", "pipe_tobacco", "filter_stick", "glue", "glue_scale", "cigaretee", "normal"]

def convert_annotation(image_id,file):
    in_file=open('/home/data/VOC2007/Annotations/%s.xml'%(image_id))
    tree=ET.parse(in_file)
    root=tree.getroot()

    
    for obj in root.iter('object'):
        difficult=obj.find('Difficult').text
        cls=obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox=obj.find('bndbox')
        b=(int(xmlbox.find('xmin').text),int(xmlbox.find('ymin').text),int(xmlbox.find('xmax').text),int(xmlbox.find('ymax').text))
        file.write(" "+",".join([str(a) for a in b])+','+str(cls_id))
        
for image_set in sets:
    #image_ids=open("/home/data/VOC2007/ImageSets/Main/%s.txt"%(image_set)).read().strip().split()
    image_ids=open("/home/data/VOC2007/ImageSets/Main/%s.txt"%(image_set)).read().strip().split()
    print(type(image_ids))
    print(image_ids)
    print('1111111111111111',len(image_ids))
    list_file=open('path_coord.txt','a')
    for image_id in image_ids:
        
        list_file.write('/home/data/VOC2007/JPEGImages/%s.jpg'%(image_id))
        convert_annotation(image_id,list_file)
        list_file.write('\n')
    list_file.close()