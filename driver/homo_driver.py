

from ..scripts.test_script_ver_4 import *
from ..scripts.homo import homo


def driver_homo():
    # making preprocessing_name string
    preprocessing_name = "HOMO"

    # method as function name
    method = homo
    # making initial list
    parameters_list = ['', method, []]


    cutoff_freq_list = [ 10 , 15 , 20, 25 , 30 ,35 , 40 , 45 ]
    # cutoff_freq_list = [30]



    # patch_size=  5
    # h = 0.5
    # patch_distance = 2
    #
    # parameters_string = '_patchSsize_' + str(patch_size) + "_h_" + str((h)) + '_patchDistance_' + str(patch_distance)
    # parameters_list[0] = parameters_string
    # parameters_list[2] = [patch_size, h, patch_distance]
    # analysis(preprocessing_name, parameters_list)

    #range change
    for cutoff_freq  in cutoff_freq_list:
        parameters_string = 'cutoffFrequency_' + str(cutoff_freq)
        parameters_list[0] = parameters_string
        parameters_list[2] = [cutoff_freq]
        analysis(preprocessing_name, parameters_list)






driver_homo()



