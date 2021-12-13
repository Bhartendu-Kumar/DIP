

from ..scripts.test_script_ver_4 import *
from ..scripts.nmbm import nmbm


def driver_nmbm():
    # making preprocessing_name string
    preprocessing_name = "NMBM"

    # method as function name
    method = nmbm
    # making initial list
    parameters_list = ['', method, []]


    patch_size_list = [ 5 , 10 , 15   ]
    h_list = [ 0.2 , 0.3 , 0.4 , 0.5 , 0.6 , 0.7 , 0.8  ]
    patch_distance_list = [2, 3, 4, 5 ,6,7]


    # patch_size=  5
    # h = 0.5
    # patch_distance = 2
    #
    # parameters_string = '_patchSsize_' + str(patch_size) + "_h_" + str((h)) + '_patchDistance_' + str(patch_distance)
    # parameters_list[0] = parameters_string
    # parameters_list[2] = [patch_size, h, patch_distance]
    # analysis(preprocessing_name, parameters_list)

    #range change
    for h  in h_list:
        for patch_size in patch_size_list:
            for patch_distance in patch_distance_list:

                parameters_string = '_patchSsize_' + str(patch_size)+"_h_" + str((h))   + '_patchDistance_' + str(patch_distance)
                parameters_list[0] = parameters_string
                parameters_list[2] = [patch_size,h, patch_distance]
                analysis(preprocessing_name, parameters_list)




driver_nmbm()






