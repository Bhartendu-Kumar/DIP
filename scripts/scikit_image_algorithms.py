#this contains using scikit image functions

# importing the required libraries
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import pywt
from scipy.signal import fftconvolve
from skimage import restoration
from skimage import data, img_as_float, img_as_ubyte
from skimage.restoration import denoise_tv_bregman , denoise_tv_chambolle , denoise_wavelet , unwrap_phase , richardson_lucy
from skimage.restoration import estimate_sigma
from skimage.metrics import peak_signal_noise_ratio
from skimage.util import random_noise
from skimage.exposure import rescale_intensity
from skimage import data, img_as_float, color, exposure
import cv2


# def richardson_lucy_blind(image, psf, original, num_iter=50):
#     im_deconv = np.full(image.shape, 0.1, dtype='float')    # init output
#     for i in range(num_iter):
#         psf_mirror = np.flip(psf)
#         conv = fftconvolve(im_deconv, psf, mode='same')
#         relative_blur = image / conv
#         im_deconv *= fftconvolve(relative_blur, psf_mirror, mode='same')
#         im_deconv_mirror = np.flip(im_deconv)
#         psf *= fftconvolve(relative_blur, im_deconv_mirror, mode='same')
#     return im_deconv



#tv bregman


def tv_bregman(img, list_of_parameters=[5]):
    # print(list_of_parameters)

    weight = float(list_of_parameters[0])

    """

    """
    # converting opencv image to skimage image
    # check if image is grayscale or color
    if len(img.shape) == 3:
        img = img[:, :, ::-1]  # BGR to RGB
        # channel_axis = -1
        multichannel = True
    else:
        multichannel = False

    # converting image to float
    img = img_as_float(img)

    # estimate the noise standard deviation for grey-scale images/ color images
    # sigma_est = np.mean(estimate_sigma(img, average_sigmas = True , multichannel=multichannel))

    # img = img_as_float(img)
    # #if rgb
    # if multichannel:
    #     img_denoised = denoise_bilateral(img,  sigma_spatial=sigma_spatial, multichannel=True)
    # else:
    #     img_denoised = denoise_bilateral(img, sigma_spatial=sigma_spatial ,multichannel=False)

    img_denoised = denoise_tv_bregman(img, weight= weight, multichannel=multichannel )

    img_denoised = np.nan_to_num(img_denoised)

    img_denoised = rescale_intensity(img_denoised, out_range=(-1, 1))

    # img_denoised.replace(np.inf , 0 , inplace=True)
    # convert skimage image to opencv image
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


#list_of_parameters=[0.1]
def tv_chambolle(img,list_of_parameters =[0.1]):
    # print(list_of_parameters)

    weight = float(list_of_parameters[0])

    """

    """
    # converting opencv image to skimage image
    # check if image is grayscale or color
    if len(img.shape) == 3:
        img = img[:, :, ::-1]  # BGR to RGB
        # channel_axis = -1
        multichannel = True
    else:
        multichannel = False

    # converting image to float
    img = img_as_float(img)

    # estimate the noise standard deviation for grey-scale images/ color images
    # sigma_est = np.mean(estimate_sigma(img, average_sigmas = True , multichannel=multichannel))

    # img = img_as_float(img)
    # #if rgb
    # if multichannel:
    #     img_denoised = denoise_bilateral(img,  sigma_spatial=sigma_spatial, multichannel=True)
    # else:
    #     img_denoised = denoise_bilateral(img, sigma_spatial=sigma_spatial ,multichannel=False)

    img_denoised = denoise_tv_chambolle(img, weight= weight, multichannel=multichannel , n_iter_max=50)

    # img_denoised = np.nan_to_num(img_denoised)

    # img_denoised = rescale_intensity(img_denoised, out_range=(-1, 1))

    # img_denoised.replace(np.inf , 0 , inplace=True)
    # convert skimage image to opencv image
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


