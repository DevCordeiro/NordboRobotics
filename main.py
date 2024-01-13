"""
Project: Nordbo Robotics. Get the image, crop, rotate and resize
Author: Anderson Cordeiro de Souza
Date: 01/12/2024
"""
import argparse
import math
import matplotlib.pyplot as plt
import numpy as np
import os

from PIL import Image


def main():
    parser = argparse.ArgumentParser(description='Script to manipulation of Images.')
    parser.add_argument('--image', type=str, help='Image name')
    parser.add_argument('--resize', nargs=2, type=int, metavar=('width', 'height'), help='Resize the image')
    parser.add_argument('--crop', nargs=4, type=int, metavar=('x', 'y', 'width', 'height'), help='crop the image')
    parser.add_argument('--rotate', type=float, help='Rotate the image for Angle in degree')

    args = parser.parse_args()

    if (args.image is not None) and (args.resize is not None) and (args.crop is not None) and (args.rotate is not None):
        manipulate_image_args(args.image, args.resize, args.crop, args.rotate)
    else:
        run_friendly_user_interface()


def manipulate_image_args(image_name_args, resize_args, crop_args, rotate_args):
    images_folder = search_images_name()
    clear_display()
    image = Image.open(os.path.join(images_folder, image_name_args))
    image_resize_to_plot = resize_image(image, resize_args[0], resize_args[1])
    image_crop_to_plot = crop_image(image, crop_args[0], crop_args[1], crop_args[2], crop_args[3])
    image_rotate_to_plot = rotation_image(image, rotate_args)
    plot_all_images(image, image_crop_to_plot, image_rotate_to_plot, image_resize_to_plot)


def run_friendly_user_interface():
    while True:
        clear_display()
        images_folder = search_images_name()

        chosen_command = input("---------------------------- Welcome! ---------------------------- \n\n"
                               "Enter with a command >>> ")

        if chosen_command.upper() == "EXIT":
            clear_display()
            break

        elif chosen_command.upper() == "UPDATE":
            continue

        elif chosen_command.upper() == "HELP":
            show_help()
            continue
        elif (chosen_command.upper() != "CROP" and chosen_command.upper() != "ROTATE" and
                chosen_command.upper() != "RESIZE" and chosen_command.upper() != "ALL"):
            clear_display()
            print(">>> NO COMMANDS FOUND <<<\n")
            input("Press Enter to try again...")
            continue

        name_image_user = input("\nEnter the name of the image (e.g., Image01.jpeg) >> ")

        image = Image.open(os.path.join(images_folder, name_image_user))
        # print("Dimensions of Image: ", image.size[0])

        if chosen_command.upper() == "CROP":
            image_crop_to_plot = crop_image(image, 0, 0, 0, 0)
            plot_image(image, image_crop_to_plot, "Cropped")

        elif chosen_command.upper() == "ROTATE":
            image_rotate_to_plot = rotation_image(image, 0)
            plot_image(image, image_rotate_to_plot, "Rotated")

        elif chosen_command.upper() == "RESIZE":
            image_resize_to_plot = resize_image(image, 0, 0)
            plot_image(image, image_resize_to_plot, "Resized")

        elif chosen_command.upper() == "ALL":
            image_resize_to_plot = resize_image(image, 0, 0)
            image_crop_to_plot = crop_image(image, 0, 0, 0, 0)
            image_rotate_to_plot = rotation_image(image, 0)
            plot_all_images(image, image_crop_to_plot, image_rotate_to_plot, image_resize_to_plot)


