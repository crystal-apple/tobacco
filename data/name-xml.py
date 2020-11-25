import os 
result_path = '/home/jdh/meiling/darknet/data/tobacco/'
file_dir = os.listdir(result_path)
file = open('./train.txt','w')
#print(file_dir)
for dir in file_dir:
    if dir[-4:]=='.txt':
        path = result_path + dir[:-4] + '.jpg'
        print(path)
        file.write(path + '\n')
