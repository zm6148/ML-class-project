import os
import numpy as np

#ask user for the name of the prediction to evaluate
file_path = os.path.dirname(os.path.abspath(__file__))

#msg_true = 'Please type in the name of the true lables, \n (example: breast_cancer.labels or climate.labels) \n: '
#true_name = raw_input(msg_true).strip()

msg_true = 'Please type in the name of the predicted lables\n (example: breast_cancer.prediction.a or climate.prediction.b) \n: '
prediction_name = raw_input(msg_true).strip()
prediction_name.split('.')[0]

true_path=file_path+'\\data\\'+prediction_name.split('.')[0]+'\\' + prediction_name.split('.')[0]+'.labels'
prediction_path=file_path+'\\data\\'+prediction_name.split('.')[0]+'\\'+prediction_name

#open files and load data
true_file=open(true_path)
true_str = true_file.read().split('\n')

prediction_file=open(prediction_path)
prediction_str = prediction_file.read().split('\n')

true=[]
for ii in range(0,len(true_str)-1):
    true.append([int(jj) for jj in true_str[ii].split(' ')])
true=np.asarray(true)    

prediction=[]
for ii in range(0,len(prediction_str)-1):
    prediction.append([int(jj) for jj in prediction_str[ii].split(' ')])
prediction=np.asarray(prediction)  

#count for TP FP FN TN and calcualte 
TP=0.0
FP=0.0
FN=0.0
TN=0.0

for ii in range(0,true.shape[0]):
    if true[ii,0]==1 and prediction[ii,0]==1:
        TP=TP+1
    elif true[ii,0]==1 and prediction[ii,0]==0:
        FN=FN+1    
    elif true[ii,0]==0 and prediction[ii,0]==1:
        FP=FP+1        
    elif true[ii,0]==0 and prediction[ii,0]==0:
        TN=TN+1

E=(FP+FN)/(TP+FP+FN+TN)
BER=0.5*(FP/(FP+TN)+FN/(FN+TP))
Recall=TP/(TP+FN)  
Precision=TP/(TP+FP) 
 
print('{0} | {1} | {2}'.format('Data Point','True Labels', 'Predicted Labels')) 
for ii in range(0, true.shape[0]):    
    print('{0:10d}{1:10d}{2:10d}'.format(true[ii,1],true[ii,0], prediction[ii,0]))
print('{0} | {1} | {2}'.format('Data Point','True Labels', 'Predicted Labels'))
print('{0} = {1} ; {2} = {3} ; {4} = {5} ; {6} = {7}'.format('TP',TP, 'FP',FP,'FN',FN,'TN',TN))
print('{0} = {1} ; {2} = {3} ; {4} = {5} ; {6} = {7}'.format('E',E, 'BER',BER,'Precision',Precision,'Recall',Recall))


 

   
     