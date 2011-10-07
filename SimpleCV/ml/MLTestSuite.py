from numpy import *
from SimpleCV.Display import Display, pg
from SimpleCV.EdgeHistogramFeatureExtractor import *
from SimpleCV.HueHistogramFeatureExtractor import *
from SimpleCV.BOFFeatureExtractor import *
from SimpleCV.HaarLikeFeatureExtractor import *
from SimpleCV.MorphologyFeatureExtractor import *
import Orange
import os
import glob
import pickle
from SVMClassifier import *
from NaiveBayesClassifier import *
from KNNClassifier import *
from TreeClassifier import *

w = 800
h = 600
n=50

display = Display(resolution = (w,h))
hue = HueHistogramFeatureExtractor(mNBins=16)
edge = EdgeHistogramFeatureExtractor()
bof = BOFFeatureExtractor()
bof.load('cbdata.txt')
morph = MorphologyFeatureExtractor()
haar = HaarLikeFeatureExtractor(fname="haar.txt")

spath = "../sampleimages/data/structured/"
upath = "../sampleimages/data/unstructured/"
ball_path = spath+"ball/"
basket_path = spath+"basket/"
boat_path = spath+"boat/"
cactus_path = spath +"cactus/"
cup_path = spath+"cup/"
duck_path = spath+"duck/"
gb_path = spath+"greenblock/"
match_path = spath+"matches/"
rb_path = spath+"redblock/"
s1_path = spath+"stuffed/"
s2_path = spath+"stuffed2/"
s3_path = spath+"stuffed3/"

arbor_path = upath+"arborgreens/"
football_path = upath+"football/"
sanjuan_path = upath+"sanjuans/"

#
#print('###############################################################################')
#print('Vanilla Tree')
#
#
extractors = [haar]
classifierTree = TreeClassifier(featureExtractors=extractors)
print('Train')
path = [s1_path,s2_path,s3_path]
classes = ['s1','s2','s3']
classifierTree.train(path,classes,disp=display,subset=n) #train
print('Test')
[pos,neg,confuse] = classifierTree.test(path,classes,disp=display,subset=n)
files = glob.glob( os.path.join(path[0], '*.jpg'))
for i in range(10):
        img = Image(files[i])
        cname = classifierTree.classify(img)
        print(files[i]+' -> '+cname)

classifierTree.save('tree.pkl')
testTree = TreeClassifier.load('tree.pkl')
for i in range(10):
        img = Image(files[i])
        cname = testTree.classify(img)
        print(files[i]+' -> '+cname)



print('###############################################################################')
print('Boosted Tree')
extractors = [haar]
classifierBTree = TreeClassifier(extractors,flavor='Boosted')#
print('Train')
path = [s1_path,s2_path,s3_path]
classes = ['s1','s2','s3']
classifierBTree.train(path,classes,disp=display,subset=n) #train
print('Test')
[pos,neg,confuse] = classifierBTree.test(path,classes,disp=display,subset=n)
files = glob.glob( os.path.join(path[0], '*.jpg'))
for i in range(10):
        img = Image(files[i])
        cname = classifierBTree.classify(img)
        print(files[i]+' -> '+cname)
        
classifierBTree.save('btree.pkl')
#testBoostTree = TreeClassifier.load('btree.pkl')
#files = glob.glob( os.path.join(path[0], '*.jpg'))
#for i in range(10):
#        img = Image(files[i])
#        cname = testBoostTree.classify(img)
#        print(files[i]+' -> '+cname)


print('###############################################################################')
print('Bagged Tree')
extractors = [hue]
classifierBagTree = TreeClassifier(extractors,flavor='Bagged')#
print('Train')
path = [s1_path,s2_path,s3_path]
classes = ['s1','s2','s3']
classifierBagTree.train(path,classes,disp=display,subset=n) #train
print('Test')
[pos,neg,confuse] = classifierBagTree.test(path,classes,disp=display,subset=n)
files = glob.glob( os.path.join(path[0], '*.jpg'))
for i in range(10):
        img = Image(files[i])
        cname = classifierBagTree.classify(img)
        print(files[i]+' -> '+cname)
        
#classifierBagTree.save('bagtree.pkl')
#testBagTree = TreeClassifier.load('bagtree.pkl')
#files = glob.glob( os.path.join(path[0], '*.jpg'))
#for i in range(10):
#        img = Image(files[i])
#        cname = testBagTree.classify(img)
#        print(files[i]+' -> '+cname)

print('###############################################################################')
print('Forest')
extractors = [edge]
classifierForest = TreeClassifier(extractors,flavor='Forest')#
print('Train')
path = [s1_path,s2_path,s3_path]
classes = ['s1','s2','s3']
classifierForest.train(path,classes,disp=display,subset=n) #train
print('Test')
[pos,neg,confuse] = classifierForest.test(path,classes,disp=display,subset=n)
files = glob.glob( os.path.join(path[0], '*.jpg'))
for i in range(10):
        img = Image(files[i])
        cname = classifierForest.classify(img)
        print(files[i]+' -> '+cname)
        
