import math

import numpy as np

from .interpolation import interpolation

bi = interpolation()


class Geometric:
    def __init__(self):
        pass

    def forward_rotate(self, image, theta):
        """Computes the forward rotated image by and angle theta
                image: input image
                theta: angle to rotate the image by (in radians)
                return the rotated image"""
        maxX, maxY, minX, minY = self.maxyMini(theta, image)
        new_image_ = np.zeros((math.ceil(maxX - minX), math.ceil(maxY - minY)), dtype=int)
        rows = new_image_.shape[0]
        cols = new_image_.shape[1]
        for i in range(rows):
            for j in range(cols):
                x = int((i * math.cos(theta) - j * math.sin(theta)))
                y = int((i * math.sin(theta) + j * math.cos(theta)))
                if image.shape[0] > i >= 0 and image.shape[1] > j >= 0:
                    a = x - minX
                    b = y - minY
                    new_image_[int(a)][int(b)] = image[i][j]
        return new_image_

    def reverse_rotation(self, rotated_image, theta, origin, original_shape):
        """Computes the reverse rotated image by and angle theta
                rotated_image: the rotated image from previous step
                theta: angle to rotate the image by (in radians)
                Origin: origin of the original image with respect to the rotated image
                Original shape: Shape of the original image
                return the original image"""
        new_image = np.zeros((original_shape[0], original_shape[1]), dtype=int)
        for a in range(rotated_image.shape[0]):
            for b in range(rotated_image.shape[1]):
                a_ = a - origin[0]
                b_ = b - origin[1]
                a__ = int((a_ * math.cos(theta)) + (b_ * math.sin(theta)))
                b__ = int((-a_ * math.sin(theta)) + (b_ * math.cos(theta)))

                if new_image.shape[0] > a__ >= 0 and new_image.shape[1] > b__ >= 0:
                    new_image[a__][b__] = rotated_image[a][b]

        return new_image

    def rotate(self, image, theta, interpolation_type):
        """Computes the reverse rotated image by and angle theta
                image: the input image
                theta: angle to rotate the image by (in radians)
                interpolation_type: type of interpolation to use (nearest_neighbor, bilinear)
                return the original image"""
        maxX, maxY, minX, minY = self.maxyMini(theta, image)
        new_image = np.zeros((math.ceil(maxX - minX), math.ceil(maxY - minY)), dtype=int)
        origin = (-minX, -minY)
        rows = new_image.shape[0]
        cols = new_image.shape[1]
        for i in range(rows):
            i_ = i - origin[0]
            for j in range(cols):
                j_ = j - origin[1]
                i__ = math.ceil((i_ * math.cos(theta)) + (j_ * math.sin(theta)))
                j__ = math.ceil((j_ * math.cos(theta)) - (i_ * math.sin(theta)))
                if image.shape[0] > round(i__) >= 0 and image.shape[1] > round(j__) >= 0:
                    if interpolation_type == 'nearest_neighbor':
                        new_image[i][j] = image[round(i__)][round(j__)]
                    elif interpolation_type == 'bilinear':
                        i1 = math.floor(i__)
                        j1 = math.floor(j__)
                        i2 = i1 + 1
                        j2 = j1 + 1
                        a = round(i__)
                        b = round(j__)
                        c = image.shape[0]
                        d = image.shape[1]
                        if 0 <= a < image.shape[0] and 0 <= b < image.shape[1] and i1 < \
                                image.shape[0] and i2 < c and j1 < d and j2 < image.shape[1]:
                            new_image[i][j] = bi.bilinear_interpolation([i1, j1], [i1, j2], [i2, j1], [i2, j2],
                                                                        [i__, j__], image)
        return new_image

    def maxyMini(self, theta, image):
        minX, maxX = 0, 0
        minY, maxY = 0, 0
        for i in range(0, image.shape[0]):
            for j in range(0, image.shape[1]):
                x = i * math.cos(theta) - j * math.sin(theta)
                if x <= minX:
                    minX = x
                else:
                    minX = minX
                if x > maxX:
                    maxX = x
                else:
                    maxX = maxX
                y = i * math.sin(theta) + j * math.cos(theta)
                if y <= minY:
                    minY = y
                else:
                    minY = minY
                if y > maxY:
                    maxY = y
                else:
                    maxY = maxY
        return maxX, maxY, minX, minY
