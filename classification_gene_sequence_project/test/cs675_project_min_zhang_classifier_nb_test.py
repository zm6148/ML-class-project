import os

    
def find_max(data,n):
    
    index=sorted(range(len(data)), key=lambda x: data[x])[-n:]
    
    return index
    
def file_to_array(data_path):
    
     #open file
    data_file=open(data_path)
       
    #read file as string separated by \n
    data_str = data_file.read().split('\n')

    #store data in 2d array
    data=[] 
    for ii in range(0,len(data_str)-1):
        data.append( [float(s) for s in data_str[ii].split(' ') if s != ''])
        
    data_file.close()
 
    return data
    
def average(data):
    sum_of_data = sum(data)
    average = sum_of_data / len(data)
    return average

def variance(data,average):
    variance = 0
    for ele in data:
         variance += (average - ele) ** 2
    return variance / len(data)

   
    
def classifier(train_data,train_labels,test_data):
    #find all data indices that belong to each class and calculate mean and var
    #class mean var
    
    mean_var_c0=[]
    mean_var_c1=[]
    for jj in range(len(train_data[0])):
        
        class_c0=[]
        class_c1=[]
        
        for ii in range(len(train_data)):
            if train_labels[ii][0]==0:
                class_c0.append(train_data[ii][jj])
            else:
                class_c1.append(train_data[ii][jj])
                
        average_c0=average(class_c0)
        var_c0=variance(class_c0,average_c0)
        
        average_c1=average(class_c1)
        var_c1=variance(class_c1,average_c1)
        
        mean_var_c0.append([average_c0,var_c0])
        mean_var_c1.append([average_c1,var_c1])


    #trianing complete, using naive bayes to calculate distance and perdicte data and generate perdicted_labels 
    perdicted_labels=[]
    for ii in range(len(test_data)): 
        distance_c0=0
        distance_c1=0       
        for jj in range(len(test_data[ii])):
            distance_c0=distance_c0+((test_data[ii][jj]-mean_var_c0[jj][0])**2/(mean_var_c0[jj][1]+1))
            distance_c1=distance_c1+((test_data[ii][jj]-mean_var_c1[jj][0])**2/(mean_var_c1[jj][1]+1))
        if distance_c0 <= distance_c1:
            perdicted_labels_dummy=0
        else:
            perdicted_labels_dummy=1
        perdicted_labels.append(perdicted_labels_dummy)
        
            
        
    return perdicted_labels

############# load data to array ##########################
file_path = os.path.dirname(os.path.abspath(__file__))

train_data_path = file_path +'/data/' + 'traindata'
test_data_path = file_path +'/data/' + 'testdata'
true_class_path = file_path +'/data/' + 'trueclass'
#selection_value_path = file_path +'/selection_value_test'
selection_value_path = file_path +'/selection_value_test'
separate_index_path = file_path +'/separate_index_test'


train_data = file_to_array(train_data_path)
test_data = file_to_array(test_data_path)
true_class = file_to_array(true_class_path)


############### split train_data by half train_data_1 as training, train_data_2 as testing ##########

############### load separation index and feature index from file ##########
separate_index_dummy= file_to_array(separate_index_path)
separate_index=[]
for ele in separate_index_dummy:
    separate_index.append(int(ele[0]))

selection_value=[]
selection_value_dummy= file_to_array(selection_value_path)
for ele in selection_value_dummy:
    selection_value.append(ele[0])

num_feaure=15
feature_index=find_max(selection_value,num_feaure)

## combine train_data with true label list ###
for ii in range(0,len(train_data)):
    train_data[ii].append(true_class[ii][0])

train_data_1=[]
train_data_2=[]
for ii in range(len(train_data)):
    if ii in separate_index:
        train_data_1.append(train_data[ii])
    else:
        train_data_2.append(train_data[ii])
        
######### build new training dataset with only the selected feature ########

new_data_1=[]
for ii in range(0,len(train_data_1)):
    dummy=[]
    for ele in feature_index:
        dummy.append(train_data_1[ii][ele])
    new_data_1.append(dummy)
#train_data=np.array(new_data_1)    

train_class_1=[]
for ii  in range(len(train_data_1)):
    train_class_1.append([int(train_data_1[ii][-1]),int(ii)])
#train_label=np.array(train_class_1)
    

######### build new testing dataset with only the selected feature ########

new_data_2=[]
for ii in range(0,len(train_data_2)):
    dummy=[]
    for ele in feature_index:
        dummy.append(train_data_2[ii][ele])
    new_data_2.append(dummy)
#test_data=np.array(new_data_2)   

test_class_2=[]
for ele in train_data_2:
    test_class_2.append(ele[-1])
#test_label=np.array(test_class_2)

#############################################################################
perdicted_labels=classifier(new_data_1,train_class_1,new_data_2)

nps=0
for ii in range(len(test_class_2)):
    if test_class_2[ii]==perdicted_labels[ii]:
        nps=nps+1

print(float(nps)/len(test_class_2))






