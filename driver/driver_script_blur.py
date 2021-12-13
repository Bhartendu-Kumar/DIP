#this is the driver code for the blur script
#we will use the test_script_ver_*.py to test the script

#import the script
from ..scripts.test_script_ver_4 import *

#imported the test script



#defining function for blur

#note kernel size be odd
def blur_analysis_driver():
    preprocessing_name = 'gaussian_blur'
    parameters_list = ["", None, []]

    for k_size in range(1,4 , 2):
        for sigma in range(1,2):
            parameters_string = 'k_size_' + str(k_size) + '_sigma_' + str(sigma)
            parameters_list[0] = parameters_string
            method = gaussian_blur
            parameters_list[1] = method
            parameters_list[2] = [k_size, sigma]
            analysis(preprocessing_name, parameters_list)




if __name__ == '__main__':
    blur_analysis_driver()





