import pandas as pd

dataset = pd.read_csv('large_data.csv')

dataset.head()
dataset.describe()
allergy_data = dataset.loc[dataset['TYPE'] == 'ALLERGY']
cold_data = dataset.loc[dataset['TYPE'] == 'COLD']
covid_data = dataset.loc[dataset['TYPE'] == 'COVID']
flu_data = dataset.loc[dataset['TYPE'] == 'FLU']
allergy_data = dataset.loc[dataset['TYPE'] == 'ALLERGY']
cold_data = dataset.loc[dataset['TYPE'] == 'COLD']
covid_data = dataset.loc[dataset['TYPE'] == 'COVID']
flu_data = dataset.loc[dataset['TYPE'] == 'FLU']
allergy_data = dataset.loc[dataset['TYPE'] == 'ALLERGY']
cold_data = dataset.loc[dataset['TYPE'] == 'COLD']
covid_data = dataset.loc[dataset['TYPE'] == 'COVID']
flu_data = dataset.loc[dataset['TYPE'] == 'FLU']
allergy_data = dataset.loc[dataset['TYPE'] == 'ALLERGY']
cold_data = dataset.loc[dataset['TYPE'] == 'COLD']
covid_data = dataset.loc[dataset['TYPE'] == 'COVID']
flu_data = dataset.loc[dataset['TYPE'] == 'FLU']
allergy_data = dataset.loc[dataset['TYPE'] == 'ALLERGY']
cold_data = dataset.loc[dataset['TYPE'] == 'COLD']
covid_data = dataset.loc[dataset['TYPE'] == 'COVID']
flu_data = dataset.loc[dataset['TYPE'] == 'FLU']
import matplotlib.pyplot as plt
import seaborn as sb

dataset_corr = dataset.corr()
sb.heatmap(dataset_corr, annot=True)
import matplotlib.pyplot as plt
import seaborn as sb

dataset_corr = dataset.corr()
sb.heatmap(dataset_corr, annot=True)
plt.show()
import matplotlib.pyplot as plt
import seaborn as sb

dataset_corr = dataset.corr()
plt.figure(figsize=(30,30))
sb.heatmap(dataset_corr, annot=True)
import matplotlib.pyplot as plt
import seaborn as sb

dataset_corr = dataset.corr()
plt.figure(figsize=(30,20))
sb.heatmap(dataset_corr, annot=True)
dataset_cov = dataset.cov()
sb.heatmap(dataset_cov, annot=True)
dataset_cov = dataset.cov()
plt.figure(figsize=(20,20))
sb.heatmap(dataset_cov, annot=True)
dataset_cov = dataset.cov()
plt.figure(figsize=(30,20))
sb.heatmap(dataset_cov, annot=True)
sb.distplot(dataset)
sb.histplot(dataset)
sb.displot(dataset)
sb.displot(dataset, col='TYPE')
sb.displot(dataset, col="type")
sb.displot(dataset, col="TYPE")
sb.displot(dataset, col="COUGH")
sb.displot(dataset, col=dataset['TYPE'])
dataset.plot.hist(subplots=True)
plt.figure(figsize=(30, 5))
dataset.plot.hist(subplots=True)
plt.figure(figsize=(30, 5))
dataset.plot.hist(subplots=True, layout=(5, 4))
dataset.plot.hist(subplots=True, layout=(5, 4), figsize=(20, 10))
dataset.hist(subplots=True, layout=(5, 4), figsize=(20, 10))
dataset.plot.hist(subplots=True, layout=(5, 4), figsize=(20, 10))
dataset.plot.hist(subplots=True, layout=(5, 4), figsize=(20, 10))
dataset.hist(figsize=(20,10))
dataset.plot.hist(subplots=True, layout=(5, 4), figsize=(25, 10))
dataset.hist(figsize=(20,10))
dataset.plot.hist(subplots=True, layout=(4, 5), figsize=(25, 10))
dataset.hist(figsize=(20,10))
dataset.plot.hist(layout=(4, 5), figsize=(25, 10))
dataset.hist(figsize=(20,10))
dataset.plot.hist(subplots=True, layout=(4, 5), figsize=(25, 10))
dataset.hist(figsize=(20,10))
dataset.plot.hist(subplots=True, layout=(4, 5), figsize=(25, 10), legend=False)
dataset.plot.hist(subplots=True, layout=(4, 5), figsize=(25, 10), labels=False)
dataset.hist(figsize=(25, 10))
dataset.hist(figsize=(25, 14))
dataset.hist(figsize=(22, 16))
allergy_data = dataset.loc[dataset['TYPE'] == 'ALLERGY']
allergy_data.hist(figsize=(22,16))
cold_data = dataset.loc[dataset['TYPE'] == 'COLD']
cold_data.hist(figsize=(22,16))
covid_data = dataset.loc[dataset['TYPE'] == 'COVID']
covid_data.hist(figsize=(22,16))
flu_data = dataset.loc[dataset['TYPE'] == 'FLU']
flu_data.hist(figsize=(22,16))


