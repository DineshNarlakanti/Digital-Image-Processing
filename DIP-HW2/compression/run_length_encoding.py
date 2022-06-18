import numpy as np


class Rle:
    def __init__(self):
        pass

    def encode_image(self, binary_image):
        """
        For efficiency, flatten the image by concatinating rows to create one long array, and
        compute run length encoding.
        Compress the image
        takes as input:
        image: binary_image
        returns run length code
        """
        rle_code = []
        count = 0
        p_v = binary_image[0][0]
        for x in range(0, binary_image.shape[0]):
            for y in range(0, binary_image.shape[1]):
                if p_v == binary_image[x][y]:
                    count = count + 1
                else:
                    if x == 0 and y == 0:
                        count = 1
                    rle_code.append([p_v, count])
                    p_v = binary_image[x][y]
                    count = 1
        rle_code.append([p_v, count])
        return rle_code  # replace zeros with rle_code

    def decode_image(self, rle_code, height, width):
        """
        Since the image was flattened during the encoding, use the hight and width to reconstruct the image
        Reconstructs original image from the rle_code
        takes as input:
        rle_code: the run length code to be decoded
        Height, width: height and width of the original image
        returns decoded binary image
        """
        decode_image = np.zeros((height, width), dtype="int")
        rows, cols = 0, 0
        for x in range(len(rle_code)):
            temp = rle_code[x]
            for y in range(temp[1]):
                if cols > width - 1:
                    cols = 0
                    rows = rows + 1
                decode_image[rows][cols] = temp[0]
                cols = cols + 1
        return decode_image  # replace zeros with image reconstructed from rle_Code












