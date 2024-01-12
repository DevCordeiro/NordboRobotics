"""
Project: Nordbo Robotics. Get the image, crop, rotate and resize
Author: Anderson Cordeiro de Souza
Date: 01/12/2024
"""
import math
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def crop_image(image_to_crop, x, y, width, height):
    image_matrix = np.array(image_to_crop)
    if x >= 0 and y >= 0 and width >= 0 and height >= 0:
        if x + width <= image_matrix.shape[1] and y + height <= image_matrix.shape[0]:
            cropped_matrix = image_matrix[y:y+height, x:x+width]
            new_image = Image.fromarray(np.uint8(cropped_matrix))

            plot_image(image_to_crop, new_image, "Cropped")

        else:
            print("Cropping dimensions outside the image boundaries.")
    else:
        print("Invalid cropping dimensions.")


def rotation_image(image_to_rotate, degree):
    rads = math.radians(degree)
    image_matrix = np.array(image_to_rotate)
    height_image, width_image, layer_image = image_matrix.shape

    height_rot_img = round(abs(height_image*math.sin(rads))) + round(abs(width_image*math.cos(rads)))
    width_rot_img = round(abs(width_image*math.cos(rads))) + round(abs(height_image*math.sin(rads)))

    new_image_matrix = np.uint8(np.zeros((height_rot_img, width_rot_img, layer_image)))

    center_y = int(height_image/2)
    center_x = int(width_image/2)

    mid_rot_y, mid_rot_x = (height_rot_img/2, width_rot_img/2)

    print("center y: ", center_y)
    print("center x: ", center_x)

    for y in range(height_rot_img):
        for x in range(width_rot_img):
            new_x = int((math.cos(rads) * (x - mid_rot_x)) - (math.sin(rads) * (y - mid_rot_y)) + center_x)
            new_y = int((math.sin(rads) * (x - mid_rot_x)) + (math.cos(rads) * (y - mid_rot_y)) + center_y)

            if 0 <= new_y < height_image and 0 <= new_x < width_image:
                new_image_matrix[y, x, :] = image_matrix[new_y, new_x, :]

    new_image = Image.fromarray(new_image_matrix)

    plot_image(image_to_rotate, new_image, "Rotated")


def plot_image(original_image_to_plot, image_to_plot, title_reference):

    fig, axs = plt.subplots(1, 2)
    axs[0].imshow(original_image_to_plot)
    axs[0].set_title('Original Image')
    axs[0].axis('on')
    axs[0].set_xticks([]), axs[0].set_yticks([])

    axs[1].imshow(image_to_plot)
    axs[1].set_title(title_reference + ' Image')
    axs[1].axis('on')
    axs[1].set_xticks([]), axs[1].set_yticks([])

    for ax in axs:
        ax.spines['top'].set_linewidth(2)
        ax.spines['bottom'].set_linewidth(2)
        ax.spines['left'].set_linewidth(2)
        ax.spines['right'].set_linewidth(2)

    fig.suptitle(title_reference + ' Image')
    plt.show()


if __name__ == '__main__':
    folder_code = os.path.dirname(os.path.abspath(__file__))     # Get path to script folder
    images_folder = os.path.join(folder_code, 'Images')           # Create a path to Images folder

    folder_files_name = os.listdir(images_folder)
    for file in folder_files_name:
        print(file)

    name_image_user = input("Type an Image name, example (Image01.jpeg): ")
    print("You write: ", name_image_user)

    image = Image.open(os.path.join(images_folder, name_image_user))
    print("Dimensions of Image: ", image.size)

    commandChoose = input("Type a command: ")

    if commandChoose.upper() == "CROP":
        coordinates = input("Type the coordinates >> x,y: ")
        coordinatesArray = coordinates.split(',')

        newSize = input("Type the width and height >> width,height: ")
        newSizeArray = newSize.split(',')

        crop_image(image, int(coordinatesArray[0]), int(coordinatesArray[1]), int(newSizeArray[0]), int(newSizeArray[1]))

    if (commandChoose.upper()) == "ROTATE":
        user_angle = input("Type a angle for rotation: ")
        rotation_image(image, int(user_angle))
