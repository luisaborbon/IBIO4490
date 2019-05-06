# Fully Convolutional Networks for Image Segmentation

In this report, J. Long's method [1] was implemented in order to understand how Fully Convolutional Networks can be used for semantic segmentation tasks. 

## Network Architecture

![](imgs/1.png)
![](imgs/2.png)

## Pascal VOC

![](https://www.researchgate.net/profile/Marco_San_Biagio/publication/271834295/figure/fig7/AS:613891893628956@1523374641887/Example-images-from-Pascal-VOC-2007-dataset.ppm)

## FCN on Pascal VOC

![](imgs/3.png)

__________________
# Results and Observations

1. Train 32s from vgg weights (finetuning).

![](imgs/32svgg.gif)
![](imgs/32vggi.jpg)

2. Train 32s from scratch (**No** finetuninng). 

![](imgs/32s.gif)


3. Train 16s from 32s weights.

![](imgs/16s32.gif)
![](imgs/1632i.jpg)

4. Train 16s from vgg weights.

![](imgs/16svgg.gif)
![](imgs/16vggi.jpg)

5. Train 16s from scratch.

![](imgs/16s.gif)

## References
[1] J. Long, E. Shelhamer, and T. Darrell.  Fully convolutional networks for semantic segmentation.  In Proceedings of the IEEE  conference  on  computer  vision  and  pattern  recognition, pages 3431–3440, 2015.
