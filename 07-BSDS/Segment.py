#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def segmentByClustering( rgbImage, colorSpace, clusteringMethod, numberOfClusters):
    # Parameters
    # colorSpace : 'rgb', 'lab', 'hsv', 'rgb+xy', 'lab+xy' or 'hsv+xy'
    # clusteringMethod = 'kmeans', 'gmm', 'hierarchical' or 'watershed'.
    # numberOfClusters positive integer (larger than 2)
    
    
    # Normalizes de image
    def debugImg(rawData):
        import cv2
        import numpy as np
        #import matplotlib.pyplot as plt
        toShow = np.zeros((rawData.shape), dtype=np.uint8)
        cv2.normalize(rawData, toShow, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        #plt.imshow(toShow)
        #plt.show()
        return(toShow)
    
    
    # Color Space Configuration
    # Import modules
    from skimage import io, color
    import numpy as np
    
    # Read the image
    img = rgbImage
    
    # Create the normalized x, y channels
    h = np.indices((img.shape[0],img.shape[1]))
    y = np.uint8((h[0,:,:]/(img.shape[0]-1))*255)
    x = np.uint8((h[1,:,:]/(img.shape[1]-1))*255)
            
    # Change the image into the specified colorSpace
    if colorSpace == 'rgb+xy':
        img = np.dstack((img,x,y))
    
    elif colorSpace == 'lab' or colorSpace=='lab+xy':
        img = color.rgb2lab(img)
        img = debugImg(img)
        if colorSpace=='lab+xy':
            img = np.dstack((img,x,y))
                
    elif colorSpace == 'hsv' or colorSpace=='hsv+xy':
        img = color.rgb2hsv(img)
        img = debugImg(img)
        if colorSpace == 'hsv+xy':
            img = np.dstack((img,x,y))


    #Clustering methods
    y,x,chan = img.shape
    vect = img.reshape(x*y,chan)
    
    import numpy as np
    if clusteringMethod=='hierarchical':
        import cv2
        img = cv2.resize(img, (281,121))
        yh,xh,chanh = img.shape
        vecth = img.reshape(xh*yh,chanh)
    
    if clusteringMethod=='kmeans':
        from sklearn.cluster import KMeans
        kmeans = KMeans(n_clusters=numberOfClusters).fit_predict(vect)
        segmentation = np.reshape(kmeans,(y,x))
    
    elif clusteringMethod == 'gmm':
        from sklearn import mixture
        gmm = mixture.GaussianMixture(n_components=numberOfClusters).fit_predict(vect)
        segmentation = np.reshape(gmm,(y,x))

    elif clusteringMethod == 'hierarchical':
        import scipy
        from sklearn.cluster import AgglomerativeClustering
        clustering = AgglomerativeClustering(n_clusters=numberOfClusters).fit_predict(vecth)
        segmentation = np.reshape(clustering,(yh,xh))
        segmentation = np.uint8(segmentation)
        segmentation = scipy.misc.imresize(segmentation,(y,x),interp='nearest', mode=None)
       
        
        # The idea to implement the watershed algorithm segmentation was taken
        # from [1]
    elif clusteringMethod == 'watershed':
        import numpy as np
        from scipy import ndimage as ndi
        from skimage.morphology import watershed
        from skimage.feature import peak_local_max
        img=np.mean(img,axis=2)
        img1=img*-1 #local MINS
        local_max = peak_local_max(img1, indices=False,num_peaks=numberOfClusters,num_peaks_per_label=1)
        markers=ndi.label(local_max)[0]
        segmentation=watershed(img,markers)
        
    return segmentation


# References 
# [1] http://scikit-image.org/docs/dev/auto_examples/segmentation/plot_watershed.html