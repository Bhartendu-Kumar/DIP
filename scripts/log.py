
#importing libraries
import numpy
import skimage
import skimage.io
import skimage.color
from matplotlib import pyplot, pyplot as plt
from pathlib import Path
import numpy as np

#import stub for histograms, plotting, array manipulation and stuff

# importing libraries
import numpy
import skimage
import skimage.io
import skimage.color
from matplotlib import pyplot, pyplot as plt
from pathlib import Path
import numpy as np

# declaring global array
index_0_255_array = np.array([x for x in range(256)])


# generic function to plot histograms of any number of images given


# parameter to call should be : name<string> = image <ndarray>   pairs
def plot_images(**kwargs):  # generic number of arguments
    list_of_names = [x for x in kwargs.keys()]  # now we have keys

    number_of_images = len(kwargs)

    fig = plt.figure(figsize=(25, 25))  # create instance of figure
    # figsize to make plots smaller or larger, it is large
    hor = 2  # 2 rows, first has horizontal stack of images, second has horizontal stack of histograms
    ver = number_of_images  # columns as number of images passed to function

    # first row has plots of images
    for x in range(number_of_images):
        fig.add_subplot(hor, ver, (x + 1))  # indexing of subplots starts at 1
        pyplot.imshow(kwargs[list_of_names[x]], cmap='gray', vmin=0, vmax=255, aspect="auto")
        pyplot.title(list_of_names[x], fontsize=20)

    for x in range(number_of_images):
        fig.add_subplot(hor, ver, (x + 1 + number_of_images))
        pyplot.plot(index_0_255_array, histogram(kwargs[list_of_names[x]]))
        pyplot.xlabel('intensities')
    plt.show()


# same as above function, just saving plots to file instead of displying
# could have implemented signle function via a flag, but its called much frequently, so writing sepearte is good

def save_plot_images(path, **kwargs):  # generic number of arguments
    list_of_names = [x for x in kwargs.keys()]  # now we have keys

    number_of_images = len(kwargs)

    fig = plt.figure(figsize=(25, 25))  # create instance of figure
    # figsize to make plots smaller or larger, it is large
    hor = 2  # 2 rows, first has horizontal stack of images, second has horizontal stack of histograms
    ver = number_of_images  # columns as number of images passed to function

    # first row has plots of images
    for x in range(number_of_images):
        fig.add_subplot(hor, ver, (x + 1))  # indexing of subplots starts at 1
        pyplot.imshow(kwargs[list_of_names[x]], cmap='gray', vmin=0, vmax=255, aspect="auto")
        pyplot.title(list_of_names[x], fontsize=20)

    for x in range(number_of_images):
        fig.add_subplot(hor, ver, (x + 1 + number_of_images))
        pyplot.plot(index_0_255_array, histogram(kwargs[list_of_names[x]]))
        pyplot.xlabel('intensities')
    plt.savefig(str(path), bbox_inches='tight')  # bbox_inches='tight' to remove extra whitespace

    # for plotting single histogram


def histogram_plotting(image):
    bin_center_array = creating_intensity_index_array()

    # creating intensity array
    bin_intensity = histogram(image)
    # print("histogram")
    # print(bin_intensity)

    # plt.bar(bin_center_array, bin_intensity)

    plt.plot(bin_center_array, bin_intensity)
    plt.show()


# plotting histogram and showing images for 2 images


# function to create histogram of an image
def histogram(image, bins=256) -> numpy.ndarray:
    intensity_array = np.zeros((256,), dtype=int)
    row_count, col_count = image.shape

    image_temp = image.astype(np.uint8)  # ensuring only greyscale images as input        :sanity check

    for row in range(row_count):
        for col in range(col_count):
            index = image[row, col]

            intensity_array[index] = intensity_array[index] + 1

    return intensity_array


# imp   its not 0-1  to 0-255 but float in 0-255 to int 0-255
def array_float_to_0_255(intensity_array):
    intensity_array_temp = intensity_array.astype(int)  # if float to int

    # making intensities saturate to 0 and 255
    intensity_array_temp[intensity_array_temp < 0] = 0  # saturate to 0
    intensity_array_temp[intensity_array_temp > 255] = 255  # saturate to 255

    intensity_array_output = intensity_array_temp.astype(np.uint8)  # appropiate data type

    return intensity_array_output


def array_0_1_to_0_255(intensity_array):
    intensity_array = intensity_array * 255
    intensity_array = array_float_to_0_255(intensity_array)
    return intensity_array


