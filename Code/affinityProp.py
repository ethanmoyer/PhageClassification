#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 13:27:20 2018

@author: ethanmoyer
"""

from sklearn.cluster import AffinityPropagation
from sklearn import metrics
import statistics
import numpy as np
from sklearn.datasets.samples_generator import make_blobs
from scipy.spatial import distance
import math as math
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


def euclidean_distance(x,y):
    return abs((x[0]-y[0])**2)

def affinitytest(namecolumn, envcolumn):
    with open('W:/MoreInfo.csv', 'r') as text:
        AverageTempArray = []
        Name = []
        for row in text:
            newrow=row.split(",")
            if(newrow[envcolumn] != "*"):
                AverageTempArray.append(newrow[envcolumn])
                Name.append(newrow[namecolumn])
        del AverageTempArray[0]
        del Name[0]
        AveTempArray=[]
        for item in range(0,len(AverageTempArray)):
            number=float(AverageTempArray[item])
            AveTempArray.append([number])
        X = AveTempArray
        distance = [] 
        for i in range(0,len(X)):
            for j in range(i, len(X)):
                distance.append(euclidean_distance(X[i], X[j]))
        median = -statistics.median(distance)
        maximum = -np.amax(distance)
        af = AffinityPropagation(damping=0.9,preference=maximum).fit(X)
        cluster_centers_indices = af.cluster_centers_indices_
        center = af.cluster_centers_
        clusters = list(af.labels_)
        n_clusters_ = len(cluster_centers_indices)
        clusternumbers=[]
        for num in range(0, n_clusters_):
            clusternumbers.append(clusters.count(num))
        PhageClusters={}
        for d in range(len(clusters)):
            if clusters[d] in PhageClusters.keys():
                PhageClusters[clusters[d]].append(Name[d])
            else:
                PhageClusters[clusters[d]]=[Name[d]]
        return(PhageClusters, len(PhageClusters.keys()))
    
def specialcluster(namecolumn, gencolumn):
    with open('W:/MoreInfo.csv', 'r') as text:
        AverageTempArray = []
        Name = []
        for row in text:
            newrow=row.split(",")
            if(newrow[gencolumn] != "*"):
                AverageTempArray.append(newrow[gencolumn])
                Name.append(newrow[namecolumn])
        del AverageTempArray[0]
        del Name[0]
        AveTempArray=[]
        for item in range(0,len(AverageTempArray)):
            number=float(AverageTempArray[item])
            AveTempArray.append([number])
        X = AveTempArray
        distance = [] 
        for i in range(0,len(X)):
            for j in range(i, len(X)):
                distance.append(euclidean_distance(X[i], X[j]))
        median = -statistics.median(distance)
        maximum = -np.amax(distance)
        af = AffinityPropagation(damping=0.9,preference=maximum).fit(X)
        cluster_centers_indices = af.cluster_centers_indices_
        center = af.cluster_centers_
        clusters = list(af.labels_)
        n_clusters_ = len(cluster_centers_indices)
        clusternumbers=[]
        for num in range(0, n_clusters_):
            clusternumbers.append(clusters.count(num))
        PhageClusters={}
        for d in range(len(clusters)):
            if clusters[d] in PhageClusters.keys():
                PhageClusters[clusters[d]].append(Name[d])
            else:
                PhageClusters[clusters[d]]=[Name[d]]
        newdict = {}
        for genetic_label in PhageClusters.keys():
            for name in PhageClusters[genetic_label]:
                newdict[name] = genetic_label
    return(newdict, len(PhageClusters.keys()))


def create_contingency(namecolumn, envcolumn, gencolumn):
    envcluster = affinitytest(namecolumn, envcolumn)[0]
    if(gencolumn == 9):
        gencluster = specialcluster(namecolumn, gencolumn)[0]
        gencluster_length = specialcluster(namecolumn, gencolumn)[1]
      #  print(gencluster)
        biglist = []
        for env_key in envcluster.keys():
            littlelist = []
            for q in range(0, gencluster_length):
                littlelist.append(0)
     #       print(littlelist)
            for phagename in envcluster[env_key]:
                loc = gencluster[phagename]
                littlelist[loc] += 1
            biglist.append(littlelist)
        return(biglist)
    elif(gencolumn == 1):
        biglist = []
        more_info = {}
        with open('W:/MoreInfoTest.csv', 'r') as text: 
            for row in text:
                newrow = row.split(",")
                if (newrow[1] != '*'):
                    more_info[newrow[0]] = newrow[1]
        for env_key in envcluster.keys():
            littlelist = [0, 0, 0]
            for phagename in envcluster[env_key]:
                if(phagename in more_info):
                    if more_info[phagename] == "CLR":
                        littlelist[0] += 1
                    elif more_info[phagename] == "OVC":
                        littlelist[1] += 1
                    elif more_info[phagename] == "SCT":
                        littlelist[2] += 1
            biglist.append(littlelist)
        return(biglist)
    else:
        biglist2 = []
        more_info2 = {}
        with open('W:/MoreInfoTest.csv', 'r') as text: #CHANGE THIS
            for row in text:
                newrow = row.split(",")
                if(newrow[gencolumn] != '*'):
                    more_info2[newrow[0]] = newrow[gencolumn]
        for env_key in envcluster.keys():
            littlelist = [0, 0]
            for phagename in envcluster[env_key]:
                if(phagename in more_info2):
                    if more_info2[phagename] == '0\n':
                        littlelist[0] += 1
                    elif more_info2[phagename] == '1\n':
                        littlelist[1] += 1
            biglist2.append(littlelist)
        return(biglist2)

def statstest(namecolumn, envcolumn, gencolumn):
    contingency = create_contingency(namecolumn, envcolumn, gencolumn)
    obs = np.array(contingency)
   # print(scipy.stats.chi2_contingency(obs))
    print("Below is the p-value:       (Look for under .05)")
    print(scipy.stats.chi2_contingency(obs)[1])
    print("Below is the test statistic:")
    print(scipy.stats.chi2_contingency(obs)[0])

