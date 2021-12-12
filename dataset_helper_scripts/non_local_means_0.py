# Non Local means preprocessing
#NMBN: An enhancement for the well known
#Non-Local Means Algorithm (NL Means)

#importing the required libraries
import numpy as np
import matplotlib.pyplot as plt

from skimage import data, img_as_float , img_as_ubyte
from skimage.restoration import denoise_nl_means, estimate_sigma
from skimage.metrics import peak_signal_noise_ratio
from skimage.util import random_noise

import  cv2
#h : 0.5 +- (0.3)
#patch size: 5
#patch distance: 2-6

def nmbm(img,list_of_parameters =[5 , 0.5 , 2]  ):

    patch_size = list_of_parameters[0]
    h = list_of_parameters[1]
    patch_distance = list_of_parameters[2]


    """
    Non-Local Means Denoising
    """
    #converting opencv image to skimage image
    #check if image is grayscale or color
    if img.shape[2] == 3:
        img = img[:, :, ::-1]
        multichannel = True
    else:
        multichannel = False

    #converting image to float
    img = img_as_float(img)

    # estimate the noise standard deviation for grey-scale images/ color images
    sigma_est = np.mean(estimate_sigma(img, average_sigmas = True , multichannel=multichannel))



    # img = img_as_float(img)
    img_denoised =  denoise_nl_means(img, h=h* sigma_est, sigma=sigma_est,fast_mode=False, patch_size=patch_size, patch_distance=patch_distance , multichannel=multichannel)

    #convert skimage image to opencv image
    if img.shape[2] == 3:
        img_denoised = img_denoised[:, :, ::-1]

    img_denoised = img_as_ubyte(img_denoised)
    return img_denoised


#
# def test_NMBM():
#     #loading the image using opencv
#     img = cv2.imread('test_img.jpg')
#     out = NMBM(img , h = 0)
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
#     test_NMBM()

