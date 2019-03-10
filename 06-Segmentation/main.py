#!/home/lfborbon/anaconda3/bin/python

def imshow(img, seg, title='Image'):
    import matplotlib.pyplot as plt
    plt.imshow(img, cmap=plt.get_cmap('gray'))
    plt.imshow(seg, cmap=plt.get_cmap('rainbow'), alpha=0.5)
    cb = plt.colorbar()
    cb.set_ticks(range(seg.max()+1))
    plt.title(title)
    plt.axis('off')
    plt.show()

def groundtruth(img_file):
    import scipy.io as sio
    img = imageio.imread(img_file)
    gt=sio.loadmat(img_file.replace('jpg', 'mat'))
    segm=gt['groundTruth'][0,3][0][0]['Segmentation']
    imshow(img, segm, title='Groundtruth')
    return(segm)

def check_dataset(folder):
    import os
    if not os.path.isdir(folder):
        os.system('wget http://157.253.196.67/BSDS_small.zip')
        os.system('unzip BSDS_small.zip')
        
            
def eval_metric(seg, annot):
    import numpy as np
    anmax = np.max(annot)
    segmax = np.max(seg)
    a = 1
    resultannot=[]
    resultseg=[]
    for i in range(0,annot.shape[0]):
        for j in range(0,annot.shape[1]):
            if a>anmax:
                break
            elif annot[i,j]==a:
                b = seg[i,j]
                resultannot.append(np.sum(seg==b)/np.sum(annot==a))
                a=a+1
                break
    
    a = 0
    for i in range(0,seg.shape[0]):
        for j in range(0,seg.shape[1]):
            if a>segmax:
                break
            elif annot[i,j]==a:
                b = seg[i,j]
                resultseg.append(np.sum(annot==b)/np.sum(seg=a))
                a=a+1
                break
    
    tam=annot.shape[0]*annot.shape[1]
    val= (sum(resultannot)/tam) + (sum(resultseg)/tam)
    val=val/2
    
    return(val)

if __name__ == '__main__':
    import argparse
    import imageio
    from Segment import segmentByClustering 
    parser = argparse.ArgumentParser()

    parser.add_argument('--color', type=str, default='rgb', choices=['rgb', 'lab', 'hsv', 'rgb+xy', 'lab+xy', 'hsv+xy']) 
    parser.add_argument('--k', type=int, default=4)
    parser.add_argument('--method', type=str, default='watershed', choices=['kmeans', 'gmm', 'hierarchical', 'watershed'])
    parser.add_argument('--img_file', type=str, required=True)

    opts = parser.parse_args()

    check_dataset(opts.img_file.split('/')[0])

    img = imageio.imread(opts.img_file)
    seg = segmentByClustering(rgbImage=img, colorSpace=opts.color, clusteringMethod=opts.method, numberOfClusters=opts.k)
    imshow(img, seg, title='Prediction')
    annot = groundtruth(opts.img_file)
    val=eval_metric(seg,annot)
    print(str(val))

    #import matplotlib.pyplot as plt
    #plt.figure()
    #plt.subplot(1,2,1)
    #plt.imshow(seg)
    #plt.axis('off')
    #plt.subplot(1,2,2)
    #plt.imshow(annot)
    #plt.axis('off')
    #plt.subplots_adjust(wspace=0, hspace=0)
    