import sklearn.preprocessing as skpre

le = skpre.LabelEncoder()
dataset['TYPE'] = le.fit_transform(dataset['TYPE'])
labels = dataset.pop('TYPE')

labels.head()
import sklearn.preprocessing as skpre

le = skpre.LabelEncoder()
dataset['TYPE'] = le.fit_transform(dataset['TYPE'])
labels = dataset.pop('TYPE')

print(labels)
import sklearn.preprocessing as skpre

le = skpre.LabelEncoder()
dataset['TYPE'] = le.fit_transform(dataset['TYPE'])
labels = dataset.pop('TYPE')
import sklearn.preprocessing as skpre

le = skpre.LabelEncoder()
dataset['TYPE'] = le.fit_transform(dataset['TYPE'])
labels = dataset.pop('TYPE')
import pandas as pd

dataset = pd.read_csv('large_data.csv')

dataset.head()
import sklearn.preprocessing as skpre

le = skpre.LabelEncoder()
dataset['TYPE'] = le.fit_transform(dataset['TYPE'])
labels = dataset.pop('TYPE')
import sklearn.preprocessing as skpre

le = skpre.LabelEncoder()
dataset['TYPE'] = le.fit_transform(dataset['TYPE'])
labels = dataset.pop('TYPE')
import sklearn.preprocessing as skpre

dataset = pd.read_csv('large_data.csv')
le = skpre.LabelEncoder()
dataset['TYPE'] = le.fit_transform(dataset['TYPE'])
labels = dataset.pop('TYPE')
import sklearn.preprocessing as skpre

dataset = pd.read_csv('large_data.csv')
le = skpre.LabelEncoder()
dataset['TYPE'] = le.fit_transform(dataset['TYPE'])
labels = dataset.pop('TYPE')
print(labels)
import sklearn.model_selection as skmodel

(train_in, test_in, train_class, test_class) = skmodel.train_test_split(dataset, labels, test_size=0.25, random_state=3)
import sklearn.preprocessing as skpre

dataset = pd.read_csv('large_data.csv')
le = skpre.LabelEncoder()
dataset['TYPE'] = le.fit_transform(dataset['TYPE'])
labels = dataset.pop('TYPE')
import sklearn.model_selection as skmodel

(train_in, test_in, train_class, test_class) = skmodel.train_test_split(dataset, labels, test_size=0.25, random_state=3)
import sklearn.preprocessing as skpre

dataset = pd.read_csv('large_data.csv')
le = skpre.LabelEncoder()
dataset['TYPE'] = le.fit_transform(dataset['TYPE'])
labels = dataset.pop('TYPE')
import sklearn.model_selection as skmodel

(train_in, test_in, train_class, test_class) = skmodel.train_test_split(dataset, labels, test_size=0.25, random_state=3)
import sklearn.tree as sktree

decision_tree = sktree.DecisionTreeClassifier()
decision_tree.fit(train_in, train_class)
decision_tree.score(test_in, test_class)
import sklearn.tree as sktree
import sklearn.metrics as skmetric

decision_tree = sktree.DecisionTreeClassifier()
decision_tree.fit(train_in, train_class)
prediction = decision_tree.predict(test_in, test_class)
skmetric.classification_report(test_class, prediction)
import sklearn.tree as sktree
import sklearn.metrics as skmetric

decision_tree = sktree.DecisionTreeClassifier()
decision_tree.fit(train_in, train_class)
prediction = decision_tree.predict(test_in)
skmetric.classification_report(test_class, prediction)
import sklearn.tree as sktree
import sklearn.metrics as skmetric

decision_tree = sktree.DecisionTreeClassifier()
decision_tree.fit(train_in, train_class)
prediction = decision_tree.predict(test_in)
print(skmetric.classification_report(test_class, prediction))
import sklearn.tree as sktree
import sklearn.metrics as skmetric

decision_tree = sktree.DecisionTreeClassifier()
decision_tree.fit(train_in, train_class)
prediction = decision_tree.predict(test_in)
print(skmetric.confusion_matrix(test_class, prediction))
print(skmetric.classification_report(test_class, prediction))
import sklearn.preprocessing as skpre

