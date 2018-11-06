#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 22:04:04 2018

@author: kathleenyoung
Kathleen Young
IEMS 308 Assignment 1: Clustering
Copyright 2018

Solve a clustering problem using the Medicare Provider Utilization Payment
Public Use File database.

The file can be found here:
https://www.cms.gov/Research-Statistics-Data-and-Systems/Statistics-Trends-and-Reports/Medicare-Provider-Charge-Data/Physician-and-Other-Supplier2015.html
"""
#Importing necessary packages
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import collections as cl
import matplotlib
from sklearn.metrics import silhouette_samples, silhouette_score
import matplotlib.cm as cm
#from sklearn import preprocessing
#import matplotlib.patches as mpatches

#Reading the Medicare data
data = pd.read_csv("Medicare_Provider_Util_Payment_PUF_CY2015.txt", sep='\t')

####################
#1. Data exploration
####################

#Histograms of features

#average_Medicare_payment_amt: Average amount that Medicare paid after
#deductible and coninsurance amounts have been deducted for the line item service
average_Medicare_payment_amt = data.average_Medicare_payment_amt.dropna(axis=0, how='any')
#hist of given data, ugly
plt.hist(average_Medicare_payment_amt, bins=100)
plt.xlabel('$'), plt.ylabel('Frequency')
plt.title('Average Medicare Payment Amount')
#log(), pretty, normal
plt.hist(np.log(average_Medicare_payment_amt), bins=100, range = (-10,10))
plt.xlabel('log($)'), plt.ylabel('Frequency')
plt.title('Log of Average Medicare Payment Amount')

#average_submitted_chrg_amt, Average amount that Medicare paid after deductible
average_submitted_chrg_amt = data.average_submitted_chrg_amt.dropna(axis=0, how='any')
#hist of given data, ugly
plt.hist(average_submitted_chrg_amt, bins = 100)
plt.xlabel('$'), plt.ylabel('Frequency')
plt.title('Average Submitted Charge Amount')
#log(), pretty, normal
plt.hist(np.log(average_submitted_chrg_amt), bins = 100)
plt.xlabel('log($)'), plt.ylabel('Frequency')
plt.title('Log of Average Submitted Charge Amount')

#Extracting the top 4 most common provider_types
provider_type = data.provider_type.dropna(axis=0, how='any')
#Find and print the distinct types
provider_types = set(list(provider_type))
print(provider_types)
#Print the number of distinct types
len(list(provider_types))
#Count and printthe number of items belonging to each data type
cnt = cl.Counter(list(provider_type))
print(cnt)

#Removing all other provider_types
top_4_practices = ['Diagnostic Radiology', 'Internal Medicine', 'Family Practice', 'Cardiology']
top_4_data = data[data.provider_type.isin(top_4_practices)]
#Comparing how much data is left over
len(data)
len(top_4_data)

#Plotting average_Medicare_payment_amt and average_submitted_chrg_amt for top 4
average_submitted_chrg_amt_top_4 = top_4_data.average_submitted_chrg_amt.dropna(axis=0, how='any')
average_Medicare_payment_amt_top_4 = top_4_data.average_Medicare_payment_amt.dropna(axis=0, how='any')
#Original data
plt.plot(average_submitted_chrg_amt_top_4, average_Medicare_payment_amt_top_4, 'ro')
plt.xlabel('Average submitted charge amount, $')
plt.ylabel('Average Medicare Payment, $')
plt.title('Amount Medicare Paid VS Submitted Charge')
#Logged data
plt.plot(np.log(average_submitted_chrg_amt_top_4), np.log(average_Medicare_payment_amt_top_4), 'ro')
plt.xlabel('Log of Average submitted charge amount, log($)')
plt.ylabel('Log of Average Medicare Payment, log($)')
plt.title('Log of Amount Medicare Paid VS Log of Submitted Charge')

#Taking the log of everything for analysis
#Isolating the numeric columns
log_data = top_4_data[["average_submitted_chrg_amt",
                       "average_Medicare_payment_amt"]].dropna(axis=0, how="any")
#Taking the log
log_data = np.log(log_data)
#Adding the provider type back in for reference
log_data['provider_type'] = top_4_data.provider_type
#log_data = pd.DataFrame({'log_data':top_4_data.provider_type})
#Dropping -inf and NA values from the dataframe caused by log and checking lengths
log_data = log_data[log_data != -np.inf]
len(log_data)
log_data = log_data.dropna(axis=0, how="any")
len(log_data)

#Plotting with colors based on provider_type
provider_lst = list(log_data.provider_type)
colors = ['red','green','blue','purple']
#Ensuring they are the same length before plotting
print(len(provider_lst))
print(len(log_data.average_submitted_chrg_amt))
#Replacing strings with integer labels
provider_lst = [1 if x == "Diagnostic Radiology" else x for x in provider_lst]
provider_lst = [2 if x == "Internal Medicine" else x for x in provider_lst]
provider_lst = [3 if x == "Family Practice" else x for x in provider_lst]
provider_lst = [4 if x == "Cardiology" else x for x in provider_lst]
#Plotting and creating a legend
plt.scatter(log_data.average_submitted_chrg_amt, log_data.average_Medicare_payment_amt,
          c=provider_lst,cmap=matplotlib.colors.ListedColormap(colors))
plt.xlabel('Log of Average submitted charge amount, log($)')
plt.ylabel('Log of Average Medicare Payment, log($)')
plt.title('Color Coded Provider Type')
red_patch = matplotlib.patches.Patch(color='red', label='Diagnostic Radiology')
green_patch = matplotlib.patches.Patch(color='green', label='Internal Medicine')
blue_patch = matplotlib.patches.Patch(color='blue', label='Family Practice')
purple_patch = matplotlib.patches.Patch(color='purple', label='Cardiology')
plt.legend(handles=[red_patch, green_patch, blue_patch, purple_patch])
plt.show()

################################################
#2. Selecting the appropriate number of clusters
################################################

#Isolate the numerical logged variables again
log_data = log_data[["average_submitted_chrg_amt","average_Medicare_payment_amt"]]

#Using the k-means algorithm and computing objective score on...
#2 clusters
kmeans_2 = KMeans(n_clusters=2, random_state=1).fit(log_data)
score_2 = kmeans_2.score(log_data)
print(score_2)
#3 clusters
kmeans_3 = KMeans(n_clusters=3, random_state=1).fit(log_data)
score_3 = kmeans_3.score(log_data)
print(score_3)
#4 clusters
kmeans_4 = KMeans(n_clusters=4, random_state=1).fit(log_data)
score_4 = kmeans_4.score(log_data)
print(score_4)
#5 clusters
kmeans_5 = KMeans(n_clusters=5, random_state=1).fit(log_data)
score_5 = kmeans_5.score(log_data)
print(score_5)
#6 clusters
kmeans_6 = KMeans(n_clusters=6, random_state=1).fit(log_data)
score_6 = kmeans_6.score(log_data)
print(score_6)
#7 clusters
kmeans_7 = KMeans(n_clusters=7, random_state=1).fit(log_data)
score_7 = kmeans_7.score(log_data)
print(score_7)
#8 clusters
kmeans_8 = KMeans(n_clusters=8, random_state=1).fit(log_data)
score_8 = kmeans_8.score(log_data)
print(score_8)
#9 clusters
kmeans_9 = KMeans(n_clusters=9, random_state=1).fit(log_data)
score_9 = kmeans_9.score(log_data)
print(score_9)
#10 clusters
kmeans_10 = KMeans(n_clusters=10, random_state=1).fit(log_data)
score_10 = kmeans_10.score(log_data)
print(score_10)

#Creating the scree plot
scores = np.array([abs(score_2), abs(score_3), abs(score_4), abs(score_5),
                   abs(score_6), abs(score_7), abs(score_8), abs(score_9),
                   abs(score_10)])
clusters = np.array([2, 3, 4, 5, 6, 7, 8, 9, 10])
plt.plot(clusters, scores, 'ro')
plt.xlabel('Number of clusters')
plt.ylabel('Objective value')
plt.title('Scree Plot')
plt.axvline(x=7)

#It appears that kmeans_7 is the best choice. Run the k-means alg again, as
#it only seems capable of storing one k-means at a time.
kmeans_7 = KMeans(n_clusters=7, random_state=1).fit(log_data)

#####################
#3. Plotting clusters
#####################

#Finding cluster labels and centroids
labels = kmeans_7.labels_
centroids = kmeans_7.cluster_centers_
#Turning the data into an array
log_data_array = np.array(log_data)

#Plotting the clusters based on color
for i in range(7):
    # select only data observations with cluster label == i
    ds = log_data_array[np.where(labels==i)]
    # plot the data observations
    plt.plot(ds[:,0],ds[:,1],'o')
    # plot the centroids
    lines = plt.plot(centroids[i,0],centroids[i,1],'kx')
    # make the centroid x's bigger
    plt.setp(lines,ms=15.0)
    plt.setp(lines,mew=2.0)
plt.xlabel('Log of Average submitted charge amount, log($)')
plt.ylabel('Log of Average Medicare Payment, log($)')
plt.title('Color Coded According to Cluster')
plt.show()

###############################################
#4. Silhouettes and effectiveness of clustering
###############################################

#Create a random sample of the data
sample_data = np.array(log_data.sample(frac=0.0001, random_state=10))

#Set up the plot
fig, ax1 = plt.subplots(1, 1)
fig.set_size_inches(18, 7)
ax1.set_xlim([-0.1, 1])
ax1.set_ylim([0, len(sample_data) + (7 + 1) * 10])

#Initialize the clusterer
clusterer = KMeans(n_clusters=7, random_state=10)
cluster_labels = clusterer.fit_predict(sample_data)

#Find the average silhouette value
silhouette_avg = silhouette_score(sample_data, cluster_labels)
print(silhouette_avg)

#Compute the silhouette scores for each sample
sample_silhouette_values = silhouette_samples(sample_data, cluster_labels)

#Create the silhouette plots
y_lower = 10
for i in range(7):
    #Aggregate the silhouette scores for samples belonging to
    #cluster i, and sort them
    ith_cluster_silhouette_values = sample_silhouette_values[cluster_labels == i]
    ith_cluster_silhouette_values.sort()
    size_cluster_i = ith_cluster_silhouette_values.shape[0]
    y_upper = y_lower + size_cluster_i
    #Create the colors
    color = cm.spectral(float(i) / 7)
    ax1.fill_betweenx(np.arange(y_lower, y_upper),
                      0, ith_cluster_silhouette_values,
                      facecolor=color, edgecolor=color, alpha=0.7)
    #Label the silhouette plots with their cluster numbers at the middle
    ax1.text(-0.05, y_lower + 0.5 * size_cluster_i, str(i))
    #Compute the new y_lower for next plot
    y_lower = y_upper + 10  # 10 for the 0 samples

#Label the silhouette plot
ax1.set_title("Silhouette plot for the various clusters.")
ax1.set_xlabel("Silhouette coefficient values")
ax1.set_ylabel("Cluster label")

#Create a vertical line showing the average silhouette value
ax1.axvline(x=silhouette_avg, color="red", linestyle="--")

ax1.set_yticks([])  # Clear the yaxis labels / ticks
ax1.set_xticks([-0.1, 0, 0.2, 0.4, 0.6, 0.8, 1])
plt.suptitle(("Silhouette analysis for KMeans clustering on sample data with n_clusters = 4"),
                 fontsize=14, fontweight='bold')
plt.show()
