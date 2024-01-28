import os
import cv2 as cv


def gauss_filter_image(input_path, output_path):
    for i in range(1, 199):
        file_path = os.path.join(input_path, f"{i}.png")
        img = cv.imread(file_path)
        source = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        result = cv.GaussianBlur(source, (3, 3), 0)
        output_file_path = os.path.join(output_path, f"{i}_Gauss_filter.png")
        cv.imwrite(output_file_path, result)


gauss_filter_image(r".\data\imgs", r'.\data\filterWaved_img\img')
gauss_filter_image(r".\data\masks", r'.\data\filterWaved_img\msk')
