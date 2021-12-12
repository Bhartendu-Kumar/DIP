#this file has all the preprocessing methods for the viola-jones that we want to look at

#importing the necessary libraries
import cv2

#the format to be followed is that there be 2 parameters
#first be image
#second is list , having all the parameters

#gaussian blur
#this is the gaussian blur function
def gaussian_blur(image , list_of_parameters):
    kernel_size = list_of_parameters[0]
    sigma = list_of_parameters[1]
    image = cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)
    return image

