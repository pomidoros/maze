import numpy as np

# colors for map
rgb = [
    # first - dark-brown
    [41, 23, 4],
    [66, 36, 1],
    [89, 49, 3],
    [150, 57, 3],
    [171, 65, 3],
    [171, 104, 3],
    [199, 124, 12],
    [227, 142, 14],
    [242, 203, 7],
    [252, 215, 28],
    [255, 223, 61],
    [118, 161, 0],
    [140, 189, 6],
    [177, 240, 5],
    [188, 255, 5],
    [0, 250, 233],
    [2, 245, 229],
    [2, 224, 210],
    [89, 216, 255],
    [35, 200, 250],
    [2, 190, 247],
    [2, 161, 209],
    [2, 149, 194],
    [5, 118, 153],
    [6, 107, 138],
    # last - dark blue
    [3, 81, 105]
]


# convert black-white format to colored format
def make_polygon_colored(field):
    # calibration array
    make_points = np.linspace(20, 230, num=len(rgb))
    # init output image
    image = np.zeros(field.shape[0] * field.shape[1] * 3)
    # convert image to RGB standard
    image = image.reshape(field.shape[0], field.shape[1], 3)
    for i in range(field.shape[0]):
        for j in range(field.shape[1]):
            # round the perlin value to the nearest point of calibration array and find needed index
            idx = np.searchsorted(make_points, field[i, j])
            # make RGB
            image[i, j, 0] = rgb[idx][0]
            image[i, j, 1] = rgb[idx][1]
            image[i, j, 2] = rgb[idx][2]
    return image.astype("uint8")