# creating an array storing 0 to 255
def creating_intensity_index_array():
    intensity_index_array = np.zeros((256,), dtype=int)  # stores 0-255

    # creating intensity values array
    sum = 0
    for x in range(256):
        intensity_index_array[x] = sum
        sum += 1

    return intensity_index_array


# changing image as per remapped intensity values

def remap_image_intensities(intensity_mapping, image):
    intensity_index_array = creating_intensity_index_array()  # array from 0-255 values
    image = intensity_mapping[image]  # JUST ONE LINE!!!!     <-
    # it changes the intensity values in "image" as per the inensity mapping
    return image
def logarithmic_intensity_conversion():

    intensity_values = creating_intensity_index_array().astype(float)      #stores 0-255, float just as we will be converting to 0-1

    normalized_intensity_values = intensity_values * (1/255)
    normalized_intensity_values = normalized_intensity_values + 1
    logarithmic_mapping_values = np.log2(normalized_intensity_values)   #as the argument of log will be between 1 and 2, no inf or boundary values possible
    mapping_intensities = array_0_1_to_0_255(logarithmic_mapping_values)     #to map 0-1 to 0-255
    return  mapping_intensities

def log_intensity_stretch(image , parameter_list):
    mapped_intensities = logarithmic_intensity_conversion()
    image_output = remap_image_intensities(mapped_intensities, image)
    return image_output




#expo


def exponential_intensity_conversion():

    intensity_values = creating_intensity_index_array().astype(float)      #stores 0-255, float just as we will be converting to 0-1

    normalized_intensity_values = intensity_values * (1/255)

    raise_intensity_e = np.expm1(normalized_intensity_values)       #y = e^x - 1
    converted_intensity_array = raise_intensity_e * (255/(e-1))



    new_intensity_indexes_array = array_float_to_0_255(converted_intensity_array)        #new intensities in proper range

    return  new_intensity_indexes_array


#map intensities from initial to new
def exponential_constrast_stretch(image , parameter_list):

    mapped_intensities = exponential_intensity_conversion()
    image_output = remap_image_intensities(mapped_intensities, image)
    return image_output



##



#fcfs



def contrast_stretching(image):
    intensity_array = histogram(image)

    # minimum_intensity =
    # maximum_intensity = numpy.argmin(intensity_array)

    #finding index of first non-zero frequency intensity
    for x in range(len(intensity_array)):
        if intensity_array[x] > 0 :
            minimum_present_intensity_index = x
            break

    #finding index of largest intensity present
    for x in range(len(intensity_array) -1 , minimum_present_intensity_index -1, -1 ):          #starting from end and stopping at minimum present intensity
        if intensity_array[x] > 0 :
            maximum_present_intensity_index = x
            break



    #handling edge cases
    if minimum_present_intensity_index == maximum_present_intensity_index:
        return image
    #no FSCS possible

    #if already using full scale of intensities
    if minimum_present_intensity_index == 0 and maximum_present_intensity_index == 255:
        return image

    #non edge cases: i.e. atleast 2 diff intensities

    image_temp = image.astype(int)     #ensuring image to be of INT datatype, UNIT8 have wrap-around behaviour!! CAUTION

    image_temp = image_temp - minimum_present_intensity_index   #( I - min): offset

    intensity_scaling_constant = (255/(maximum_present_intensity_index - minimum_present_intensity_index))

    image_temp = image_temp * intensity_scaling_constant        #scaling   will make array of float

    image_output = image_temp.astype(int)  #due to scaling, it becomes float, now again INT

    #making intensities saturate to 0 and 255
    image_output[image_output < 0] = 0       #saturate to 0
    image_output[image_output > 255] = 255      #saturate to 255

    image_output = image_output.astype(np.uint8)
    return image_output , intensity_array   #now in unit8 form internally, suitable for display



#the driver function for fcfs: returns fscs image and 2 histograms

def full_scale_contrast_stretch(image , parameter_list):
    image_output, intensity_array = contrast_stretching(image)
    return image_output









#



#
# if __name__ == "__main__":
#     image_path = "IIScMainBuilding_LowContrast.png"
#     image = skimage.io.imread(image_path)
#     #histogram_plotting(image)
#     image_output= log_intensity_stretch(image)
#     #plt.imshow(image, cmap='gray', vmin=0, vmax=255)
#     #plotting images
#     output_image_path = "results1/q1_log.png"
#     save_plot_images(output_image_path, original=image , logarithmic_contrast_stretch = image_output)
#

