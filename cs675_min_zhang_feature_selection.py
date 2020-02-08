import os
 
##################### functions ##################################
########### read file and store as array function #################
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

#################### find nth largest number from list ################### 


def v_sum(v1,v2):
    v=[]
    for ii in range(len(v1)):
        v.append(v1[ii]+v2[ii])
    return v

def v_dis(v1,v2):
    dis=0
    for ii in range(len(v1)):
        dis=dis+(float(v1[ii])-float(v2[ii]))**2
    return dis
    

########### perform modified t_test to do feature selection ##########

def feature_selection (train_data):
    N=len(train_data)
    C=2
    nominal_train_data=train_data[:]
    t_value=[]
    for jj in range(len(nominal_train_data[0])-1):
        
        print("running feature: " +str(jj))
        sum_c1=[0]*3 #0 label
        sum_c2=[0]*3 #1 label
        nc1=0
        nc2=0
        
        for ii in range(len(nominal_train_data)):
            
            if train_data[ii][jj]==0:
                nominal_train_data[ii][jj]=[0,0,1]            
            elif train_data[ii][jj]==1:
                nominal_train_data[ii][jj]=[0,1,0]            
            elif train_data[ii][jj]==2:
                nominal_train_data[ii][jj]=[1,0,0]
                
            if train_data[ii][-1]==0:
                sum_c1=v_sum(sum_c1,nominal_train_data[ii][jj])
                nc1=nc1+1
            else:
                sum_c2=v_sum(sum_c2,nominal_train_data[ii][jj])
                nc2=nc2+1
        
        mean_c1=[float(ele)/nc1 for ele in sum_c1]
        mean_c2=[float(ele)/nc2 for ele in sum_c2]
        mean=[float(ele)/2 for ele in v_sum(mean_c1,mean_c2)]
        
        s_c1=0
        s_c2=0
        for ii in range(len(nominal_train_data)):
            if train_data[ii][-1]==0:
                s_c1=s_c1+v_dis(nominal_train_data[ii][jj],mean_c1)
            else:
                s_c2=s_c2+v_dis(nominal_train_data[ii][jj],mean_c2)
            s=(s_c1+s_c2)/(N-C)
        
        mc1=1/float(nc1)+1/float(N)
        mc2=1/float(nc2)+1/float(N)
        
        #print(s)
        #print(mc1)
        #print(mc2)
        #print(nc1)
        #print(nc2)
        
        t_c1=v_dis(mean_c1,mean)/(s*mc1)
        t_c2=v_dis(mean_c2,mean)/(s*mc2)
        t_value.append(max([t_c1,t_c2]))
        
        
    
    del nominal_train_data
        
    return t_value
    
#######################################################################
#################### main program #####################################  
#######################################################################
   
############# load data to array ##########################
file_path = os.path.dirname(os.path.abspath(__file__))

train_data_path = file_path +'/data/' + 'traindata'
test_data_path = file_path +'/data/' + 'testdata'
true_class_path = file_path +'/data/' + 'trueclass'

train_data = file_to_array(train_data_path)
test_data = file_to_array(test_data_path)
true_class = file_to_array(true_class_path)

############### split train_data by half train_data_1 as training, train_data_2 as testing ##########

## combine train_data with true label list ###
for ii in range(0,len(train_data)):
    train_data[ii].append(true_class[ii][0])
        
########### select top n from t_value as feature ###########

selection_value=feature_selection(train_data)

path=label_path = file_path+'/selection_value'
f = open(path, "w")
for item in selection_value:
  f.write("%s\n" % item)
f.close()

print("selection_value saved on file")
