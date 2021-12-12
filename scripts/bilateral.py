#bilateral filtering

#importing the required libraries
import numpy as np
import matplotlib.pyplot as plt

from skimage import data, img_as_float , img_as_ubyte
from skimage.restoration import denoise_bilateral
from skimage.restoration import  estimate_sigma
from skimage.metrics import peak_signal_noise_ratio
from skimage.util import random_noise
from  skimage.exposure import rescale_intensity
import  cv2
#h : 0.5 +- (0.3)
#patch size: 5
#patch distance: 2-6

def bilateral_filter(img,list_of_parameters =[1]  ):

    # print(list_of_parameters)


    sigma_spatial = list_of_parameters[0]



    """
    
    """
    #converting opencv image to skimage image
    #check if image is grayscale or color
    if len(img.shape) == 3:
        img = img[:, :, ::-1]       #BGR to RGB
        # channel_axis = -1
        multichannel = True
    else:
        multichannel = False

    #converting image to float
    img = img_as_float(img)

    # estimate the noise standard deviation for grey-scale images/ color images
    # sigma_est = np.mean(estimate_sigma(img, average_sigmas = True , multichannel=multichannel))



    # img = img_as_float(img)
    # #if rgb
    # if multichannel:
    #     img_denoised = denoise_bilateral(img,  sigma_spatial=sigma_spatial, multichannel=True)
    # else:
    #     img_denoised = denoise_bilateral(img, sigma_spatial=sigma_spatial ,multichannel=False)

    if multichannel:
        img_denoised = denoise_bilateral(img,sigma_spatial=sigma_spatial  ,multichannel=True)
    else:
        img_denoised = denoise_bilateral(img, sigma_spatial =sigma_spatial ,multichannel=False)

    # img_denoised = np.nan_to_num(img_denoised)

    # img_denoised = rescale_intensity(img_denoised, out_range=(-1, 1))

    # img_denoised.replace(np.inf , 0 , inplace=True)
    #convert skimage image to opencv image
    if len(img.shape) == 3:
        img_denoised = img_denoised[:, :, ::-1]


    # img_denoised = rescale_intensity(img_denoised, out_range=(-1, 1))
    # min = np.amin(img_denoised)
    # max = np.amax(img_denoised)
    # if min< -1:
    #     print("min is less than -1", min)
    #     #plotimage
    #     plt.imshow(img_denoised)
    #     plt.show()
    # if max>1:
    #     print("max is greater than 1", max)
    #     #plotimage
    #     plt.imshow(img_denoised)
    #     plt.show()


    img_denoised = img_as_ubyte(img_denoised)
    return img_denoised

#
# # #
# def test_bilateral(sigma_spatial):
#     #loading the image using opencv
#     img = cv2.imread('image_test.jpg')
#     print(img.shape)
#     print(type(img))
#     print(img[0][0])
#     print(type(img[0][0]))
#     out = bilateral_filter(img , [sigma_spatial])
#
#
#     #data type of out
#     print(type(out))
#     #shape of out
#     print(out.shape)
#     #data type of out
#     print(type(out[0][0]))
#     print(out[0][0])
#     #plotting the images
#     plt.figure(figsize=(10, 5))
#     plt.subplot(1, 2, 1)
#     plt.imshow(img)
#     plt.axis('off')
#     plt.subplot(1, 2, 2)
#     plt.imshow(out)
#     plt.axis('off')
#     plt.show()
#
#
#
# if __name__ == '__main__':
#     test_bilateral(10)
#