def resize_image(image_to_resize, new_width, new_height):
    if new_width == 0 and new_height == 0:
        create_header("RESIZE", os.path.basename(image_to_resize.filename), str(image_to_resize.size[0]),
                      str(image_to_resize.size[1]))

        values_input = (input("\nEnter with the new width and height to resize. E.g. (width,height) >>> ").
                        replace("(", "").replace(")", ""))

        values_input_array = values_input.split(',')
        new_width, new_height = int(values_input_array[0]), int(values_input_array[1])

    resize_img_matrix = np.array(image_to_resize)
    height, width, layer = resize_img_matrix.shape
    resized_image_matrix = np.zeros((new_height, new_width, layer), dtype=np.uint8)

    mapped_h = np.arange(new_height) * (height / new_height)
    mapped_w = np.arange(new_width) * (width / new_width)

    mapped_h[mapped_h > height - 1] = height-1
    mapped_w[mapped_w > width - 1] = width - 1

    for i in range(mapped_h.size):
        for j in range(mapped_w.size):
            nearest_i, nearest_j = mapped_h[i], mapped_w[j]

            if nearest_i == int(nearest_i) and nearest_j == int(nearest_j):
                resized_image_matrix[i, j] = resize_img_matrix[int(nearest_i), int(nearest_j)]
            elif nearest_i == int(nearest_i):
                nearest_i1, nearest_j1 = int(nearest_i), int(nearest_j)
                nearest_i2, nearest_j2 = int(nearest_i), min(int(nearest_j) + 1, width)
                resized_image_matrix[i, j] = interpolate_pixel(resize_img_matrix, [[nearest_i1, nearest_j1],
                                                                                   [nearest_i2, nearest_j2],
                                                                                   [nearest_i1, nearest_j]], axis=1)
            elif nearest_j == int(nearest_j):
                nearest_i1, nearest_j1 = int(nearest_i), int(nearest_j)
                nearest_i2, nearest_j2 = min(int(nearest_i) + 1, height-1), int(nearest_j)
                resized_image_matrix[i, j] = interpolate_pixel(resize_img_matrix, [[nearest_i1, nearest_j1],
                                                                                   [nearest_i2, nearest_j2],
                                                                                   [nearest_i, nearest_j]], axis=0)
            else:
                nearest_i1, nearest_j1 = int(nearest_i), int(nearest_j)
                nearest_i2, nearest_j2 = int(nearest_i), min(int(nearest_j1) + 1, width - 1)
                nearest_i3, nearest_j3 = min(int(nearest_i) + 1, height - 1), int(nearest_j)
                nearest_i4, nearest_j4 = min(int(nearest_i) + 1, height - 1), min(int(nearest_j) + 1, width - 1)

                pixel_ij1 = interpolate_pixel(resize_img_matrix, [[nearest_i1, nearest_j1],
                                                                  [nearest_i2, nearest_j2],
                                                                  [nearest_i1, nearest_j]], axis=1)
                pixel_ij2 = interpolate_pixel(resize_img_matrix, [[nearest_i3, nearest_j3],
                                                                  [nearest_i4, nearest_j4],
                                                                  [nearest_i3, nearest_j]], axis=1)

                dy1, dy2 = nearest_i - nearest_i1, nearest_i3 - nearest_i
                resized_image_matrix[i, j] = pixel_ij1 * dy2 + pixel_ij2 * dy1

    new_image = Image.fromarray(resized_image_matrix)
    # """  -- Plot Images using PIL -- """
    # concatenated_image = Image.new("RGB", (new_width + width + 30, height + 20))
    #
    # if new_height > height:
    #     concatenated_image = Image.new("RGB", (new_width + width + 30, new_height + 20))
    #
    # concatenated_image.paste(image_to_resize, (10, 10))
    # concatenated_image.paste(new_image, (width + 20, 10))

    # concatenated_image.show()

    return new_image


def interpolate_pixel(image_interp, points, axis=1):
    p1, p2, p3 = points
    pixel_1, pixel_2 = image_interp[p1[0], p1[1]], image_interp[p2[0], p2[1]]
    d1, d2 = p3[axis] - p1[axis], p2[axis] - p3[axis]
    pixel_1_2 = pixel_1 * d2 + pixel_2 * d1

    return pixel_1_2


def crop_image(image_to_crop, x, y, width, height):
    if x == 0 and y == 0 and width == 0 and height == 0:
        create_header("CROP", os.path.basename(image_to_crop.filename), str(image_to_crop.size[0]),
                      str(image_to_crop.size[1]))
        coordinates = (input("\nEnter with the init coordinates. E.g. (x,y) >>> ").replace("(", "").
                       replace(")", ""))
        coordinates_array = coordinates.split(',')
        x, y = round(float(coordinates_array[0])), round(float(coordinates_array[1]))

        new_size = (input("Enter with the width and height. E.g. (width,height) >> ").replace("(", "").
                    replace(")", ""))
        new_size_array = new_size.split(',')
        width, height = round(float(new_size_array[0])), round(float(new_size_array[1]))

    image_matrix = np.array(image_to_crop)
    if x >= 0 and y >= 0 and width >= 0 and height >= 0:
        if x + width <= image_matrix.shape[1] and y + height <= image_matrix.shape[0]:
            cropped_matrix = image_matrix[y:y + height, x:x + width]
            new_image = Image.fromarray(np.uint8(cropped_matrix))

            return new_image

        else:
            print(" >>> Cropping dimensions outside the image boundaries <<<")
            input("\nPress Enter to go for welcome display...")
            return
    else:
        print(">>> Invalid cropping dimensions <<<")
        input("\nPress Enter to go for welcome display...")
        return


