import numpy as np
from skimage.io import imshow
from skimage import img_as_ubyte
from matplotlib import pyplot as plt
from random import uniform, choice
from maze_generation.perlin_to_color import make_polygon_colored


# gradient vectors for an of the main vectors
available_gradient_vectors = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0)
]


# generate gradient vectors
def gradient_vectors(arr):
    for i in range(arr.shape[0]):
        for j in range(arr.shape[0]):
            choice_sign = choice([-1, 1])
            x = uniform(-1, 1)
            # len should be equal 1
            y = (1 - pow(x, 2)) ** 0.5
            y = y * choice_sign
            arr[i, j, 0] = round(x, 3)
            arr[i, j, 1] = round(y, 2)
    return arr


# mark all gradient vectors
def advanced_gradient_vectors(arr):
    for i in range(arr.shape[0]):
        for j in range(arr.shape[0]):
            choice_vec = choice(available_gradient_vectors)
            arr[i, j, 0] = choice_vec[0]
            arr[i, j, 1] = choice_vec[1]
    return arr


# smoothing
def fade(t):
    return 6 * t ** 5 - 15 * t ** 4 + 10 * t ** 3


# perlin noise for current cell
def detour_of_cells(grid, grads):
    dim = grid.shape[0]
    for i in range(1, dim + 1):
        for j in range(1, dim + 1):
            dots = []
            inner_vectors = []
            cur_x = j / dim
            cur_y = i / dim
            inner_vectors.append(np.array([cur_x, cur_y]))
            inner_vectors.append(np.array([cur_x - 1, cur_y]))
            inner_vectors.append(np.array([cur_x, cur_y - 1]))
            inner_vectors.append(np.array([cur_x - 1, cur_y - 1]))
            # find scalar products of gradient vectors and inner vectors
            for k in range(4):
                dots.append(inner_vectors[k].dot(grads[k]))
            # first interpolation by x
            f_interpol = fade(cur_x) * (dots[1] - dots[0]) + dots[0]
            # second interpolation by x
            s_interpol = fade(cur_x) * (dots[3] - dots[2]) + dots[2]
            # bilinear interpolation
            bilinear_interpol = fade(cur_y) * (s_interpol - f_interpol) + f_interpol
            # enrolling of result to pixel
            grid[i - 1, j - 1] = (bilinear_interpol + 1) / 2
    return grid


def make_perlin_field(dim_fld=5, dim_cell=10):
    # make field
    field = np.zeros((dim_cell * dim_fld, dim_cell * dim_fld))
    # init the array for every integer point of plane
    init_gradient = np.zeros((dim_fld + 1, dim_fld + 1, 2))
    # gr_vecs = advanced_gradient_vectors(init_gradient)
    gr_vecs = gradient_vectors(init_gradient)

    # brute force of every cell
    for i in range(dim_fld):
        for j in range(dim_fld):
            cur_cell = field[i*dim_cell:i*dim_cell+dim_cell, j*dim_cell:j*dim_cell + dim_cell]
            # choose the key gradient vectors for current cell
            cur_vectors = [gr_vecs[i, j], gr_vecs[i, j + 1], gr_vecs[i + 1, j], gr_vecs[i + 1, j + 1]]
            # detour of black-white grid to cell by perlin algorithm
            colored_cell = detour_of_cells(cur_cell, cur_vectors)
            # appointing colored cell to current cell
            field[i*dim_cell:i*dim_cell+dim_cell, j*dim_cell:j*dim_cell + dim_cell] = colored_cell

    return img_as_ubyte(field)


if __name__ == "__main__":
    # make black-white perlin
    polygon = make_perlin_field()
    # make map by perlin field
    result_image = make_polygon_colored(polygon)

    # echo
    imshow(result_image)
    plt.show()



