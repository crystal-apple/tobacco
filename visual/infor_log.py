import inspect
import os 
import random 
import sys
def extract_log(log_file,new_log_file,key_word):
    with open(log_file,"r") as f:
        with open(new_log_file,"w") as train_log:
            for line in f:
                if ("Syncing" in line) or ("nan" in line):
                    continue
                
                if key_word in line:
                    train_log.write(line)
    f.close()
    train_log.close()

extract_log("log-enhance-new.txt","train_log_loss.txt","images")
#extract_log("log-24000-all.txt","train_log_iou.txt","IOU")