dataset = pd.read_csv('large_data.csv')
le = skpre.LabelEncoder()
dataset['TYPE'] = le.fit_transform(dataset['TYPE'])
labels = dataset.pop('TYPE')
print(le.classes_)
import sklearn.model_selection as skmodel

(train_in, test_in, train_class, test_class) = skmodel.train_test_split(dataset, labels, test_size=0.25, random_state=3)
import sklearn.tree as sktree
import sklearn.metrics as skmetric

decision_tree = sktree.DecisionTreeClassifier()
decision_tree.fit(train_in, train_class)
prediction = decision_tree.predict(test_in)
print(skmetric.confusion_matrix(test_class, prediction))
print(skmetric.classification_report(test_class, prediction))
accuracies = []
for rep in range(1000):
    (train_in, test_in, train_class, test_class) = skmodel.train_test_split(dataset, labels, test_size=0.25)
    dtc = sktree.DecisionTreeClassifier()
    dtc.fit(train_in, train_class)
    accuracies.append(dtc.score(test_in, test_class))

sb.histplot(accuracies)
cv_scores = skmodel.cross_val_score(decision_tree, dataset, labels, cv=10) 
sb.histplot(cv_scores)
print(f"Max score: {max(cv_scores)}")
print(f"Average score: {sum(cv_scores)/len(cv_scores)}")
cv_scores = skmodel.cross_val_score(decision_tree, dataset, labels, cv=10) 
sb.histplot(cv_scores)
print(f"Max score: {max(cv_scores)}")
print(f"Average score: {sum(cv_scores)/len(cv_scores)}")
cv_scores = skmodel.cross_val_score(decision_tree, dataset, labels, cv=10) 
sb.histplot(cv_scores)
print(f"Max score: {max(cv_scores)}")
print(f"Average score: {sum(cv_scores)/len(cv_scores)}")
cv_scores = skmodel.cross_val_score(decision_tree, dataset, labels, cv=10) 
sb.histplot(cv_scores)
print(f"Max score: {max(cv_scores)}")
print(f"Average score: {sum(cv_scores)/len(cv_scores)}")
parameters = {'criterion': ['gini', 'entropy'],
                  'splitter': ['best', 'random'],
                  'max_depth': [1, 2, 3, 4, 5],
                  'max_features': [1, 2, 3, 4]}

cross_val = skmodel.StratifiedKFold(n_splits=10)
grid_search = skmodel.GridSearchCV(decision_tree, param_grid=parameters, cv=cross_val)
grid_search.fit(dataset, labels)
print(f"Best score: {grid_search.best_score_}")
print(f"Best parameters: {grid_search.best_params_}")
parameters = {'criterion': ['gini', 'entropy'],
                  'splitter': ['best', 'random'],
                  'max_depth': [1, 2, 3, 4, 5, 6, None],
                  'max_features': [0.25, 0.5, 0.75, 1]}

cross_val = skmodel.StratifiedKFold(n_splits=10)
grid_search = skmodel.GridSearchCV(decision_tree, param_grid=parameters, cv=cross_val)
grid_search.fit(dataset, labels)
print(f"Best score: {grid_search.best_score_}")
print(f"Best parameters: {grid_search.best_params_}")
parameters = {'criterion': ['gini', 'entropy'],
                  'splitter': ['best', 'random'],
                  'max_depth': [1, 2, 3, 4, 5, 6, None],
                  'max_features': [0.25, 0.5, 0.75, 1.0]}

cross_val = skmodel.StratifiedKFold(n_splits=10)
grid_search = skmodel.GridSearchCV(decision_tree, param_grid=parameters, cv=cross_val)
grid_search.fit(dataset, labels)
print(f"Best score: {grid_search.best_score_}")
print(f"Best parameters: {grid_search.best_params_}")
parameters = {'criterion': ['gini', 'entropy'],
                  'splitter': ['best', 'random'],
                  'max_depth': [1, 2, 3, 4, 5, 6, None],
                  'max_features': [0.25, 0.5, 0.75, 1.0]}

cross_val = skmodel.StratifiedKFold(n_splits=10)
grid_search = skmodel.GridSearchCV(decision_tree, param_grid=parameters, cv=cross_val)
grid_search.fit(dataset, labels)
print(f"Best score: {grid_search.best_score_}")
print(f"Best parameters: {grid_search.best_params_}")
best_dt = grid_search.best_estimator_
prediction = best_dt.predict(dataset)
print(skmetric.confusion_matrix(labels, prediction))
print(skmetric.classification_report(labels, prediction))
