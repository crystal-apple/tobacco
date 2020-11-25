'''
import numpy as np

def kmeans_txt(cluster_number,filename):
    all_boxes=txt2boxes(filename)
    result=kmeans(all_boxes,cluster_number)
    result=result[np.lexsort(result.T[0,None])]
    result2txt(result)
    print('K anchors:\n {}'.format(result))
    print("Accuracy:{:.2f}%".format(avg_iou(all_box,result)*100))

if __name__=="__main__":
    cluster_number = 9
    filename="path_coord.txt"
    f=open(filename,'r')
    dataSet=[]
    for line in f:
        infors=line.split(" ")
        length=len(infors)
        #print(infors,length)
        for i in range(1,length):
            #print('111111111',infors[i].split(","))
            width =int(infors[i].split(",")[1])-int(infors[i].split(",")[0])
            height=int(infors[i].split(",")[3])-int(infors[i].split(",")[2])
            dataSet.append([width,height])
            #print('111111',dataSet)
            #print(infors[i].strip().split(","))
        break
    result=np.array(dataSet)
    #print(result)
    f.close()
    box_number=result.shape
    #print(box_number)
    distances=np.empty((box_number,k))
    last_nearest=np.zeros((box_number,))
    np.random.seed()
    
    
a = np.array([2,3,4])
b = np.array([2.0,3.0,4.0])
c = np.array([[1.0,2.0],[3.0,4.0]])
d = np.array([[1,2],[3,4]],dtype=complex) # 指定数据类型
print a, a.dtype
print b, b.dtype
print c, c.dtype
print d, d.dtype

# def txt2boxes(filename):
    # f=open(file,'r')
    # dataSet=[]
    # for line in f:
        # infors=line.split("")
        # length

# def kmeans_txt(cluster_number,filename):
    # all_boxes=txt2boxes(filename)
    # result=kmeans(all_boxes,cluster_number)
    # result=result[np.lexsort(result.T[0,None])]
    # result2txt(result)
    # print('K anchors:\n {}'.format(result))
    # print("Accuracy:{:.2f}%".format(avg_iou(all_box,result)*100))

# if __name__=="__main__":
    # cluster_number = 9
    # filename="train.txt"
    # kmeans_txt()
'''

import numpy as np

class YOLO_Kmeans:

    def __init__(self, cluster_number, filename):
        self.cluster_number = cluster_number
        self.filename = "path_coord.txt"

    def iou(self, boxes, clusters):  # 1 box -> k clusters
        n = boxes.shape[0]
        k = self.cluster_number

        box_area = boxes[:, 0] * boxes[:, 1]
        box_area = box_area.repeat(k)
        box_area = np.reshape(box_area, (n, k))

        cluster_area = clusters[:, 0] * clusters[:, 1]
        cluster_area = np.tile(cluster_area, [1, n])
        cluster_area = np.reshape(cluster_area, (n, k))

        box_w_matrix = np.reshape(boxes[:, 0].repeat(k), (n, k))
        cluster_w_matrix = np.reshape(np.tile(clusters[:, 0], (1, n)), (n, k))
        min_w_matrix = np.minimum(cluster_w_matrix, box_w_matrix)

        box_h_matrix = np.reshape(boxes[:, 1].repeat(k), (n, k))
        cluster_h_matrix = np.reshape(np.tile(clusters[:, 1], (1, n)), (n, k))
        min_h_matrix = np.minimum(cluster_h_matrix, box_h_matrix)
        inter_area = np.multiply(min_w_matrix, min_h_matrix)
        
        print("111111111",box_area)
        print("222222222",cluster_area)
        print("333333333",inter_area)

        if (box_area + cluster_area - inter_area) == 0:
            pass
        else:
            result = inter_area / (box_area + cluster_area - inter_area)
        return result

    def avg_iou(self, boxes, clusters):
        accuracy = np.mean([np.max(self.iou(boxes, clusters), axis=1)])
        return accuracy

    def kmeans(self, boxes, k, dist=np.median):
        box_number = boxes.shape[0]
        distances = np.empty((box_number, k))
        last_nearest = np.zeros((box_number,))
        np.random.seed()
        clusters = boxes[np.random.choice(
            box_number, k, replace=False)]  # init k clusters
        while True:

            distances = 1 - self.iou(boxes, clusters)

            current_nearest = np.argmin(distances, axis=1)
            if (last_nearest == current_nearest).all():
                break  # clusters won't change
            for cluster in range(k):
                clusters[cluster] = dist(  # update clusters
                    boxes[current_nearest == cluster], axis=0)

            last_nearest = current_nearest

        return clusters

    def result2txt(self, data):
        f = open("yolo_anchors.txt", 'w')
        row = np.shape(data)[0]
        for i in range(row):
            if i == 0:
                x_y = "%d,%d" % (data[i][0], data[i][1])
            else:
                x_y = ", %d,%d" % (data[i][0], data[i][1])
            f.write(x_y)
        f.close()

    def txt2boxes(self):
        f = open(self.filename, 'r')
        dataSet = []
        for line in f:
            infos = line.split(" ")
            length = len(infos)
            for i in range(1, length):
                width = int(infos[i].split(",")[2]) - \
                    int(infos[i].split(",")[0])
                height = int(infos[i].split(",")[3]) - \
                    int(infos[i].split(",")[1])
                dataSet.append([width, height])
        result = np.array(dataSet)
        print(result)
        f.close()
        return result

    def txt2clusters(self):
        all_boxes = self.txt2boxes()
        result = self.kmeans(all_boxes, k=self.cluster_number)
        result = result[np.lexsort(result.T[0, None])]
        self.result2txt(result)
        print("K anchors:\n {}".format(result))
        print("Accuracy: {:.2f}%".format(
            self.avg_iou(all_boxes, result) * 100))


if __name__ == "__main__":
    cluster_number = 9
    filename = "path_coord.txt"
    kmeans = YOLO_Kmeans(cluster_number, filename)
    kmeans.txt2clusters()
    print("done111111111donoe")


