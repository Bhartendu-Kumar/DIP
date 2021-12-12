
from scripts.test_script_ver_4 import *
from scripts.hist_eq import hist_eq

def driver_he():
    # making preprocessing_name string
    preprocessing_name = "HE"

    # method as function name
    method = hist_eq
    # making initial list
    parameters_list = ['', method, []]



    parameters_string = 'histogram_eq'
    parameters_list[0] = parameters_string
    parameters_list[2] = []
    analysis(preprocessing_name, parameters_list)



# def





































if __name__ == "__main__":
    driver_he()



