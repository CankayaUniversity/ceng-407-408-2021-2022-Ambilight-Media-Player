import cv2
from sklearn.cluster import KMeans
import numpy as np
import yeelight
import time
from yeelight.main import Bulb
class FindDominantColors:
    MX=0
    def __init__(self, source_Image, source_clusters):
        self.clusters = source_clusters
        self.image = cv2.imread(source_Image)
        
    def cluster_percents(self,labels):
        total = len(labels)
        percents = []
        for i in set(labels):
            percent = (np.count_nonzero(labels == i) / total) * 100
            percents.append(round(percent, 2))
        return percents
    
    def dominantColors(self):
        sPercentValue = 10
        sWidth = int(self.image.shape[1] * sPercentValue / 100)
        sHeight = int(self.image.shape[0] * sPercentValue / 100)
        newSize = (sWidth, sHeight)
        resizedImage = cv2.resize(self.image, newSize)
        rgbImg = cv2.cvtColor(resizedImage, cv2.COLOR_BGR2RGB)
        rgbImg = rgbImg.reshape((rgbImg.shape[0] * rgbImg.shape[1], 3))
        self.image = rgbImg
        resultKmeans = KMeans(n_clusters=self.clusters)
        resultKmeans.fit(rgbImg)
        self.colors = resultKmeans.cluster_centers_
        self.labels = resultKmeans.labels_
        percents = self.cluster_percents(self.labels)
        s=0
        for i in percents:
            if i>percents[self.MX]:
                self.MX=s
            s=s+1
        return self.colors.astype(int)
    
bulb = Bulb('192.168.40.34', effect="smooth")
bulb.turn_on()
img = './images/1.png'
clusters = 5
dc = FindDominantColors(img, clusters) 
colors = dc.dominantColors()
bulb.set_rgb(int(colors[dc.MX][0]),int(colors[dc.MX][1]),int(colors[dc.MX][2]))
time.sleep(5)
img = './images/2.png'
clusters = 5
dc = FindDominantColors(img, clusters) 
colors = dc.dominantColors()
bulb.set_rgb(int(colors[dc.MX][0]),int(colors[dc.MX][1]),int(colors[dc.MX][2]))
time.sleep(5)
