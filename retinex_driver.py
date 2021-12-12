

from scripts.test_script_ver_4 import *

from scripts.retinex import *
from scripts.retinex import retinex_FM , retinex_SSR, retinex_MSR, retinex_AMSR , retinex_gimp

#signature

#retinex_FM (img,iter=4)

#SSR
#def retinex_SSR(img,sigma)

#MSR
#def retinex_MSR(img,sigmas=[15,80,250],weights=None)

#(ASSR ) or AMSR
# retinex_AMSR(img,sigmas=[12,80,250] , weights=None)

#def retinex_gimp(img,sigmas=[12,80,250], weights=None,dynamic=2)

#function for MSR sigma values

def test_MSR_5():
    # making preprocessing_name string
    preprocessing_name = "MSR"

    # method as function name
    method = retinex_MSR
    # making initial list
    parameters_list = ['', method, []]


    # looping over parameter space
    list_initial_5 = [10, 20, 30 , 40 , 50]
    list_initial_array = np.array(list_initial_5)

    #range change
    for sigma_step in range(0,400, 50 ):
        sigma_array = list_initial_array + sigma_step

        #to list
        sigma_list = sigma_array.tolist()
        string_temp = ""
        for index in range(len(sigma_list)):
            string_temp = string_temp + str(sigma_list[index]) + "_"
        #removing last _
        string_temp = string_temp[:-1]

        parameters_string = "_iter_"+ str(len(sigma_list))+'_sigmas_'+ string_temp
        parameters_list[0] = parameters_string
        parameters_list[2] = [sigma_list]
        analysis(preprocessing_name, parameters_list)



    # #change to 400 , 10
    # test_list = [1, 10000]
    # #range(1, 212 , 10)
    # #range(1, 370 , 35)
    # # for sigma in [[15,80,250]]:
    # parameters_string =  '_sigma_'+str([15,80,250])
    # parameters_list[0] = parameters_string
    # parameters_list[2] = [ [15,80,250]]
    # analysis(preprocessing_name, parameters_list)


def test_MSR_10():
    # making preprocessing_name string
    preprocessing_name = "MSR"

    # method as function name
    method = retinex_MSR
    # making initial list
    parameters_list = ['', method, []]

    # looping over parameter space
    list_initial_10 = [10, 20, 30, 40, 50 , 60 , 70 , 80 , 90 , 100]
    list_initial_array = np.array(list_initial_10)

    # range change
    for sigma_step in range(0, 301, 40):
        sigma_array = list_initial_array + sigma_step

        # to list
        sigma_list = sigma_array.tolist()
        string_temp = ""
        for index in range(len(sigma_list)):
            string_temp = string_temp + str(sigma_list[index]) + "_"
        # removing last _
        string_temp = string_temp[:-1]

        parameters_string = "_iter_" + str(len(sigma_list)) + '_sigmas_' + string_temp
        parameters_list[0] = parameters_string
        parameters_list[2] = [sigma_list]
        analysis(preprocessing_name, parameters_list)


def test_MSR_15():
    # making preprocessing_name string
    preprocessing_name = "MSR"

    # method as function name
    method = retinex_MSR
    # making initial list
    parameters_list = ['', method, []]

    # looping over parameter space
    list_initial_15 = [10, 15 , 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80]
    list_initial_array = np.array(list_initial_15)

    # range change
    for sigma_step in range(0, 310, 40):
        sigma_array = list_initial_array + sigma_step

        # to list
        sigma_list = sigma_array.tolist()
        string_temp = ""
        for index in range(len(sigma_list)):
            string_temp = string_temp + str(sigma_list[index]) + "_"
        # removing last _
        string_temp = string_temp[:-1]

        parameters_string = "_iter_" + str(len(sigma_list)) + '_sigmas_' + string_temp
        parameters_list[0] = parameters_string
        parameters_list[2] = [sigma_list]
        analysis(preprocessing_name, parameters_list)


def test_MSR_20():
    # making preprocessing_name string
    preprocessing_name = "MSR"

    # method as function name
    method = retinex_MSR
    # making initial list
    parameters_list = ['', method, []]

    # looping over parameter space
    list_initial_20 = [5 , 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
    list_initial_array = np.array(list_initial_20)

    # range change
    for sigma_step in range(0, 310, 40):
        sigma_array = list_initial_array + sigma_step

        # to list
        sigma_list = sigma_array.tolist()
        string_temp = ""
        for index in range(len(sigma_list)):
            string_temp = string_temp + str(sigma_list[index]) + "_"
        # removing last _
        string_temp = string_temp[:-1]

        parameters_string = "_iter_" + str(len(sigma_list)) + '_sigmas_' + string_temp
        parameters_list[0] = parameters_string
        parameters_list[2] = [sigma_list]
        analysis(preprocessing_name, parameters_list)


test_MSR_5()
test_MSR_10()
test_MSR_15()
test_MSR_20()
