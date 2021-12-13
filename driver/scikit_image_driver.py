

from ..scripts.test_script_ver_4 import *
from ..scripts.scikit_image_algorithms import tv_bregman , tv_chambolle , wavelet , bda


def driver_tv_bregman():
    # making preprocessing_name string
    preprocessing_name = "tv_bregman"

    # method as function name
    method = tv_bregman
    # making initial list
    parameters_list = ['', method, []]

    #
    # patch_size_list = [ 5 , 10 , 15   ]
    # h_list = [ 0.2 , 0.3 , 0.4 , 0.5 , 0.6 , 0.7 , 0.8  ]
    # patch_distance_list = [2, 3, 4, 5 ,6,7]

    weight_list = [  4, 5, 6, 7, 8 ,3 ]
    # weight_list = [1]

    #range change
    for  weight in weight_list:

        parameters_string = 'weight_' + str(weight)
        parameters_list[0] = parameters_string
        parameters_list[2] = [weight]
        analysis(preprocessing_name, parameters_list)



def driver_tv_chambolle():
    # making preprocessing_name string
    preprocessing_name = "tv_chambolle"

    # method as function name
    method = tv_chambolle
    # making initial list
    parameters_list = ['', method, []]

    #
    # patch_size_list = [ 5 , 10 , 15   ]
    # h_list = [ 0.2 , 0.3 , 0.4 , 0.5 , 0.6 , 0.7 , 0.8  ]
    # patch_distance_list = [2, 3, 4, 5 ,6,7]

    weight_list = [ 0.1 , 0.2 , 0.3 , 0.4 , 0.5 , 0.6 , 0.7 , 0.8 , 0.9]
    # weight_list = [0.1]

    #range change
    for  weight in weight_list:

        parameters_string = 'weight_' + str(weight)
        parameters_list[0] = parameters_string
        parameters_list[2] = [weight]
        analysis(preprocessing_name, parameters_list)

def driver_wavelet():
    # making preprocessing_name string
    preprocessing_name = "wavelet"

    # method as function name
    method = wavelet
    # making initial list
    parameters_list = ['', method, []]

    list = ['haar', 'db1', 'sym2', 'coif1']
    # list = ['db1']
    # weight_list = [ 0.1 , 0.2 , 0.3 , 0.4 , 0.5 , 0.6 , 0.7 , 0.8 , 0.9]
    # weight_list = [0.1]

    #range change
    for  w  in list:

        parameters_string = 'wavelet_' + w
        parameters_list[0] = parameters_string
        parameters_list[2] = [w]
        analysis(preprocessing_name, parameters_list)


def driver_bda():
    # making preprocessing_name string
    preprocessing_name = "BDA"

    # method as function name
    method = bda
    # making initial list
    parameters_list = ['', method, []]



    parameters_string = ''
    parameters_list[0] = parameters_string
    parameters_list[2] = []
    analysis(preprocessing_name, parameters_list)


if __name__ == '__main__':
    driver_bda()

    driver_tv_chambolle()
    driver_wavelet()
    driver_tv_bregman()






