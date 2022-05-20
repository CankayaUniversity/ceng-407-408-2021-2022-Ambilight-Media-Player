#This class finds the dominant color in the specified number of clusters in the picture sent as a parameter.
import cv2
from sklearn.cluster import KMeans
class FindDominantColors:
    def __init__(self, source_Image, source_clusters):
        self.clusters = source_clusters
        self.image = source_Image
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
        return self.colors.astype(int)

