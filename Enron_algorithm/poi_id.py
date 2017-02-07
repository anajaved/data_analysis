#!/usr/bin/python

import sys
import pickle
import pandas as pd 
import matplotlib.pyplot as plt
import numpy 

from tester import test_classifier

sys.path.append("../tools/")

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data


### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature is "poi".


outliers = ['TOTAL', 'LOCKHART EUGENE E', 'THE TRAVEL AGENCY IN THE PARK']

### Load the dictionary containing the dataset
### Task 2: Remove outliers, create visualizations
### Task 3: Create new feature 

with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)

for point in data_dict.items():
    if point[0] in outliers:
        data_dict.pop(point[0])
    
    salary = point[1]['salary']
    bonus=point[1]['bonus']
    sb_ratio= float(bonus)/float(salary)
    shared_email = point[1]['shared_receipt_with_poi']
    total_stock= point[1]['total_stock_value']
    ss_ratio= float(total_stock)/float(salary)
    point[1]["sb_ratio"]=sb_ratio
    point[1]['ss_ratio']=ss_ratio
    
    plt.scatter(sb_ratio, shared_email )
    
#plt.show()

features_list = ['poi', 'salary', 
'total_payments', 'bonus', 'restricted_stock_deferred', 
'deferred_income', 'total_stock_value', 'exercised_stock_options', 
'long_term_incentive', 'restricted_stock' ,
 'shared_receipt_with_poi', 'from_poi_to_this_person'] 

    
df = pd.DataFrame.from_records(list(data_dict.values()))
df.set_index(pd.Series(list(data_dict.keys())), inplace=True) 

df.replace(to_replace= 'NaN', value= 0,inplace=True)
data_dict= df.to_dict('index')

my_dataset = data_dict

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn import tree
from sklearn import cross_validation
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.decomposition import PCA
from sklearn import tree
from sklearn.preprocessing import MinMaxScaler 
from sklearn.naive_bayes import GaussianNB


features_train, features_test, labels_train, labels_test = cross_validation.train_test_split(
	features, labels, test_size=0.3, random_state=42)
	

### Task 4: Try a varity of classifiers

#Decision Tree classifier
'''
parameters = {"pca__n_components": range(2,12), 
              'tree__criterion': ('gini','entropy'),
              'tree__splitter':('best','random'),
              'tree__min_samples_split':[3,4,5,10],
                'tree__max_depth':[10,15,20],
                'tree__max_leaf_nodes':[5,10,25]}
                
pca=PCA()
tree= tree.DecisionTreeClassifier()
pipe= Pipeline(steps=[('pca', pca), ('tree', tree)])

clf= GridSearchCV(pipe, parameters)
clf= clf.fit(features_train, labels_train)
clf=clf.best_estimator_

predictions = clf.predict(features_test)
print "accuracy", accuracy_score(predictions, labels_test)
'''

#SVC classifier

'''
from sklearn.svm import SVC
cv=StratifiedShuffleSplit(labels, 100)
pca=PCA()
svc= SVC()

parameters = {"pca__n_components": range(1,12), 
                "pca__whiten": [False,True],
                "svc__kernel": ['linear', 'rbf'],
                "svc__C": [1, 10, 100]}
                
pipe= Pipeline(steps=[('scaler', MinMaxScaler(copy=True, feature_range=(0, 1))),('pca', pca), ('svc', svc)])
gs = GridSearchCV(pipe, parameters, cv=cv, scoring="f1")
gs.fit(features, labels)
clf=gs.best_estimator_

predictions = clf.predict(features_test)
print accuracy_score(predictions, labels_test) 
'''         


#Naive Bayes Classifier 


cv=StratifiedShuffleSplit(labels, 100)
pca=PCA()
gnb = GaussianNB()

pipe= Pipeline(steps=[('scaler', MinMaxScaler(copy=True, feature_range=(0, 1))),('pca', pca), ('gnb', gnb)])
                
parameters = {"pca__n_components": range(1,12), 
                "pca__whiten": [False,True]
             }


gs = GridSearchCV(pipe, parameters, cv=cv, scoring="f1")
gs.fit(features, labels)
clf=gs.best_estimator_

predictions = clf.predict(features_test)

print accuracy_score(predictions, labels_test)



### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. 

from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score

prec= precision_score(labels_test, predictions)
recall = recall_score(labels_test, predictions)
f1= f1_score(labels_test, predictions) 

print "precision", prec
print "recall", recall 
print "f1", f1

test_classifier(clf, my_dataset, features_list)

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

dump_classifier_and_data(clf, my_dataset, features_list)

'''
GB:

output w/ created features:
Pipeline(steps=[('scaler', MinMaxScaler(copy=True, feature_range=(0, 1))), ('pca', PCA(copy=True, n_components=6, whiten=True)), ('gnb', GaussianNB())])
	Accuracy: 0.85147	Precision: 0.43545	Recall: 0.38450	F1: 0.40839	F2: 0.39371
	Total predictions: 15000	True positives:  769	False positives:  997False negatives: 1231	True negatives: 12003
	
w/o features:
Pipeline(steps=[('scaler', MinMaxScaler(copy=True, feature_range=(0, 1))), ('pca', PCA(copy=True, n_components=4, whiten=False)), ('gnb', GaussianNB())])
	Accuracy: 0.84613	Precision: 0.41782	Recall: 0.39150	F1: 0.40423	F2: 0.39650
	Total predictions: 15000	True positives:  783	False positives: 1091	False negatives: 1217	True negatives: 11909
	
##########################################################################################


SVC Results:

Pipeline(steps=[('scaler', MinMaxScaler(copy=True, feature_range=(0, 1))), ('pca', PCA(copy=True, n_components=3, whiten=True)), ('svc', SVC(C=100, cache_size=200, class_weight=None, coef0=0.0,
  decision_function_shape=None, degree=3, gamma='auto', kernel='rbf',
  max_iter=-1, probability=False, random_state=None, shrinking=True,
  tol=0.001, verbose=False))])
	Accuracy: 0.84847	Precision: 0.34400	Recall: 0.15050	F1: 0.20939	F2: 0.16958
	Total predictions: 15000	True positives:  301	False positives:  574	False negatives: 1699	True negatives: 12426
'''
