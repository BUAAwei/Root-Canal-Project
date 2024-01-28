import os
import cv2 as cv
import numpy as np
from numpy.core import integer, asarray, roll, zeros, swapaxes, take
from numpy.core.multiarray import normalize_axis_index
from numpy.fft import _pocketfft_internal as pfi


def imagefft2(a, s=None, axes=(-2, -1)):  # 图片二维傅里叶变换
    return raw_fftnd(a, s, axes, fft)


def imageifft2(a, s=None, axes=(-2, -1)):
    return raw_fftnd(a, s, axes, ifft)


def fft_shift(x, axes=None):  # 将图像低频部分转移到图像的中心
    x = asarray(x)
    if axes is None:
        axes = tuple(range(x.ndim))
        shift = [dim // 2 for dim in x.shape]
    elif isinstance(axes, integer):
        shift = x.shape[axes] // 2
    else:
        shift = [x.shape[ax] // 2 for ax in axes]
    return roll(x, shift, axes)


def ifft_shift(x, axes=None):  # 将图像低频部分移到原来位置
    x = asarray(x)
    if axes is None:
        axes = tuple(range(x.ndim))
        shift = [-(dim // 2) for dim in x.shape]
    elif isinstance(axes, integer):
        shift = -(x.shape[axes] // 2)
    else:
        shift = [-(x.shape[ax] // 2) for ax in axes]
    return roll(x, shift, axes)


def fft(a, n=None, axis=-1):  # 定义一维傅里叶变换函数
    a = asarray(a)
    if n is None:
        n = a.shape[axis]
    inv_norm = 1
    output = raw_fft(a, n, axis, False, True, inv_norm)
    return output


def ifft(a, n=None, axis=-1):
    a = asarray(a)
    if n is None:
        n = a.shape[axis]
    inv_norm = n
    output = raw_fft(a, n, axis, False, False, inv_norm)
    return output


def raw_fft(a, n, axis, is_real, is_forward, inv_norm):  # 为了变换结果，这里需要定义浮点数inv_norm
    axis = normalize_axis_index(axis, a.ndim)
    if n is None:
        n = a.shape[axis]

    fct = 1 / inv_norm

    if a.shape[axis] != n:
        s = list(a.shape)
        index = [slice(None)] * len(s)
        if s[axis] > n:
            index[axis] = slice(0, n)
            a = a[tuple(index)]
        else:
            index[axis] = slice(0, s[axis])
            s[axis] = n
            z = zeros(s, a.dtype.char)
            z[tuple(index)] = a
            a = z

    if axis == a.ndim - 1:
        r = pfi.execute(a, is_real, is_forward, fct)
    else:
        a = swapaxes(a, axis, -1)
        r = pfi.execute(a, is_real, is_forward, fct)
        r = swapaxes(r, axis, -1)
    return r


def cook_nd_args(a, s=None, axes=None, invreal=0):
    if s is None:
        shapeless = 1
        if axes is None:
            s = list(a.shape)
        else:
            s = take(a.shape, axes)
    else:
        shapeless = 0
    s = list(s)
    if axes is None:
        axes = list(range(-len(s), 0))
    if invreal and shapeless:
        s[-1] = (a.shape[axes[-1]] - 1) * 2
    return s, axes


def raw_fftnd(a, s=None, axes=None, function=fft):
    a = asarray(a)
    s, axes = cook_nd_args(a, s, axes)
    itl = list(range(len(axes)))
    itl.reverse()
    for ii in itl:
        a = function(a, n=s[ii], axis=axes[ii])
    return a


def low_pass_filter_image(input_path, output_path):
    for i in range(1, 199):
        file_path = os.path.join(input_path, f"{i}.png")
        img = cv.imread(file_path)
        original_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        # 傅里叶变换
        f = imagefft2(original_gray)
        fshift = fft_shift(f)
        r = 15
        # 低通蒙板
        rows, cols = fshift.shape
        mid_x, mid_y = int(rows / 2), int(cols / 2)
        mask = np.zeros((rows, cols), dtype=np.uint8)
        mask[mid_x - r:mid_x + r, mid_y - r:mid_y + r] = 1
        fshift2 = mask * fshift
        ishift = ifft_shift(fshift2)
        result = imageifft2(ishift)
        result = np.abs(result)
        output_file_path = os.path.join(output_path, f"{i}_low_pass_filter.png")
        cv.imwrite(output_file_path, result)


low_pass_filter_image(r".\data\imgs", r'.\data\filterWaved_img\img')
low_pass_filter_image(r".\data\masks", r'.\data\filterWaved_img\msk')
