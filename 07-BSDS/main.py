#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from Segment import segmentByClustering 
import numpy as np
import os
import cv2
import matplotlib.pyplot as plt
import scipy.io as sio


k=range(5,80,15)
names=os.listdir(path='BSR/BSDS500/data/images/test')
for name in names:
    
    img=cv2.imread(os.path.join("BSR/BSDS500/data/images/test/", name))
    name = name.split('.')[0]
    labgmm = np.zeros((len(k),), dtype = np.object)
    rgbgmm = np.zeros((len(k),), dtype = np.object)
 
    i=0
    for K in k:   
        seglab = segmentByClustering(rgbImage=img, colorSpace='lab+xy', clusteringMethod='kmeans', numberOfClusters=K)
        segrgb = segmentByClustering(rgbImage=img, colorSpace='rgb+xy', clusteringMethod='kmeans', numberOfClusters=K)  
        labgmm[i] = seglab
        rgbgmm[i] = segrgb
        i=i+1
        print(K , 'method=kmeans')
    
    if not os.path.exists('labkm'):
        os.mkdir('labkm')
    if not os.path.exists('rgbkm'):
        os.mkdir('rgbkm')

    labname='labkm'+'/'+name+'.mat'
    rgbname='rgbkm'+'/'+name+'.mat'
    sio.savemat(labname, {'segs':labgmm})
    sio.savemat(rgbname, {'segs':rgbgmm})
    print(name)

 
 