classifierForest.save('forest.pkl')
#testForest = TreeClassifier.load('forest.pkl')
#files = glob.glob( os.path.join(path[0], '*.jpg'))
#for i in range(10):
#        img = Image(files[i])
#        cname = testForest.classify(img)
#        print(files[i]+' -> '+cname)

print('###############################################################################')
print('KNN')
extractors = [hue,edge]
classifierKNN = KNNClassifier(extractors)#
print('Train')
path = [s1_path,s2_path,s3_path]
classes = ['s1','s2','s3']
classifierKNN.train(path,classes,disp=display,subset=n) #train
print('Test')
[pos,neg,confuse] = classifierKNN.test(path,classes,disp=display,subset=n)
files = glob.glob( os.path.join(path[0], '*.jpg'))
for i in range(10):
        img = Image(files[i])
        cname = classifierKNN.classify(img)
        print(files[i]+' -> '+cname)
        
classifierKNN.save('knn.pkl')
testKNN = KNNClassifier.load('knn.pkl')
files = glob.glob( os.path.join(path[0], '*.jpg'))
for i in range(10):
        img = Image(files[i])
        cname = testKNN.classify(img)
        print(files[i]+' -> '+cname)

print('###############################################################################')
print('SVMPoly')
#Set up am SVM with a poly kernel
extractors = [hue]
path = [cactus_path,cup_path,basket_path]
classes = ['cactus','cup','basket']
props ={
        'KernelType':'Poly', #default is a RBF Kernel
        'SVMType':'C',     #default is C 
        'nu':None,          # NU for SVM NU
        'c':None,           #C for SVM C - the slack variable
        'degree':3,      #degree for poly kernels - defaults to 3
        'coef':None,        #coef for Poly/Sigmoid defaults to 0
        'gamma':None,       #kernel param for poly/rbf/sigma - default is 1/#samples       
    }
print('Train')
classifierSVMP = SVMClassifier(extractors,props)
classifierSVMP.train(path,classes,disp=display,subset=n) #train
print('Test')
[pos,neg,confuse] = classifierSVMP.test(path,classes,disp=display,subset=n)
files = glob.glob( os.path.join(path[0], '*.jpg'))
for i in range(10):
        img = Image(files[i])
        cname = classifierSVMP.classify(img)
        print(files[i]+' -> '+cname)
classifierSVMP.save('PolySVM.pkl')
#testSVM = SVMClassifier.load('PolySVM.pkl')
#files = glob.glob( os.path.join(path[0], '*.jpg'))
#for i in range(10):
#        img = Image(files[i])
#        cname = testSVM.classify(img)
#        print(files[i]+' -> '+cname)

print('###############################################################################')
print('SVMRBG')
# now try an RBF kernel
extractors = [hue,edge]
path = [cactus_path,cup_path,basket_path]
classes = ['cactus','cup','basket']
props ={
        'KernelType':'RBF', #default is a RBF Kernel
        'SVMType':'NU',     #default is C 
        'nu':None,          # NU for SVM NU
        'c':None,           #C for SVM C - the slack variable
        'degree':None,      #degree for poly kernels - defaults to 3
        'coef':None,        #coef for Poly/Sigmoid defaults to 0
        'gamma':None,       #kernel param for poly/rbf/sigma  
    }
print('Train')
classifierSVMRBF = SVMClassifier(extractors,props)
classifierSVMRBF.train(path,classes,disp=display,subset=n) #train
print('Test')
[pos,neg,confuse] = classifierSVMRBF.test(path,classes,disp=display,subset=n)
files = glob.glob( os.path.join(path[0], '*.jpg'))
for i in range(10):
        img = Image(files[i])
        cname = classifierSVMRBF.classify(img)
        print(files[i]+' -> '+cname)
classifierSVMRBF.save('RBFSVM.pkl')
#testSVMRBF = SVMClassifier.load('RBFSVM.pkl')
#files = glob.glob( os.path.join(path[0], '*.jpg'))
#for i in range(10):
#        img = Image(files[i])
#        cname = testSVMRBF.classify(img)
#        print(files[i]+' -> '+cname)


print('###############################################################################')
print('Bayes')
extractors = [haar]
classifierBayes = NaiveBayesClassifier(extractors)#
print('Train')
path = [arbor_path,football_path,sanjuan_path]
classes = ['arbor','football','sanjuan']
classifierBayes.train(path,classes,disp=display,subset=n) #train
print('Test')
[pos,neg,confuse] = classifierBayes.test(path,classes,disp=display,subset=n)
files = glob.glob( os.path.join(path[0], '*.jpg'))
for i in range(10):
        img = Image(files[i])
        cname = classifierBayes.classify(img)
        print(files[i]+' -> '+cname)
classifierBayes.save('Bayes.pkl')
#testBayes = NaiveBayesClassifier.load('RBFSVM.pkl')
#files = glob.glob( os.path.join(path[0], '*.jpg'))
#for i in range(10):
#        img = Image(files[i])
#        cname = testBayes.classify(img)
#        print(files[i]+' -> '+cname)

print('###############################################################################')

