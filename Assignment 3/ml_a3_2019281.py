# -*- coding: utf-8 -*-
"""ML_A3_2019281.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Rd_LmJc6-bILWlkScmdCO07hbyIPukcF
"""

# Commented out IPython magic to ensure Python compatibility.
from google.colab import drive
drive.mount('/content/gdrive')
# %cd '/content/gdrive/MyDrive/ML datasets/ML A3'
# %ls

!pip install pyclustering

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)

#Read data
population_data=pd.read_csv('population.csv')
more_than_50k_data=pd.read_csv('more_than_50k.csv')
description_data=pd.read_csv('Dataset Description.csv')

pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

#Part-1.1
new_pop_data=population_data.replace(' ?',np.nan)
null_vals=new_pop_data.isnull().sum()
print(null_vals)

#Part-1.2
allowed_null_vals=(population_data.shape[0])*0.4
ind=0
indx=[]
for i in null_vals:
  if i>allowed_null_vals:
    indx.append(ind)
  ind=ind+1
  
#Drop columns
new_population_data=new_pop_data.drop(columns=new_pop_data.columns[indx])
more_than_50k_data=more_than_50k_data.drop(columns=new_pop_data.columns[indx])
print(new_population_data.shape,population_data.shape)

##Part-2.1
new_population_data.head(5)
fig, ax = plt.subplots(6, 6)
j=0
k=0
for i in new_population_data.columns:
  new_population_data[i].value_counts().plot(kind='hist',ax=ax[j][k],figsize=(250,250),fontsize=80,legend=True).set_title(i,size=90)
  if k==5:
    k=0
    j=j+1
  else:
    k=k+1
fig.show()
fig.savefig('Q1_2.png')
fig.savefig('Q1_2.pdf')


##Part-2.2
#Remove cols with 80% data in single entity
rem_cols=[]
for i in new_population_data.columns:
  if (new_population_data[i].value_counts().max()/(new_population_data.shape[0]))>=0.80:
    rem_cols.append(i)

new_population_data.drop(columns=rem_cols,inplace=True)
more_than_50k_data.drop(columns=rem_cols,inplace=True) #For part-5

print(new_population_data.shape)

#Part-3

#Part-3.1
#Replacing values in each col with there mode
for i in new_population_data.columns[new_population_data.isna().any()]:
  mode=new_population_data[i].mode()[0]
  new_population_data[i].fillna(mode,inplace=True)
  more_than_50k_data[i].fillna(mode,inplace=True)

print(new_population_data.isna().sum())

#Part-3.2
#Bucketize Numerical features
print(new_population_data.describe())

#Numerical data
cols_to_bin=['AAGE','WKSWORK']

for i in cols_to_bin:
  data=new_population_data[i]
  maxi=data.max()
  mini=data.min()
  #Calculate 4 bins of equal distribution
  bin=np.linspace(mini,maxi+1,4)
  new_population_data[i]=pd.cut(x=data,bins=bin,right=False).cat.codes

  #for more_than_50k_data
  maxi2=more_than_50k_data[i].max()
  mini2=more_than_50k_data[i].min()
  bin2=np.linspace(mini2,maxi2+1,4)
  more_than_50k_data[i]=pd.cut(x=more_than_50k_data[i],bins=bin2,right=False).cat.codes


#Part-3.3
# One hot encode features
cat_col_list=list(new_population_data.columns)
for i in cols_to_bin:
  cat_col_list.remove(i)

hot_encode=pd.get_dummies(new_population_data,columns=cat_col_list)
hot_encode_more_than_50k_data=pd.get_dummies(more_than_50k_data,columns=cat_col_list)

print(hot_encode.shape)

from sklearn.decomposition import PCA

pca=PCA(0.80)
pca=pca.fit(hot_encode)
pca_data=pca.transform(hot_encode)
pca_data_df=pd.DataFrame(pca_data)

#For more than 50k
pca2=PCA(0.80)
pca2=pca2.fit(hot_encode_more_than_50k_data)
pca_data2=pca2.transform(hot_encode_more_than_50k_data)
pca_data_df2=pd.DataFrame(pca_data2)

print(hot_encode.shape)
print(pca_data.shape)

print(hot_encode_more_than_50k_data.shape)
print(pca_data2.shape)

#Part-4
from pyclustering.cluster.kmedians import kmedians
import pickle

