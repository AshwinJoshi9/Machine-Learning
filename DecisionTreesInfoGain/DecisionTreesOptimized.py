'''
Created on Aug 9, 2018

@author: Ashwin
'''
import pandas
import sys
import copy
import math

def calculateEntropy(trainData, classes, totalSamples):    
    entropy = 0
    
    classesCount = trainData[36].value_counts()
    for classWeight in classesCount:
        entropy += (-1) * (classWeight / totalSamples) * math.log2(classWeight / totalSamples)
    return entropy

def informationGain(trainData, attribute, threshold, classes):
    leftChildweight = 0
    rightChildweight = 0
    totalSamples = 0
    
    for val in trainData[0]:    #trainData[0].count()
        totalSamples += 1
    
    priorEntropy = calculateEntropy(trainData, classes, totalSamples)
        
    for val in trainData[attribute]:
        if val <= threshold:
            leftChildweight += 1    
        else:
            rightChildweight += 1
            
    trainDataCopy = copy.deepcopy(trainData)
    lefttrainMatrix = trainData.values
    leftDataSample = []
    for row in lefttrainMatrix:
        if row[attribute] <= threshold:
            leftDataSample.append(row)
    leftExamples = pandas.DataFrame(leftDataSample)
    if not leftExamples.empty:
        leftChildEntropy = calculateEntropy(leftExamples, classes, leftChildweight)
        EntropyLeft = (leftChildweight / totalSamples) * leftChildEntropy
    else:
        EntropyLeft = 0
    trainData = copy.deepcopy(trainDataCopy)     
    
    righttrainMatrix = trainData.values
    rightDataSample = []
    for row in righttrainMatrix:
        if row[attribute] > threshold:
            rightDataSample.append(row)
    rightExamples = pandas.DataFrame(rightDataSample)
    if not rightExamples.empty:
        rightChildEntropy = calculateEntropy(rightExamples, classes, rightChildweight)
        EntropyRight = (rightChildweight / totalSamples) * rightChildEntropy
    else:
        EntropyRight = 0
    trainData = copy.deepcopy(trainDataCopy)
      
    return priorEntropy - (EntropyLeft + EntropyRight)

def chooseAttribute(trainData, attributes, classes):
    maxGain = -1
    bestAttribute = -1
    bestThreshold = -1 
    for attribute in attributes[:-1]:
        Lmin = min(trainData[attribute])
        Mmax = max(trainData[attribute])
        for k in range(1, 51, 1):
            threshold = (Lmin + (k * (Mmax - Lmin))) / 51.0
            gain = informationGain(trainData, attribute, threshold, classes)
            if gain > maxGain:
                maxGain = gain
                bestAttribute = attribute
                bestThreshold = threshold
    return bestAttribute, bestThreshold

class Node():
    leftChild = None
    rightChild = None
    parent = None
    samples = None
    Attribute = None
    Threshold = None
    Class = None
    
def DTLtrain(trainData, attributes, classes, listMode): 
    leftChildData = []
    rightChildData = []
    rootNode = Node()
    if trainData.shape[0] == 0:
        #classList = list((trainData[36].value_counts()).index)
        rootNode.Class = listMode[0]
        return rootNode
    
    elif trainData[36].nunique() == 1:
        rootNode.Class = trainData[36][0]
        return rootNode
    else:
        bestAttribute, bestThreshold = chooseAttribute(trainData, attributes, classes)
        print(bestAttribute, bestThreshold)
        rootNode.samples = trainData
        rootNode.Attribute = bestAttribute
        rootNode.Threshold = bestThreshold
        trainDataCopy = copy.deepcopy(trainData)  
        matrixData = trainData.values
        for row in matrixData:          
            if row[bestAttribute] <= bestThreshold:
                leftChildData.append(row)
            else:
                rightChildData.append(row)
        leftChildSamples = pandas.DataFrame(leftChildData)
        rightChildSamples = pandas.DataFrame(rightChildData)
        trainData = copy.deepcopy(trainDataCopy)
        rootNode.leftChild = Node()
        rootNode.leftChild = DTLtrain(leftChildSamples, attributes, classes, MODE(trainData))
        #rootNode.leftChild.leftChild = leftChildreturn
        #trainData = copy.deepcopy(trainDataCopy)
        '''for row in matrixData:          
            if row[bestAttribute] > bestThreshold:
                rightChildData.append(row)'''
        #rightChildSamples = pandas.DataFrame(rightChildData)
        rootNode.rightChild = Node()
        rootNode.rightChild = DTLtrain(rightChildSamples, attributes, classes, MODE(trainData))
        #rootNode.rightChild = rightChildreturn
        trainData = copy.deepcopy(trainDataCopy)
        return rootNode
    
def MODE(trainData):
    #print((trainData[36].value_counts()).index)
    listMode = (trainData[36].value_counts()).index
    return listMode
    
if __name__ == '__main__':
    classes = []
    trainData = pandas.read_csv(sys.argv[1], sep = ' ', header = None)
    attributes = trainData.columns
    for val in trainData[36]:
        if val not in classes:
            classes.append(val)
    Tree = DTLtrain(trainData, attributes, classes, MODE(trainData))
    print(attributes)
    print(Tree)