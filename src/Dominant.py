#This class finds the dominant color in the specified number of clusters in the picture sent as a parameter.
#Source: https://scikit-learn.org/stable/auto_examples/index.html
import cv2
from sklearn.cluster import KMeans
import warnings
from sklearn.exceptions import ConvergenceWarning
import numpy as np
class FindDominantColors:
    MAXINDEX = -1
    BRIGHTNESS=100
    def __init__(self, source_Image, source_clusters):
        warnings.filterwarnings('ignore', category=ConvergenceWarning) #ConvergenceWarnings are disabled
        self.clusters = source_clusters
        self.image = source_Image
    @staticmethod
    def findPercents(labels):
        total = len(labels)
        percents = []
        for i in set(labels):
            percent = (np.count_nonzero(labels == i) / total) * 100
            percents.append(round(percent, 2))
        return percents
    @staticmethod
    def findBrightness(cColors):
        maxColor=cColors[0]
        for c in cColors:
            if c>maxColor:
                maxColor=c
        if maxColor/255*100<35:
            return False
        else:
            BRIGHTNESS=int(maxColor/255*100)
            return True
        
    def dominantColors(self):
        sPercentValue = 1
        sWidth = int(self.image.shape[1] * sPercentValue / 100)
        sHeight = int(self.image.shape[0] * sPercentValue / 100)
        newSize = (sWidth, sHeight)
        resizedImage = cv2.resize(self.image, newSize)
        rgbImg = cv2.cvtColor(resizedImage, cv2.COLOR_BGR2RGB)
        rgbImg = rgbImg.reshape((rgbImg.shape[0] * rgbImg.shape[1], 3))
        self.image = rgbImg
        resultKmeans = KMeans(n_clusters=self.clusters)
        resultKmeans.fit(rgbImg)
        Colors = resultKmeans.cluster_centers_
        Labels = resultKmeans.labels_
        Percents = self.findPercents(Labels)
        s = 0
        tx=0
        for p in Percents:
            if p >= Percents[tx] and self.findBrightness(Colors[s]):
                self.MAXINDEX = s
                tx=s
            elif p < Percents[tx] and self.findBrightness(Colors[s]) and self.MAXINDEX<0:
                self.MAXINDEX = s
                tx=s
            s = s + 1
        return Colors.astype(int)

