# -*- coding: utf-8 -*-
"""BankCreditCardApprovalPrediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1jCltUGZP4i7RFfK-gYskoqvxRsfsZeQ3
"""

import pandas as pd

"""# Loading Files"""

data = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/application_record.csv')
record = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/credit_record.csv')

"""## No of Rows"""

print('Total No. of rows in data: ',data.shape[0])
print('Total No. of rows in record: ',record.shape[0])

"""## No of Columns"""

print('Total No. of columns in data: ',data.shape[1])
print('Total No. of columns in record: ',record.shape[1])

data.columns

record.columns

data.dtypes

record.dtypes

data.head()

record.head()

"""# Preprocessing"""

record['STATUS'].unique()

"""
  0 : 1 Month past due

  1 : 1-2 Month past due

  2 : 2-3 Month Overdue

  3 : 3-4 Month Overdue

  4 : 4-5 Month Overdue

  5 : Overdue or Bad Debts

  C : Paid Off that month

  X : No loan for the month
"""

begin_months = record.groupby(['ID'])['MONTHS_BALANCE'].agg(min)

begin_month=pd.DataFrame(begin_months)
begin_month.rename(columns={'MONTHS_BALANCE':'Total Months'},inplace=True)
new_data=pd.merge(data,begin_month,how="left",on="ID")

record['target'] = None
record.loc[record['STATUS'].isin(['2','3','4','5']),'target'] = 'Yes'

record.head()

record['target'].unique()

temp = record.groupby('ID').count()
print(temp['target'].unique())
temp['target'][temp['target'] > 0] = 'Yes' # Specify Default
temp['target'][temp['target'] == 0] = 'No' # Specify Non Default
temp = temp[['target']]  # Only store target column
new_data = pd.merge(new_data, temp, how='inner', on='ID')
new_data['target'] = new_data['target'].map({'Yes': 1, 'No': 0})
new_data # here it includes target column

new_data['target'].unique()

"""# Feature Engineering

Days Birth Column
"""

new_data['Age'] = new_data['DAYS_BIRTH'].abs()//365
print(new_data['Age'])
new_data.drop(['DAYS_BIRTH'],axis=1,inplace=True)

"""Days Employed Column"""

new_data['Job Experiance'] = new_data['DAYS_EMPLOYED'].abs()//365
print(new_data['Job Experiance'])
new_data.drop(['DAYS_EMPLOYED'],axis=1,inplace=True)

"""# Renaming Columns"""

new_data.rename(columns={'CODE_GENDER':'Gender','FLAG_OWN_CAR':'Car','FLAG_OWN_REALTY':'Real Estate Owned',
                         'CNT_CHILDREN':'Total Children','AMT_INCOME_TOTAL':'Income',
                         'NAME_EDUCATION_TYPE':'Education','NAME_FAMILY_STATUS':'Marital Status',
                        'NAME_HOUSING_TYPE':'Housing Type','FLAG_EMAIL':'Email','FLAG_MOBIL':'Mobile',
                         'NAME_INCOME_TYPE':'Income Type','FLAG_WORK_PHONE':'Work Phone',
                         'FLAG_PHONE':'Phone','CNT_FAM_MEMBERS':'Total Family Members',
                        'OCCUPATION_TYPE':'Occupation Type','target':'Target'
                        },inplace=True)
new_data.columns

"""# Separate Categorical And Numerical Columns"""

for col in new_data.columns:
  print(col,':',new_data[col].unique())

"""### From above we can see that mobile has only one value which is 1.
So the mobile column must be removed.
"""

new_data.drop(['Mobile'],axis=1,inplace=True)

num_col = new_data.select_dtypes(exclude=object).columns
cat_col = new_data.select_dtypes(include=object).columns
print('Numerical Column: \n',num_col)
print('\nCategorical Columns:\n',cat_col)

num_col = num_col.drop('Target')
num_col = num_col.drop('ID')

"""# Missing Values"""

new_data.isna().sum()

# See Percent Missing Values in Occupation Type
miss_rows = new_data['Occupation Type'].isna().sum()
total_rows = new_data['Occupation Type'].shape[0]
print('Missing Rows: ',miss_rows)
print('Total Rows: ',total_rows)
percent_missing = (miss_rows/total_rows)*100
print('Missing Percentage: ',percent_missing)

