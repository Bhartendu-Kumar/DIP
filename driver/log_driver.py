

from ..scripts.test_script_ver_4 import *
from ..scripts.log import log_intensity_stretch , exponential_constrast_stretch , full_scale_contrast_stretch



import  cv2 as cv



#hist equalization
def hist_eq(img , parameter_list):


    if len(img.shape) == 3:
        img[:,:,0] = cv.equalizeHist(img[:,:,0])
        img[:,:,1] = cv.equalizeHist(img[:,:,1])
        img[:,:,2] = cv.equalizeHist(img[:,:,2])
        return img


    img = cv.equalizeHist(img)
    return img


def hist_eq_driver():
    # making preprocessing_name string
    preprocessing_name = "PDE"

    # method as function name
    method = hist_eq
    # making initial list
    parameters_list = ['', method, []]



    parameters_string = 'hist_eq'
    parameters_list[0] = parameters_string
    parameters_list[2] = []
    analysis(preprocessing_name, parameters_list)


def driver_log():
    # making preprocessing_name string
    preprocessing_name = "PDE"

    # method as function name
    method = log_intensity_stretch
    # making initial list
    parameters_list = ['', method, []]



    parameters_string = 'log'
    parameters_list[0] = parameters_string
    parameters_list[2] = []
    analysis(preprocessing_name, parameters_list)



# def

#
def driver_exp():
    # making preprocessing_name string
    preprocessing_name = "PDE"

    # method as function name
    method = exponential_constrast_stretch
    # making initial list
    parameters_list = ['', method, []]



    parameters_string = 'exponential'
    parameters_list[0] = parameters_string
    parameters_list[2] = []
    analysis(preprocessing_name, parameters_list)


def driver_full():
    # making preprocessing_name string
    preprocessing_name = "PDE"

    # method as function name
    method = full_scale_contrast_stretch
    # making initial list
    parameters_list = ['', method, []]



    parameters_string = 'fscs'
    parameters_list[0] = parameters_string
    parameters_list[2] = []
    analysis(preprocessing_name, parameters_list)

def clahe(img , parameter_list):
    clip_limit = parameter_list[0]
    clahe = cv.createCLAHE(clipLimit=clip_limit, tileGridSize=(8, 8))


    if len(img.shape) == 3:
        img[:,:,0] = clahe.apply(img[:,:,0])
        img[:,:,1] = clahe.apply(img[:,:,1])
        img[:,:,2] = clahe.apply(img[:,:,2])

        return img


    img = clahe.apply(img)
    return img



def clahe_driver():
    # making preprocessing_name string
    preprocessing_name = "PDE"

    # method as function name
    method = clahe
    # making initial list
    parameters_list = ['', method, []]


    cutoff_freq_list = [ 2, 3 , 4 ,5 ]
    # cutoff_freq_list = [2]



    #range change
    for clip_limit  in cutoff_freq_list:
        parameters_string = 'clip_limit_' + str(clip_limit)
        parameters_list[0] = parameters_string
        parameters_list[2] = [clip_limit]
        analysis(preprocessing_name, parameters_list)








if __name__ == "__main__":
    driver_log()
    # driver_exp()
    # driver_full()
    hist_eq_driver()
    clahe_driver()



