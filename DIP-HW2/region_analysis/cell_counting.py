import numpy as np
import cv2

class CellCounting:
    def _init_(self):
        pass

    def blob_coloring(self, image):
        """Uses the blob coloring algorithm based on 5 pixel cross window and assigns region names
        takes a input:
        image: binary image
        return: a list/dict of regions"""

        regions = dict()
        region_image = np.array(np.zeros((image.shape[0], image.shape[1])))

        for x in range(-1, 0):
            for y in range(0, image.shape[1]):
                image[x, y] = 0

        for x in range(0, image.shape[0]):
            for y in range(-1, 0):
                image[x, y] = 0

        w = 1
        t = 0
        for x in range(0, image.shape[0]):
            for y in range(0, image.shape[1]):
                if image[x, y] == 255 and image[x, y - 1] == 0 and image[x - 1, y] == 0:
                    region_image[x, y] = w
                    w = w + 1

                if image[x, y] == 255 and image[x, y - 1] == 0 and image[x - 1, y] == 255:
                    region_image[x, y] = region_image[x - 1, y]
                if image[x, y] == 255 and image[x, y - 1] == 255 and image[x - 1, y] == 0:
                    region_image[x, y] = region_image[x, y - 1]
                if image[x, y] == 255 and image[x, y - 1] == 255 and image[x - 1, y] == 255:
                    region_image[x, y] = region_image[x - 1, y]
                    if region_image[x, y - 1] != region_image[x - 1, y]:
                        p = 1
                        while image[x, y - p] == 255:
                            region_image[x, y - p] = region_image[x - 1, y]
                            p = p + 1
                            h = 1
                            while region_image[x - h, y - p] != 0 and region_image[x, y - p] != 0:
                                region_image[x - h, y - p] = region_image[x - 1, y]
                                t = t + 1
                                h = h + 1

        for x in range(0, image.shape[0]):
            for y in range(0, image.shape[1]):
                regions.setdefault(region_image[x, y], []).append([x, y])

        return regions


    def compute_statistics(self, region):
        """Computes cell statistics area and location
        takes as input
        region: list regions and corresponding pixels
        returns: stats"""

        # Please print your region statistics to stdout
        # <region number>: <location or center>, <area>
        # print(stats)
        stats = dict()

        m = 0
        for key in region.keys():
            values = region[key]
            if len(values) < 15:
                continue
            v = 0
            z = 0
            for value in values:
                v = v + value[0]
                z = z + value[1]
            v = v / len(values)
            z = z / len(values)
            if key != 0:
                stats.setdefault(m, []).append([int(v), int(z), len(values)])
                print("Region:", m, "Area:", len(values), "Centroid:", "(%s, %s)" % (int(v), int(z)))
            m += 1

        return stats

    def mark_image_regions(self, image, stats):
        """Creates a new image with computed stats
        Make a copy of the image on which you can write text.
        takes as input
        image: Input binary image
        stats: stats regarding location and area
        returns: image marked with center and area"""
        mi = image.copy()
        mi = cv2.cvtColor(mi, cv2.COLOR_GRAY2BGR)
        for lock in stats.keys():
            if lock != 0:
                mi = cv2.putText(mi, "*",
                                           tuple([stats[lock][0][1] - 1, stats[lock][0][0] - 1]),
                                           cv2.FONT_HERSHEY_SIMPLEX, 0.25, (0, 0, 255), 1, cv2.LINE_AA)
                mi = cv2.putText(mi, str(lock) + "," + str(stats[lock][0][2]),
                                           tuple([stats[lock][0][1], stats[lock][0][0]]),
                                           cv2.FONT_HERSHEY_SIMPLEX, 0.27, (0, 0, 0), 1, cv2.LINE_AA)

        return mi   