def wavelet(img, list_of_parameters=['haar']):
    wave = list_of_parameters[0]

    # converting opencv image to skimage image
    # check if image is grayscale or color
    if len(img.shape) == 3:
        img = img[:, :, ::-1]  # BGR to RGB
        # channel_axis = -1
        multichannel = True
    else:
        multichannel = False

    # converting image to float
    img = img_as_float(img)

    # estimate the noise standard deviation for grey-scale images/ color images
    # sigma_est = np.mean(estimate_sigma(img, average_sigmas = True , multichannel=multichannel))


    img_denoised = denoise_wavelet(img, wavelet=wave, multichannel=multichannel)

    img_denoised = np.nan_to_num(img_denoised)
    img_denoised = rescale_intensity(img_denoised, out_range=(-1, 1))

    # img_denoised.replace(np.inf , 0 , inplace=True)

    # convert skimage image to opencv image
    if len(img.shape) == 3:
        img_denoised = img_denoised[:, :, ::-1]



    img_denoised = img_as_ubyte(img_denoised)
    return img_denoised

def phase_unwrapping(img, list_of_parameters=[]):


    # converting opencv image to skimage image
    # check if image is grayscale or color
    if len(img.shape) == 3:
        img = img[:, :, ::-1]  # BGR to RGB



    # converting image to float
    img = img_as_float(img)

    # Scale the image to [0, 4*pi]
    img = exposure.rescale_intensity(img, out_range=(0, 4 * np.pi))

    # estimate the noise standard deviation for grey-scale images/ color images
    # sigma_est = np.mean(estimate_sigma(img, average_sigmas = True , multichannel=multichannel))


    img_denoised = unwrap_phase(img)

    # img_denoised = np.nan_to_num(img_denoised)
    # img_denoised = rescale_intensity(img_denoised, out_range=(-1, 1))

    # img_denoised.replace(np.inf , 0 , inplace=True)

    # # convert skimage image to opencv image
    if len(img.shape) == 3:
        img_denoised = img_denoised[:, :, ::-1]



    img_denoised = img_as_ubyte(img_denoised)
    return img_denoised


#richardson_lucy_deconvolution
def matlab_style_gauss2D(shape=(3,3),sigma=0.5):
    """
    2D gaussian mask - should give the same result as MATLAB's
    fspecial('gaussian',[shape],[sigma])
    """
    m,n = [(ss-1.)/2. for ss in shape]
    y,x = np.ogrid[-m:m+1,-n:n+1]
    h = np.exp( -(x*x + y*y) / (2.*sigma*sigma) )
    h[ h < np.finfo(h.dtype).eps*h.max() ] = 0
    sumh = h.sum()
    if sumh != 0:
        h /= sumh
    return h

def bda(img, list_of_parameters=[]):
    # print(list_of_parameters)

    psf = matlab_style_gauss2D(shape=(5,5),sigma=7)

    """

    """
    # converting opencv image to skimage image
    # check if image is grayscale or color
    if len(img.shape) == 3:
        img = img[:, :, ::-1]  # BGR to RGB
        # channel_axis = -1
        multichannel = True
    else:
        multichannel = False

    # converting image to float
    img = img_as_float(img)

    # estimate the noise standard deviation for grey-scale images/ color images
    # sigma_est = np.mean(estimate_sigma(img, average_sigmas = True , multichannel=multichannel))

    # img = img_as_float(img)
    # #if rgb
    # if multichannel:
    #     img_denoised = denoise_bilateral(img,  sigma_spatial=sigma_spatial, multichannel=True)
    # else:
    #     img_denoised = denoise_bilateral(img, sigma_spatial=sigma_spatial ,multichannel=False)
    img_denoised = img.copy()
    if multichannel:
        img_denoised[0] = restoration.richardson_lucy(img[0], psf, 25)
        img_denoised[1] = restoration.richardson_lucy(img[1], psf, 25)
        img_denoised[2] = restoration.richardson_lucy(img[2], psf, 25)
    else:
        img_denoised = restoration.richardson_lucy(img, psf, 25)

    # img_denoised = np.nan_to_num(img_denoised)

    # img_denoised = rescale_intensity(img_denoised, out_range=(-1, 1))

    # img_denoised.replace(np.inf , 0 , inplace=True)
    # convert skimage image to opencv image
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
def testing():
    #loading the image using opencv
    img = cv2.imread('image_test.jpg')
    print(img.shape)
    print(type(img))
    print(img[0][0])
    print(type(img[0][0]))
    out = tv_chambolle(img)

    #data type of out
    print(type(out))
    #shape of out
    print(out.shape)
    #data type of out
    print(type(out[0][0]))
    print(out[0][0])
    #plotting the images
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(img)
    plt.axis('off')
    plt.subplot(1, 2, 2)
    plt.imshow(out)
    plt.axis('off')
    plt.show()




if __name__ == '__main__':
    testing()
