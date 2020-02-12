import os
import math
import operator
import random

 
##################### functions ##################################

########### read file and store as array function #################
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

################### decision tree functions ################
#def majorityCnt(classlist):
#	classcount={}
#	for vote in classlist:
#		if vote not in classcount.keys():
#			classcount[vote]=0
#		classcount[vote] += 1
#	sortedClassCount=sorted(classcount.iteritems(),key=operator.itemgetter(1),reverse=True)
#	return sortedClassCount[0][0]
# 
#def entropy(dataset):
#	n=len(dataset)
#	labels={}
#	for record in dataset:
#		label=record[-1]
#		if label not in labels.keys():
#			labels[label]=0
#		labels[label]+=1
#	ent=0.0
#	for key in labels.keys():
#		prob=float(labels[key])/n
#		ent= -prob*math.log(prob,2)
#	return ent
# 
#def splitDataset(dataset,nclom,value):
#	retDataSet=[]
#	for record in dataset:
#		if record[nclom] == value:
#			reducedRecord=record[:nclom]
#			reducedRecord.extend(record[nclom+1:])
#			retDataSet.append(reducedRecord)
#	return retDataSet
# 
#def chooseBestFeatureToSplit(dataset):
#	numberFeature=len(dataset[0])-1
#	baseEntropy=entropy(dataset)
#	bestInfoGain=0.0	
#	bestFeature=-1
#	for ii in range(numberFeature):
#		featureList=[x[ii] for x in dataset]
#		uniqueValues=set(featureList)
#		newEntropy=0.0
#		for value in uniqueValues:
#			subDataset=splitDataset(dataset, ii, value)
#			prob=len(subDataset)/float(len(dataset))
#			newEntropy += prob*entropy(subDataset)
#		infoGain=baseEntropy-newEntropy
#		if infoGain>bestInfoGain:
#			bestInfoGain=infoGain
#			bestFeature=ii
#	return bestFeature
# 
#def buildTree(dataset,labels):
#	classlist=[ x[-1] for x in dataset]
#	if classlist.count(classlist[0]) == len(classlist):
#		return classlist[0]
#	if len(classlist)==1:
#		return majorityCnt(classlist)
#	if len(labels)==1:
#	    bestFeature=-1
#	else:
#	    bestFeature=chooseBestFeatureToSplit(dataset)
#	    
#	bestFeatureLabel=labels[bestFeature]
#	print(bestFeature)
#	print(labels)
#	tree={bestFeatureLabel:{}}
#	del(labels[bestFeature])
#	featValues = [x[bestFeature] for x in dataset]
#	uniqueVals = set(featValues)
#	for value in uniqueVals:
#		subLabels = labels[:]
#		tree[bestFeatureLabel][value] = buildTree(splitDataset(dataset, bestFeature, value),subLabels)
#	return tree
# 
#def classify(tree,labels,testvec):
#	firstStr = tree.keys()[0]
#	secondDict = tree[firstStr]
#	featIndex = labels.index(firstStr)
#	for key in secondDict.keys():
#		if testvec[featIndex] == key:
#			if type(secondDict[key]).__name__ == 'dict':
#				classLabel = classify(secondDict[key],labels,testvec)
#			else: classLabel = secondDict[key]
#	try:
#		return classLabel
#	except:
#		return 1

def majorityCnt(classlist):
	classcount={}
	for vote in classlist:
		if vote not in classcount.keys():
			classcount[vote]=0
		classcount[vote] += 1
	sortedClassCount=sorted(classcount.iteritems(),key=operator.itemgetter(1),reverse=True)
	return sortedClassCount[0][0]
 
def entropy(dataset):
	n=len(dataset)
	labels={}
	for record in dataset:
		label=record[-1]
		if label not in labels.keys():
			labels[label]=0
		labels[label]+=1
	ent=0.0
	for key in labels.keys():
		prob=float(labels[key])/n
		ent= -prob*math.log(prob,2)
	return ent
 
def splitDataset(dataset,nclom,value):
	retDataSet=[]
	for record in dataset:
		if record[nclom] == value:
			reducedRecord=record[:nclom]
			reducedRecord.extend(record[nclom+1:])
			retDataSet.append(reducedRecord)
	return retDataSet
 
def chooseBestFeatureToSplit(dataset):
	numberFeature=len(dataset[0])-1
	baseEntropy=entropy(dataset)
	bestInfoGain=0.0
	bestFeature=-1
	for i in range(numberFeature):
		featureList=[x[i] for x in dataset]
		uniqueValues=set(featureList)
		newEntropy=0.0
		for value in uniqueValues:
			subDataset=splitDataset(dataset, i, value)
			prob=len(subDataset)/float(len(dataset))
			newEntropy += prob*entropy(subDataset)
		infoGain=baseEntropy-newEntropy
		if infoGain>bestInfoGain:
			bestInfoGain=infoGain
			bestFeature=i
	return bestFeature
 
