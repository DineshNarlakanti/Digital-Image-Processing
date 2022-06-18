class interpolation:

    def linear_interpolation(self, x1, x2, x, pt1, pt21, image):
        """Computes the linear interpolation at location pti using pt1 and pt2 as input.
        1. Please change the function definition to add the the required arguments as needed.
        2. This function performs linear interpolation between two one dimensional points and returns the interpolated value.
        This function will require the following values
        pt1: Location of point pt1 (z1)
        I1: Intensity at the location pt1
        pt2: Location of point pt2 (z2)
        I2: Intensity at the location pt2
        pti: Location at which to determine the interpolated value (z)
        return Ii or interpolated intensity at location pti"""

        # Write your code for linear interpolation here
        a = x2 - x
        b = x2 - x1
        c = x - x1
        intensity = (((a) / (b) * image[pt1[0]][pt1[1]]) + ((c) / (b)) * image[pt21[0]][pt21[1]])
        return intensity

    def bilinear_interpolation(self, pt1, pt12, pt21, pt2, original, image):
        """Computes the bilinear interpolation at location pti using pt1, pt2, pt3, and pt4 as input
        1. Please change the function definition to add the the required arguments as needed.
        2. This function performs bilinear interpolation between four two dimensional points and returns the interpolated value.
        3. This is accomplished by performing linear interpolation three times. Reuse or call linear interpolation method above to compute this task.
        This function will require the following values
        pt1: Location of the point pt1 (x1, y1)
        I1: Intensity at location pt1
        pt2: Location of the point pt2 (x2, y2)
        I2: Intensity at location pt2
        pt3: Location of the point pt3 (x3, y3)
        I3: Intensity at location pt3
        pt4: Location of the point pt4 (x4, y4)
        I4: Intensity at location pt4
        pti: Location at which to determine the interploated value (x, y)
        return Ii or interpolated intensity at location pti"""

        # Write your code for bilinear interpolation here
        I1_ = self.linear_interpolation(pt1[0], pt21[0], original[0], pt1, pt21, image)
        I2_ = self.linear_interpolation(pt12[0], pt2[0], original[0], pt12, pt2, image)
        I3_ = ((((pt12[1] - original[1]) / (pt12[1] - pt21[1])) * I1_) + (
                    (original[1] - pt21[1]) / (pt12[1] - pt1[1]) * I2_))
        return I3_