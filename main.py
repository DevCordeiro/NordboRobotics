"""
Project: Nordbo Robotics. Get the image, crop, rotate and resize
Author: Anderson Cordeiro de Souza
Date: 01/10/2024
"""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def crop_image(image_to_crop, x, y, width, height):
    matrix_image = np.array(image_to_crop)
    cropped_matrix = matrix_image[y:height, x:width]
    new_image = Image.fromarray(np.uint8(cropped_matrix))

    fig, axs = plt.subplots(1, 2)
    axs[0].imshow(image)
    axs[0].axis('off')
    axs[1].imshow(new_image)
    axs[1].axis('off')

    fig.suptitle('Cropped Image')
    plt.show()


if __name__ == '__main__':
    operational_system = sys.platform                            # verify the operational system
    folder_code = os.path.dirname(os.path.abspath(__file__))     # Get path to script folder
    images_folder = os.path.join(folder_code, 'Images')           # Create a path to Images folder

    # if operationalSystem == 'win32':                            # Verify if is Windows
    #     imagesFolder = imagesFolder.replace('/', '\\')

    folder_files_name = os.listdir(images_folder)
    for file in folder_files_name:
        print(file)

    name_image_user = input("Type an Image name, example (Image01.jpeg): ")
    print("You write: ", name_image_user)

    image = Image.open(os.path.join(images_folder, name_image_user))

    commandChoose = input("Type a command: ")

    if commandChoose.upper() == "CROP":
        coordinates = input("Type de coordinates >> x,y: ")
        coordinatesArray = coordinates.split(',')

        newSize = input("Type de width and eight >> width,height: ")
        newSizeArray = newSize.split(',')

        crop_image(image, int(coordinatesArray[0]), int(coordinatesArray[1]), int(newSizeArray[0]), int(newSizeArray[1]))
