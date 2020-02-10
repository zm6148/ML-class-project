import os
import random
import math


#############ask for user input##########################
file_path = os.path.dirname(os.path.abspath(__file__))

msg_data = 'Please type in the name of the data file to be used, \n (example: test_data.data) \n: '
f_name = raw_input(msg_data).strip()

msg_max_stop = 'Please type in max number of loop to run, \n (example: 99999) \n: '
max_stop = float(raw_input(msg_max_stop).strip())

msg_error_stop = 'Please type in the stop condition, \n (example: 0.005) \n: '
error_stop = float(raw_input(msg_error_stop).strip())

msg_step_size = 'Please type in the step size, \n (example: 0.001) \n: '
step_size = float(raw_input(msg_step_size).strip())

data_path = file_path+'\\data\\' + '\\' + f_name.split('.')[0] + '\\' + f_name
label_path = file_path+'\\data\\'+ '\\' + f_name.split('.')[0] + '\\' + f_name.split('.')[0] + '.labels'


###########read file and store as array function#################
def file_to_array(data_path, label_path):
    
     #open file
    data_file=open(data_path)
    label_file=open(label_path)
       
    #read file as string separated by \n
    data_str = data_file.read().split('\n')
    label_str = label_file.read().split('\n')
        
    #store data in 2d array
    data=[] 
    for ii in range(0,len(data_str)):
        data.append( [float(s) for s in data_str[ii].split(' ') if s != ''])
            
    label=[]
    for ii in range(0,len(label_str)):
        label.append([int(jj) for jj in label_str[ii].split(' ')])
        
    data_file.close();
    label_file.close();
    
    return data, label
    

########dot product function###########
def dot(a,b): 
    res=float(0)
    for ii in range(0,len(a)):
        res=res+(a[ii]*b[ii])
        
    return res
    

#############gradient descent###########
def gradient_descent(w,data):
        
    ######calcualte gradient######
    gradient=[]
    for ii in range(0,len(data)):
        gradient_ele=[]
        for jj in range(0,len(data[ii])):                
            gradient_ele.append((label[ii][0]-dot(w,data[ii]))*data[ii][jj])
        gradient.append(gradient_ele)    
            
    
    ####calculate w changes########
    delta_gradient=[0]*len(data[0])  
    for ii in range(0,len(data)):
        for jj in range(0,len(data[ii])):      
            delta_gradient[jj] = delta_gradient[jj]+gradient[ii][jj]
                
    #####updata w and run again#####
    for ii in range(0,len(delta_gradient)):
        w[ii]=w[ii]+step*delta_gradient[ii]
        
    ####calculate total change in gradient#######  
    change=sum(delta_gradient)

    return w,change

#######prediction######    
def prediction(w,data):
    prediction=[]
    for ii in range(0,len(data)):
        value=dot(w,data[ii])
        if value<0:
            prediction.append([0,ii])
        elif value>0:
            prediction.append([1,ii])    
    return prediction   

##################main program#################   
if os.path.isfile(data_path) and os.path.isfile(label_path):  
    
    data, label=file_to_array(data_path, label_path)
        
    ###add one coloum of 1 in data array###
    for ele in data:    
        ele.append(1.0)
                  
    ####change 0 label to -1######
    for ii in range(0,len(label)):
        if label[ii][0]==0:
            label[ii][0]=-1
            
    ####initialize random w######
    w=[]
    for ii in range(0,len(data[0])):
        w.append(random.random())
        
    ######begin calulate gradient and change w accorindly#####
    stop_count=max_stop
    step=step_size
    running=0
    
    w,change0=gradient_descent(w,data)
    
    while (stop_count!=0 and abs(change0)>error_stop):
             
        running=running+1
        print 'running loop: '+ str(running)
        
        w,change=gradient_descent(w,data)
        
        change0=change0-change
        stop_count-=1
        
    sqr_sum=0   
    for ii in range(0,len(w)-1):
        sqr_sum=sqr_sum+w[ii]**2
    distance=abs(w[len(w)-1])/math.sqrt(sqr_sum)
    
    prediction=prediction(w,data)
        
    print 'Finished \n'  
    print 'Distance to the plane is: ' + str(distance) + '\n'
    print 'the w values are: ' + str(w) + '\n'
    
    ######save prediction on file######
    path=label_path = file_path+'\\data\\'+ '\\' + f_name.split('.')[0] + '\\' + f_name.split('.')[0] + '.prediction_gradient'
    f = open(path, "w")
    f.write('\n'.join(' '.join(map(str, ele)) for ele in prediction))
    f.close()
            
else:
    print "Invalid File Path, File Doesn't exist"


    