new_data['Occupation Type'].unique()

new_data['Occupation Type'].fillna('Unknown',inplace=True)

new_data.isna().sum()

new_data['Target'][new_data['Occupation Type']=='Unknown'].value_counts()

new_data

"""# Total 1 and 0"""

# Calculate percentage of 1's and 0's in dataset
# 1: Default
# 0: Non Default
zeros = new_data['Target'].value_counts()[0]
ones = new_data['Target'].value_counts()[1]
print('No of Ones: ',ones)
print('No of Zeros: ',zeros)
print('Percentage of Ones: ',(ones/(ones+zeros))*100)
print('Percentage of Zeros: ',(zeros/(ones+zeros))*100)

"""## Drop Duplicates"""

new_data.drop_duplicates(inplace=True)

new_data.describe()

"""## Encoding"""

cat_col

for col in cat_col:
  print(col,': ',new_data[col].unique())

nominal_col = ['Gender', 'Car','Real Estate Owned','Marital Status']
ordinal_col = ['Income Type','Education','Housing Type','Occupation Type']

"""# Nominal Encoding"""

nominal_col

"""### Marital Status"""

for status in new_data['Marital Status'].unique():
  print(status,':',new_data['Marital Status'][new_data['Marital Status']==status].value_counts()[0])

new_data['Marital Status'][new_data['Marital Status']=='Civil marriage'] = 'Married'
new_data['Marital Status'][new_data['Marital Status']=='Single / not married'] = 'Single'
new_data['Marital Status'][new_data['Marital Status']=='Separated'] = 'Single'
new_data['Marital Status'][new_data['Marital Status']=='Widow'] = 'Single'

for status in new_data['Marital Status'].unique():
  print(status,':',new_data['Marital Status'][new_data['Marital Status']==status].value_counts()[0])

"""### Income Type"""

new_data['Income Type'].unique()
new_data['Income Type'].value_counts()

new_data['Income'][new_data['Income Type']=='Student']

new_data.to_csv('Dataset.csv',index=False)

"""## One Hot Encoding"""

new_data = pd.get_dummies(new_data,columns=nominal_col)

new_data.head()

"""# Ordinal Encoding"""

ordinal_col

new_data['Income Type'].value_counts() # Encoding based on frequency/counts

new_data['Education'].value_counts()

new_data['Housing Type'].value_counts()

new_data['Occupation Type'].value_counts()

income_type=['Student','State servant','Pensioner','Commercial associate','Working']
education=['Lower secondary','Secondary / secondary special','Incomplete higher','Higher education','Academic degree']
house_type=['Co-op apartment','Office apartment','Rented apartment','Municipal apartment','With parents','House / apartment']

new_data.loc[new_data['Occupation Type'].isin(['Managers', 'Medicine staff', 'Accountants', 'High skill tech staff', 'IT staff', 'HR staff', 'Core staff']), 'Occupation Type'] = 'Professional/Management'
new_data.loc[new_data['Occupation Type'].isin(['Core staff', 'Sales staff', 'Private service staff', 'Secretaries', 'Realty agents', 'Security staff', 'Cooking staff', 'Drivers']), 'Occupation Type'] = 'Skilled Workers'
new_data.loc[new_data['Occupation Type'].isin(['Laborers', 'Low-skill Laborers', 'Waiters/barmen staff', 'Cleaning staff']), 'Occupation Type'] = 'Laborers'

occupation_type = ['Unknown','Laborers','Skilled Workers','Professional/Management']

from sklearn.preprocessing import OrdinalEncoder

oe = OrdinalEncoder(categories=[income_type,education,house_type,occupation_type])
oe.fit(new_data[ordinal_col])
new_data[ordinal_col] = oe.transform(new_data[ordinal_col])
print(oe.categories_)

new_data

for col in ordinal_col:
  print(col,': ',new_data[col].unique())

new_data.dtypes

new_data.head()

"""# Standard Scaler"""

from sklearn.preprocessing import StandardScaler

sc = StandardScaler()

sc.fit(new_data.loc[:,num_col])

