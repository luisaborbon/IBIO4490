#!/usr/bin/python2

#Import the modules
import numpy as np
import time
import os, random
import subprocess
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont

#Makes sure the following modules are installed
try:
    import zipfile
except ImportError:
    subprocess.call(['pip','install','zipfile'])
    import zipfile

try:
    import shutil
except ImportError:
    subprocess.call(['pip','install','shutil'])
    import shutil

try:    
    import urllib
except ImportError:
    subprocess.call(['pip','install','urllib'])
    import urllib
    
# Start measuring time [1]
start = time.time()

# Download the database [2]
url = 'https://www.dropbox.com/s/ldhzb3o9qai14m1/catdog.zip?dl=1'
u = urllib.urlopen(url)
data = u.read()
u.close()
with open(os.getcwd() + '/' + 'catdog.zip', "wb") as f :
    f.write(data)
f.close()

#[3] Unzip the database
zip_ref = zipfile.ZipFile(os.getcwd() + '/' + 'catdog.zip', 'r')
zip_ref.extractall(os.getcwd())
zip_ref.close()

#Choose a random even number between 6 and 20
N = np.random.randint(6,20)
if N%2 != 0:
    N=N-1

#Verify if the Resized images folder exists
if os.path.exists(os.getcwd()+ '/' + 'catdog' + '/' + 'catdogResize') == False:
     os.mkdir(os.getcwd() + '/' + 'catdog' + '/' + 'catdogResize')

plt.figure(1)
for i in range(0,N):
     #Choose a random image from the folder and resize it
     imgName = random.choice(os.listdir(os.getcwd() + '/' + 'catdog')) 
     img = Image.open(os.getcwd() + '/' + 'catdog'+ '/' + imgName)
     imgResize = img.resize((256,256))
     
     #Draw the labels on the images and save them in a different folder
     draw = ImageDraw.Draw(imgResize)
     font = ImageFont.truetype('Lato-Medium.ttf', 50)
     imgLabel = draw.text((100,80),imgName[0:3] ,font=font, fill='white')
     imgResize.save(os.getcwd() +'/' + 'catdog' + '/' + 'catdogResize' + '/' + imgName)
        
     #Plot the images in subplots
     plt.subplot(2,N/2,i+1) 
     plt.axis('off')
     plt.imshow(imgResize)
     plt.subplots_adjust(wspace=0, hspace=0) #Less Space between images [5]
plt.show()

#[6] Delete the folder created with the resized images
shutil.rmtree(os.getcwd()+ '/' + 'catdog' + '/' + 'catdogResize')

#Show the processing time
end = time.time()
print('The processing time was: ' + str(end -start) + 'seconds')

#References:
#[1] https://pythonhow.com/measure-execution-time-python-code/
#[2] http://www.xavierdupre.fr/blog/2015-01-20_nojs.html
#[3] https://stackoverflow.com/questions/3451111/unzipping-files-in-python
#[4] https://recursospython.com/guias-y-manuales/anadir-texto-imagen-pillow/
#[5] https://matplotlib.org/2.1.1/gallery/subplots_axes_and_figures/ganged_plots.html
#[6] https://stackoverflow.com/questions/303200/how-do-i-remove-delete-a-folder-that-is-not-empty-with-python
