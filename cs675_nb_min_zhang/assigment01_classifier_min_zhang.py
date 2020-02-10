import os
import numpy as np

file_path = os.path.dirname(os.path.abspath(__file__))
msg_trainlabel = 'Please type in the name of the trainlables to be used, \n (example: breast_cancer.trainlabels.6 or climate.trainlabels.3) \n: '
f_name = raw_input(msg_trainlabel).strip()

data_path=file_path+'\\data\\'+f_name.split('.')[0]+'\\' + f_name.split('.')[0] + '.data'
train_labels_path=file_path+'\\data\\'+f_name.split('.')[0]+'\\'+f_name

#labels_path=file_path+'\\data\\breast_cancer\\breast_cancer.labels'

def text_to_array(data_path,train_labels_path):
    #open file
    data_file=open(data_path)
    train_labels_file=open(train_labels_path)
    #labels_file=open(labels_path)
    
    #read file as string separated by \n
    data_str = data_file.read().split('\n')
    train_labels_str = train_labels_file.read().split('\n')
    #labels_str = labels_file.read().split('\n')
    
    #store data in 2d array
    data=[] 
    for ii in range(0,len(data_str)-1):    
        data.append( [float(s) for s in data_str[ii].split(' ') if s != ''])
    data=np.asarray(data)
        
    train_labels=[]
    for ii in range(0,len(train_labels_str)-1):
        train_labels.append([int(jj) for jj in train_labels_str[ii].split(' ')])
    train_labels=np.asarray(train_labels)
    
    return data, train_labels

def classifier(data,train_labels):
    #find all data indices that belong to each class and calculate mean and var
    #class mean var
    class_mean_var=[];
    for class_label in np.unique(train_labels[:,0]):
        class_index=train_labels[train_labels[:,0]==class_label][:,1]
        class_mean=data[class_index,:].mean(0)
        class_var=data[class_index,:].var(0)
        dummy=[class_label, class_mean, class_var]
        class_mean_var.append(dummy)
        
    #trianing complete, using nearest mean to calculate distance and perdicte data and generate perdicted_labels 
    perdicted_labels_a=[]
    for ii in range(0,data.shape[0]):
        distance=[]
        for jj in range(0,len(class_mean_var)):
            dummy = [jj,sum((data[ii,:]-class_mean_var[jj][1])**2)]
            distance.append(dummy)
        distance=np.asarray(distance)
        dummy=[int(distance[np.argmin(distance[:,1]),0]),ii]
        perdicted_labels_a.append(dummy)
    perdicted_labels_a=np.asarray(perdicted_labels_a)  
        
    #trianing complete, using naive bayes to calculate distance and perdicte data and generate perdicted_labels 
    perdicted_labels_b=[]
    for ii in range(0,data.shape[0]):
        distance=[]
        for jj in range(0,len(class_mean_var)):
            dummy=[jj,sum(((data[ii,:]-class_mean_var[jj][1])**2/(class_mean_var[jj][2]+1)))]
            distance.append(dummy)
        distance=np.asarray(distance)
        dummy=[int(distance[np.argmin(distance[:,1]),0]),ii]
        perdicted_labels_b.append(dummy)
    perdicted_labels_b=np.asarray(perdicted_labels_b) 
        
    return perdicted_labels_a, perdicted_labels_b
    

if os.path.isfile(data_path) and os.path.isfile(train_labels_path):
    data, train_labels = text_to_array(data_path,train_labels_path)
    perdicted_labels_a, perdicted_labels_b = classifier(data,train_labels) 
    save_file_name_a=file_path+'\\data\\'+f_name.split('.')[0]+'\\' + f_name.split('.')[0] + '.prediction.a'
    save_file_name_b=file_path+'\\data\\'+f_name.split('.')[0]+'\\' + f_name.split('.')[0] + '.prediction.b'
    np.savetxt(save_file_name_a, perdicted_labels_a,fmt='%i')   
    np.savetxt(save_file_name_b, perdicted_labels_b,fmt='%i')  
    print 'Finished and predictied lables are stored in the same folder as the trainlabels file \n '+ f_name.split('.')[0] +'.prediction.a is the results from nearest mean \n '+ f_name.split('.')[0]+'.prediction.b is the reuslts from naive bayes \n use assigment01_evaluate_min_zhang.py to evaluate'       
else:
    print "Invalid File Path, File Doesn't exist"
    
        