new_data.loc[:,num_col] = sc.transform(new_data.loc[:,num_col])

new_data.head()

new_data.describe()

"""# Outlier Handling"""

def outlier_treament_zscore(df , cont_columns):
    """
    This is a function for treatment of outliers
    In given data column by columns
    Here Z-score / Standard scaler technique is used
    Z_score = (x-mu)/sigma
    mu => mean of the column
    sigma => std_dev of a column
    Here we
    replace all outliers in every column one by one
    when value < -3 replace with -3 and value > 3 replace with 3
    """
    for col in cont_columns:
        df.loc[df[col] < -3 , col] = -3
        df.loc[df[col] > 3 , col] = 3
    return df

new_data = outlier_treament_zscore(new_data,num_col)

new_data.describe()

new_data.dtypes

num_col

import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(30,18))
sns.heatmap(new_data.corr(),cmap='summer', annot=True, square=True,  )
plt.show()

"""# X and Y"""

Y = new_data['Target']
X = new_data.drop(['Target','ID'],axis=1)

X.shape,Y.shape

"""# SMOTE"""

from imblearn.over_sampling import SMOTE

Y = Y.astype('int')
sm = SMOTE()
X_balance,Y_balance = sm.fit_resample(X,Y)
X_balance = pd.DataFrame(X_balance, columns = X.columns)

print(Y_balance.value_counts())

"""# Train Test Split"""

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X_balance,Y_balance,
                                                    stratify=Y_balance, test_size=0.3,
                                                    random_state = 100)

y_train.value_counts(),y_test.value_counts()

"""# Supervised Algorithm

# Logistic Regression
"""

from sklearn.metrics import classification_report,confusion_matrix

from sklearn.linear_model import LogisticRegression

model = LogisticRegression(C=0.8,
                           random_state=0,
                           solver='lbfgs')
model.fit(X_train, y_train)
y_predict = model.predict(X_test)
print(classification_report(y_test,y_predict))
print(confusion_matrix(y_test,y_predict))

"""# Decision Tree"""

from sklearn.tree import DecisionTreeClassifier

model = DecisionTreeClassifier(max_depth=12,
                               min_samples_split=8,
                               random_state=1024)
model.fit(X_train, y_train)
y_predict = model.predict(X_test)
print(classification_report(y_test,y_predict))
print(confusion_matrix(y_test,y_predict))

"""# RandomForest"""

from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(n_estimators=250,
                              max_depth=12,
                              min_samples_leaf=16
                              )
model.fit(X_train, y_train)
y_predict = model.predict(X_test)
print(classification_report(y_test,y_predict))
print(confusion_matrix(y_test,y_predict))

"""# SVM"""

from sklearn import svm

model = svm.SVC(C = 0.8,
                kernel='linear')
model.fit(X_train, y_train)
y_predict = model.predict(X_test)
print(classification_report(y_test,y_predict))
print(confusion_matrix(y_test,y_predict))

"""# LightGBM"""

from lightgbm import LGBMClassifier

model = LGBMClassifier(num_leaves=31,
                       max_depth=8,
                       learning_rate=0.02,
                       n_estimators=250,
                       subsample = 0.8,
                       colsample_bytree =0.8
                      )
model.fit(X_train, y_train)
y_predict = model.predict(X_test)
print(classification_report(y_test,y_predict))
print(confusion_matrix(y_test,y_predict))

"""# XGBoost"""

from xgboost import XGBClassifier

model = XGBClassifier(max_depth=12,
                      n_estimators=250,
                      min_child_weight=8,
                      subsample=0.8,
                      learning_rate =0.02,
                      seed=42)

model.fit(X_train, y_train)
y_predict = model.predict(X_test)
print(classification_report(y_test,y_predict))
print(confusion_matrix(y_test,y_predict))

"""# Catboost"""

pip install catboost

from catboost import CatBoostClassifier

model = CatBoostClassifier(iterations=250,
                           learning_rate=0.2,
                           od_type='Iter',
                           verbose=25,
                           depth=16,
                           random_seed=42)

model.fit(X_train, y_train)
y_predict = model.predict(X_test)
print(classification_report(y_test,y_predict))
print(confusion_matrix(y_test,y_predict))

