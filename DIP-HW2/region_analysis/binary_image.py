import collections
import math
import sys


class BinaryImage:
    def __init__(self):
        pass

    def compute_histogram(self, image):
        """Computes the histogram of the input image
        takes as input:
        image: a grey scale image
        returns a histogram as a list"""
        hist = [0] * 256
        for x in range(image.shape[0]):
            for y in range(image.shape[1]):
                hist[image[x][y]] = hist[image[x][y]] + 1
        return hist

    def find_otsu_threshold(self, hist):
        """analyses a histogram to find the otsu's threshold assuming that the input histogram is bimodal.
        takes as input
        hist: a histogram
        returns: an optimal threshold value (otsu's threshold)"""

        threshold = 0
        o_w_v = sys.maxsize
        t_s = self.sum(hist)
        p = self.cp(hist, t_s)
        for x in range(len(hist)):
            w_v = int(self.cwv(p, x))
            if w_v < o_w_v:
                o_w_v = w_v
                threshold = x
        return threshold

    def cw(self, p, t):
        s1, s2 = 0, 0
        for x in range(len(p)):
            if x <= t:
                s1 = s1 + p.get(x)
            else:
                s2 = s2 + p.get(x)
        return s1, s2

    def cwv(self, p, t):
        a1, a2 = self.cw(p, t)
        b1, b2 = self.cm(p, t, a1, a2)
        c1, c2 = self.cv(p, t, a1, a2, b1, b2)
        sw = self.cws(a1, c1, a2, c2)
        return sw

    def cv(self, p, t, a1, a2, b1, b2):
        s1, s2 = 0, 0
        for x in range(len(p)):
            if x <= t:
                if a1 != 0:
                    s1 = s1 + ((((x - b1) ** 2) * p.get(x)) / a1)
            else:
                if a2 != 0:
                    s2 = s2 + ((((x - b2) ** 2) * p.get(x)) / a2)
        return int(s1), int(s2)

    def cws(self, a1, c1, a2, c2):
        return (a1 * c1) + (a2 * c2)

    def cm(self, p, t, a1, a2):
        s1, s2 = 0, 0
        for x in range(len(p)):
            if x <= t:
                if a1 != 0:
                    s1 = s1 + ((x * p.get(x)) / a1)
            else:
                if a2 != 0:
                    s2 = s2 + ((x * p.get(x)) / a2)
        return int(s1), int(s2)

    def binarize(self, image):
        """Comptues the binary image of the the input image based on histogram analysis and thresholding
        Make calls to the compute_histogram and find_otsu_threshold methods as needed.
        takes as input
        image: an grey scale image
        returns: a binary image"""

        b_i = image.copy()
        hist = self.compute_histogram(image)
        threshold = self.find_otsu_threshold(hist)
        for x in range(b_i.shape[0]):
            for y in range(b_i.shape[1]):
                b_i[x][y] = 255 if image[x][y] <= threshold else 0
        return b_i

    def sum(self, hist):
        t_s = 0;
        for x in range(len(hist)):
            t_s = t_s + hist[x]
        return t_s

    def cp(self, hist, t_s):
        d_p = {}
        for x in range(len(hist)):
            d_p[x] = hist[x]/t_s
        return d_p

