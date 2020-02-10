import os
import random



#############ask for user input##########################
file_path = os.path.dirname(os.path.abspath(__file__))


msg_num_cluster = 'Please type in number of clusters, (example: 3) \n: '
num_cluster = int(input(msg_num_cluster).strip())

msg_error_stop = 'Please type in the stop condition, (example: 0.005) \n: '
error_stop = float(input(msg_error_stop).strip())

msg_max_stop = 'Please type in max number of loop to run, (example: 99999) \n: '
max_stop = int(input(msg_max_stop).strip())

data_path = file_path+'/data/' + 'test.data'


########### read file and store as array function #################
def file_to_array(data_path):
    
     #open file
    data_file=open(data_path)
       
    #read file as string separated by \n
    data_str = data_file.read().split('\n')

    #store data in 2d array
    data=[] 
    for ii in range(0,len(data_str)):
        data.append( [float(s) for s in data_str[ii].split(' ') if s != ''])
        
    data_file.close()
 
    return data

########## split list based on index ########   
 
def parts(alist, indices): 
    return [alist[i:j] for i, j in zip([0]+indices, indices+[None])]  
      
#def parts(list_, indices):
#    indices = [0]+indices+[len(list_)]
#    return [list_[v:indices[k+1]] for k, v in enumerate(indices[:-1])]
    
########### randomly place data into n number of clusters #################
def create_random_cluster(data,num_cluster):
    
    #shuffle data
    random.shuffle(data)
    
    #pick n = num_cluster random index from shuffled data, in range of data#
    cluster_index=sorted(random.sample(range(1,len(data)-1), (num_cluster-1)))
    
    #create random cluster#
    cluster=parts(data,cluster_index)
    
        
    return cluster


########### distance between points #########
def distance(a,b):
    res=float(0)
    for ii in range(0,len(a)):
        res=res+(a[ii]-b[ii])*(a[ii]-b[ii])
               
    return res
    
######## begin k-clustering ########
def k_mean(data, cluster):
    #claculate all cluster means#
    cluster_mean=[]
    for ele in cluster: 
        if len(ele)==1:
            mean= ele[0]
        elif len(ele)==0:
            mean=[0]*len(cluster)
        else:
            s=[0]*len(ele[0])
            for ii in range(0,len(ele)):
                for jj in range(0,len(ele[ii])):      
                    s[jj] = (s[jj]+ele[ii][jj])
                mean=[x/len(ele) for x in s]
        cluster_mean.append(mean)

    #compare each point with cluster_mean#
    d_all=[]
    index=[]
    for ii in range(0,len(data)):
        d=[]
        for jj in range(0,len(cluster_mean)):
            d_dummy=distance(data[ii],cluster_mean[jj])
            d.append(d_dummy)
        index_dummy=[i for i, j in enumerate(d) if j == min(d)]
        d_all.append(d)
        index.append(index_dummy[0])
         
    #and create new cluster based on least distance#  
    cluster=[[] for x in range(len(cluster_mean))]
    for ii in range(0,len(data)):
        cluster[index[ii]].append(data[ii])
    
    #compute objective
    sum_total=0
    for ii in range(0,len(cluster_mean)):
        sum_ele=0
        for ele in cluster[ii]:
            sum_ele=sum_ele+distance(ele,cluster_mean[ii])
        sum_total=sum_total+sum_ele
    
    obj=sum_total
    
    return cluster, obj
    
    
######################### main program ############################ 
if os.path.isfile(data_path):  
    
    data=file_to_array(data_path)
    data_origin=file_to_array(data_path)
    stop_count=max_stop
    change=1000
    running=0
    
    ### create random cluster ###
    cluster=create_random_cluster(data,num_cluster)
    
    ### do k_mean once to get initial obj value ###
    cluster, obj0 = k_mean(data, cluster)
    
    while (stop_count!=0 and abs(change)>error_stop):
             
        running=running+1
        print("running loop: {}".format(running))
        
        
        cluster, obj = k_mean(data, cluster)
        
        change=obj-obj0
        stop_count-=1
     
    cluster_index=cluster   
    for ii in range(0,len(cluster)):
        for jj in range(0,len(cluster[ii])):
            for kk in range(0,len(data_origin)):
                if cluster[ii][jj]==data_origin[kk]:
                    cluster_index[ii][jj]=kk
                    
    label=[]            
    for ii in range(0,len(cluster_index)):
        for jj in range(0,len(cluster_index[ii])):
            for kk in range(0,len(data)):
                if cluster_index[ii][jj]==kk:
                    dummy=ii
                    label.append(dummy)
                
                         
        
    print ('Finished \n')
    
    for ele in zip(label,range(0,len(data))):
        print(ele)
        
    print('\n')
    
    for ii in range(0,len(cluster_index)):
        print("cluster{} has points {}".format(ii,sorted(cluster_index[ii])))
       
            
else:
    print ("Invalid File Path, File Doesn't exist")
    

