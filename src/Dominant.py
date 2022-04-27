import time
import colorsys
from PIL import Image

import numpy as np
import numpy
import math
import cv2

from sklearn.cluster import KMeans
from collections import Counter
import wcag_contrast_ratio as contrast

class DominantColors:
    CLUSTERS = None
    IMAGE = None
    COLORS = None
    LABELS = None
    def __init__(self, image, clusters=3):
        self.CLUSTERS = clusters
        self.IMAGE = image
    def dominantColors(self):
        # read image
        img_src = self.IMAGE  
        # percent by which the image is resized
        scale_percent = 10
        # calculate the 50 percent of original dimensions
        width = int(img_src.shape[1] * scale_percent / 100)
        height = int(img_src.shape[0] * scale_percent / 100)
        # dsize
        dsize = (width, height)
        # resize image
        small_img = cv2.resize(img_src, dsize)
        # convert to rgb from bgr
        img = cv2.cvtColor(small_img, cv2.COLOR_BGR2RGB)
        # reshaping to a list of pixels
        img = img.reshape((img.shape[0] * img.shape[1], 3))
        # save image after operations
        self.IMAGE = img
        # using k-means to cluster pixels
        kmeans = KMeans(n_clusters=self.CLUSTERS)
        kmeans.fit(img)
        # the cluster centers are our dominant colors.
        self.COLORS = kmeans.cluster_centers_
        # save labels
        self.LABELS = kmeans.labels_
        # returning after converting to integer from float
        return self.COLORS.astype(int)