samples=pca_data_df.copy()
cluster=[]

for k in range(10,25):
  cluster.append(k)

# ans_final=[]

for k in cluster:
  seeds=np.random.RandomState(0).permutation(samples.shape[1])[:k]
  centers=samples.iloc[seeds]
  fname='model'+str(k+1)+'.pkl'

  Train models
  model=kmedians(samples,centers)
  model.process() 
  
  #Save models
  with open(fname,'wb') as myfile:
    pickle.dump(model,myfile)

  #Select trained models
  # with open(fname,'rb') as myfile:
  #   model=pickle.load(myfile)
  # ans_final.append(model.get_total_wce()/k)
print(ans_final)

#Plot elbow graph
plt.plot(cluster, ans_final)
plt.xlabel('Number of Clusters')
plt.ylabel('Average Distance')
plt.show()

"""From the above graph, we choose the value of k=20"""

#Selecting the best model
with open('model21.pkl','rb') as myfile:
  best_model=pickle.load(myfile)
best_model

#Part-5
#Part-4
from pyclustering.cluster.kmedians import kmedians
import pickle

samples=pca_data_df2.copy()
cluster=[]

for k in range(10,25):
  cluster.append(k)

ans_final2=[]

for k in cluster:
  seeds=np.random.RandomState(1).permutation(samples.shape[1])[:k]
  centers=samples.iloc[seeds]
  #print(centers)
  model=kmedians(samples,centers)
  model.process() 
  #Save model
  # fname='model_50k'+str(k)+'.pkl'
  # with open(fname,'wb') as myfile:
  #   pickle.dump(model,myfile)
  ans_final2.append(model.get_total_wce()/k)
print(ans_final2)

#Plot elbow graph
plt.plot(cluster, ans_final2)
plt.xlabel('Number of Clusters')
plt.ylabel('Average Distance')
plt.show()

"""From the above graph, we choose the value of k=20."""

#Selecting the best model
with open('model_50k20.pkl','rb') as myfile:
  best_model_50k=pickle.load(myfile)
best_model_50k

#Part-6
best_genpop_results=best_model.predict(pca_data)
best_50k_results=best_model_50k.predict(pca_data2)
best_genpop_results=pd.Series(best_genpop_results)
best_50k_results=pd.Series(best_50k_results)
df1=pd.DataFrame(best_genpop_results.value_counts().sort_index(),columns=['General Population'])
df2=pd.DataFrame(best_50k_results.value_counts().sort_index(),columns=['50k population'])

df1.shape,df2.shape

#Part-6.1
plt.figure(figsize=(10,10))
# fig, (ax1, ax2) = plt.subplots(1, 2)
df1.plot(kind='bar',xlabel='Clusters',ylabel='Count',colormap='RdYlGn',legend=True,figsize=(8,8))
plt.show()

plt.figure(figsize=(10,10))
df2.plot(kind='bar',xlabel='Clusters',ylabel='Count',colormap='RdYlBu_r',legend=True,figsize=(8,8))
plt.show()
# fig.show()

#Part-6.2
total1=df1.sum()[0]
total2=df2.sum()[0]

cluster=0
#Print results
print('Over-representation with respect to General Population in 50k Population')
for i in df2['50k population']:
  diff=i/total2
  diff=(diff-df1['General Population'][cluster]/total1)
  diff=diff*100
  if diff>0:
    print(f'Cluster {cluster+1} is over-represented by {diff}%')
  cluster=cluster+1

cluster=0
print('\n\nOver-representation with respect to 50k Population in General Population')
for i in df1['General Population']:
  diff=i/total1
  diff=(diff-df2['50k population'][cluster]/total2)
  diff=diff*100
  if diff>0:
    print(f'Cluster {cluster+1} is over-represented by {diff}%')
  cluster=cluster+1

#Part-6.3
cluster_list=[3,4,5,6,9,10,11,14,15,16,19]
cluster_list2=[0,1,2,7,8,12,13,17,18]

#Taking pca inverse
inv_pca=pca.inverse_transform(best_model.get_medians())
peoples=pd.DataFrame(inv_pca,columns=hot_encode.columns)

#Prinintng the results
print('overrepresented in the more_than_50k data compared to the general population')
peoples.iloc[cluster_list]

#Part-6.4
print('overrepresented in the General population data compared to the more_than_50k')
peoples.iloc[cluster_list2]