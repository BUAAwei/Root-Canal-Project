import matplotlib.pyplot as plt
import os
from PIL import Image
from mpl_toolkits.mplot3d import Axes3D


def create_3d_model(points):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x_coords = [point[0] for point in points]
    y_coords = [point[1] for point in points]
    z_coords = [point[2] for point in points]
    for i in range(len(points) - 1):
        ax.plot([x_coords[i], x_coords[i+1]], [y_coords[i], y_coords[i+1]], [z_coords[i], z_coords[i+1]])
    ax.plot([x_coords[-1], x_coords[0]], [y_coords[-1], y_coords[0]], [z_coords[-1], z_coords[0]])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()


points = []
def process_image(image_path):
    image = Image.open(image_path)
    image = image.convert("1")
    width, height = image.size
    for y in range(height):
        for x in range(width):
            color = image.getpixel((x, y))
            if color == 255:
                points.append((x, y, int(os.path.splitext(os.path.basename(image_path))[0])))


folder_path = r".\data\masks"

for i in range(1, 199):
    file_path = os.path.join(folder_path, f"{i}.png")
    process_image(file_path)
create_3d_model(points)
