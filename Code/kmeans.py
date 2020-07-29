#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 13:34:18 2018

@author: ethanmoyer
"""

from sklearn.cluster import KMeans
import numpy as np
import scipy.stats


def cluster(numcluster, namecolumn, gencolumn):    
    with open('W:/MoreInfoTest.csv', 'r') as text:
        AverageTempArray = []
        NameArray=[]
        for row in text:
            newrow=row.split(",")
            if newrow[gencolumn] != "*":
                AverageTempArray.append(newrow[gencolumn])
                NameArray.append(newrow[namecolumn])
    del AverageTempArray[0]
    del NameArray[0]
    AveTempArray=[]
    for item in range(0,len(AverageTempArray)):
        number=float(AverageTempArray[item])
        AveTempArray.append([number])
    X = np.array(AveTempArray)
    kmeans = KMeans(n_clusters=numcluster, random_state=0).fit(X)
    clusters=list(kmeans.labels_)
    clusternumbers=[]
    for num in range(0,numcluster):
        clusternumbers.append(clusters.count(num))
    PhageClusters={}
    for d in range(len(clusters)):
        if clusters[d] in PhageClusters.keys():
            PhageClusters[clusters[d]].append(NameArray[d])
        else:
            PhageClusters[clusters[d]]=[NameArray[d]]
    return(PhageClusters)



def specialcluster(numcluster, namecolumn, gencolumn):
    with open('W:/MoreInfoTest.csv', 'r') as text:
        AverageTempArray = []
        NameArray=[]
        for row in text:
            newrow=row.split(",")
            if newrow[gencolumn] != "*":
                AverageTempArray.append(newrow[gencolumn])
                NameArray.append(newrow[namecolumn])
    del AverageTempArray[namecolumn]
    del NameArray[namecolumn]
    AveTempArray=[]
    for item in range(0,len(AverageTempArray)):
        number=float(AverageTempArray[item])
        AveTempArray.append([number])
    X = np.array(AveTempArray)
    kmeans = KMeans(n_clusters=numcluster, random_state=0).fit(X)
    clusters=list(kmeans.labels_)
    clusternumbers=[]
    for num in range(0,numcluster):
        clusternumbers.append(clusters.count(num))
    PhageClusters={}
    for d in range(len(clusters)):
        if clusters[d] in PhageClusters.keys():
            PhageClusters[clusters[d]].append(NameArray[d])
        else:
            PhageClusters[clusters[d]]=[NameArray[d]]
    newdict = {}
    for genetic_label in PhageClusters.keys():
        for name in PhageClusters[genetic_label]:
            newdict[name] = genetic_label
    return(newdict)



def create_contingency(numcluster1, namecolumn, envcolumn, numcluster2, gencolumn):
    envcluster = cluster(numcluster1, namecolumn, envcolumn)
    if(gencolumn == 9): 
        gencluster = specialcluster(numcluster2, namecolumn, gencolumn)
    #    print(gencluster)
        biglist = []
        for env_key in envcluster.keys():
            littlelist = []
            for q in range(0, numcluster2):
                littlelist.append(0)
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
        with open('W:/MoreInfoTest.csv', 'r') as text: 
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

def better_contingency(numcluster1, namecolumn, envcolumn, numcluster2, gencolumn):
    start_table = create_contingency(numcluster1, namecolumn, envcolumn, numcluster2, gencolumn)
    end_table = []
    for envcluster in start_table:
        count = 0
        for cell in envcluster:
            count = count + cell
        if count >= 30:
            end_table.append(envcluster)
    return end_table
        

def statstest(numcluster1, namecolumn, envcolumn, numcluster2, gencolumn):
    contingency = better_contingency(numcluster1, namecolumn, envcolumn, numcluster2, gencolumn)
    obs = np.array(contingency)
    return(scipy.stats.chi2_contingency(obs)[1])

def significance(namecolumn, envcolumn, gencolumn):
    for i in range(2, 7):
        for j in range(2, 7):
            result = statstest(i, namecolumn, envcolumn, j, gencolumn)
            if result <= 0.05:
                print ("Significant", result, (i, j))