def buildTree(dataset,labels):
	classlist=[ x[-1] for x in dataset]
	if classlist.count(classlist[0]) == len(classlist):
		return classlist[0]
	if len(classlist)==1:
		return majorityCnt(classlist)
	bestFeature=chooseBestFeatureToSplit(dataset)
	bestFeatureLabel=labels[bestFeature]
	print(bestFeature)
	print(labels)
	tree={bestFeatureLabel:{}}
	del(labels[bestFeature])
	featValues = [x[bestFeature] for x in dataset]
	uniqueVals = set(featValues)
	for value in uniqueVals:
		subLabels = labels[:]
		tree[bestFeatureLabel][value] = buildTree(splitDataset(dataset, bestFeature, value),subLabels)
	return tree
 
def classify(tree,labels,testvec):
	firstStr = tree.keys()[0]
	secondDict = tree[firstStr]
	featIndex = labels.index(firstStr)
	for key in secondDict.keys():
		if testvec[featIndex] == key:
			if type(secondDict[key]).__name__ == 'dict':
				classLabel = classify(secondDict[key],labels,testvec)
			else: classLabel = secondDict[key]
	try:
		return classLabel
	except:
		return 1
###########################################################################
######################## functions ########################################
    
    
############# load data to array ##########################
file_path = os.path.dirname(os.path.abspath(__file__))

train_data_path = file_path +'/data/' + 'traindata'
test_data_path = file_path +'/data/' + 'testdata'
true_class_path = file_path +'/data/' + 'trueclass'
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

num_feaure=25
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

## combine new_data with train_data_1 class list ###
for ii in range(0,len(new_data_1)):
    new_data_1[ii].append(train_data_1[ii][-1])
    

######### build new testing dataset with only the selected feature ########

new_data_2=[]
for ii in range(0,len(train_data_2)):
    dummy=[]
    for ele in feature_index:
        dummy.append(train_data_2[ii][ele])
    new_data_2.append(dummy)


## combine new_data with train_data_2 class list ###
for ii in range(0,len(new_data_2)):
    new_data_2[ii].append(train_data_2[ii][-1])

                
################# implement random forest to do the classification #############

####### do random selection of samples with 80-20 split for n times #########

split_time=20
num_sample=int(len(new_data_1)*0.5)
#num_sample=int(num_feaure*0.5)

data_subset=[]
for ii in range(split_time):
    dummy=random.sample(new_data_1,num_sample)
    data_subset.append(dummy)
    
    
    
########################### create n tree ###################################### 
nfeature=len(data_subset[0][0])
random_trees=[]
for subset in data_subset: 
    labels=["att"+str(i) for i in range(nfeature-1)]   
    tree=buildTree(subset, labels)
    random_trees.append(tree)
    

###################### for each sample from the test datasets try all n tress ###################
nfeature=len(new_data_2[0])
result_vote=[]
for sample in new_data_2:
    result=[]
    for tree in random_trees:
        labels=["att"+str(i) for i in range(nfeature-1)]
        ret=classify(tree, labels, sample)
        result.append(ret)
    result_vote.append(result)

########################### majority vote to determine the class of each sample ######################
class_code=[]
for result in result_vote:
    class_code_dummy=max(set(result), key=result.count)
    class_code.append(class_code_dummy)
    
################### test pertiction ###########################
nPos=0
test=[]
for ii in range(len(new_data_2)):
    if class_code[ii]==new_data_2[ii][-1]:
        nPos +=1
    test.append([class_code[ii],new_data_2[ii][-1]])
		
ntest=len(new_data_2)
print ("The accuracy for data 2 is " + str(nPos/float(ntest)))

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
################## test against the training data set ###############

nPos=0
test=[]
nfeature=len(new_data_1[0])
for r in new_data_1:
        labels=["att"+str(i) for i in range(nfeature-1)]   
	ret=classify(tree, labels, r)
	test.append(ret)
	if ret==r[-1]:
		nPos +=1
ntest=len(new_data_1)
print ("The accuracy rate for data 1 is " + str(nPos/float(ntest)))


################## test against the testing data set ###############

nPos=0
test=[]
nfeature=len(new_data_2[0])
for r in new_data_2:
        labels=["att"+str(i) for i in range(nfeature-1)]  
	ret=classify(tree, labels, r)
	test.append(ret)
	if ret==r[-1]:
		nPos +=1
ntest=len(new_data_1)
print ("The accuracy rate for data 2 is " + str(nPos/float(ntest)))

	