def rotation_image(image_to_rotate, degree):
    if degree == 0:
        create_header("ROTATE", os.path.basename(image_to_rotate.filename), str(image_to_rotate.size[0]),
                      str(image_to_rotate.size[1]))
        degree = input("\nEnter with an angle (in degree) of rotation >>> ")

    rads = math.radians(float(degree))
    image_matrix = np.array(image_to_rotate)
    height_image, width_image, layer_image = image_matrix.shape

    height_rot_img = round(abs(height_image * math.cos(rads))) + round(abs(width_image * math.sin(rads)))
    width_rot_img = round(abs(width_image * math.cos(rads))) + round(abs(height_image * math.sin(rads)))

    new_image_matrix = np.uint8(np.zeros((height_rot_img, width_rot_img, layer_image)))

    center_y = int(height_image / 2)
    center_x = int(width_image / 2)

    mid_rot_y, mid_rot_x = (height_rot_img / 2, width_rot_img / 2)

    for y in range(height_rot_img):
        for x in range(width_rot_img):
            new_x = int((math.cos(rads) * (x - mid_rot_x)) - (math.sin(rads) * (y - mid_rot_y)) + center_x)
            new_y = int((math.sin(rads) * (x - mid_rot_x)) + (math.cos(rads) * (y - mid_rot_y)) + center_y)

            if 0 <= new_y < height_image and 0 <= new_x < width_image:
                new_image_matrix[y, x, :] = image_matrix[new_y, new_x, :]

    new_image = Image.fromarray(new_image_matrix)

    return new_image


def plot_image(original_image_to_plot, image_to_plot, title_reference):
    fig, (ax1, ax2) = plt.subplots(1, 2)

    ax1.imshow(original_image_to_plot)
    ax1.set_title('Original Image')

    ax2.imshow(image_to_plot)
    ax2.set_title(title_reference + ' Image')

    plt.tight_layout()

    fig.suptitle(title_reference + ' Image')
    plt.show()


def plot_all_images(original_img, crop_img, rotate_img, resize_img):
    fig, axs = plt.subplots(2, 2)

    axs[0, 0].imshow(original_img)
    axs[0, 0].set_title('Original Image')

    axs[0, 1].imshow(resize_img)
    axs[0, 1].set_title('Resized Image')

    axs[1, 0].imshow(crop_img)
    axs[1, 0].set_title('Cropped Image')

    axs[1, 1].imshow(rotate_img)
    axs[1, 1].set_title('Rotate Image')

    plt.tight_layout()

    fig.suptitle('All Images')
    plt.show()


def clear_display():
    os_name = os.name
    if os_name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


def create_header(name_header, name_image="", width_value="", height_value=""):
    clear_display()
    if width_value != "" and height_value != "":
        print('-------------------------------------------------------------------------------------------------------')
        print('                                            ' + name_header)
        print('-------------------------------------------------------------------------------------------------------')
        print("                      Image name: " + name_image +
              "     Width: " + width_value + ", Height: " + height_value)
        print('-------------------------------------------------------------------------------------------------------')
    else:
        print('-------------------------------------------------------------------------------------------------------')
        print('                                            ' + name_header)
        print('-------------------------------------------------------------------------------------------------------')


def search_images_name():
    folder_code = os.path.dirname(os.path.abspath(__file__))  # Get path to script folder
    search_images_folder = os.path.join(folder_code, 'Images')  # Create a path to Images folder

    folder_files_name = os.listdir(search_images_folder)
    num_columns = 3

    items_per_column = len(folder_files_name) // num_columns
    remainder = len(folder_files_name) % num_columns

    print('------------------------------------------------------------------')
    print('                            IMAGES')
    print('------------------------------------------------------------------')

    for col in range(num_columns):
        start = col * items_per_column + min(col, remainder)
        end = start + items_per_column + (1 if col < remainder else 0)
        print('|    ', end="")
        for i in range(start, end):
            print(f"{folder_files_name[i]:<20}", end="")
        print('|')
    print('__________________________________________________________________\n')

    return search_images_folder
# def update_action():
#     print("Performing update...")
#     input("Press Enter to continue...")


def show_help():
    create_header("HELP")
    print('\n---------------------------------------------------------------------------------------------------------')
    print("COMMAND     |              DESCRIPTION                           |       PARAMETERS")
    print('---------------------------------------------------------------------------------------------------------')
    print("RESIZE      |   Change the size of image                         |   (Width,Height)")
    print("CROP        |   Select a specific part of image                  |   (x,y) | (Width, Height) ")
    print("ROTATE      |   Rotate a image with a determinate angle          |   (Angle in degrees) ")
    print("ALL         |   Will do all actions, Resize, Crop, and Rotate    |   See parameters of each one command")
    print("UPDATE      |   Update list of images that are inside the folder |")
    print("HELP        |   Show the commands of program                     |")
    print("EXIT        |   Close the program                                |")
    print('---------------------------------------------------------------------------------------------------------\n')

    input("Press Enter to continue... ")


if __name__ == '__main__':
    main()
