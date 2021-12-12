#this is the driver script to run the test analysis

#it first imports the test script file

#import the script
from scripts.test_script_ver_4 import *
#the function from this script that we will use is
#analysis
#the parameter signature: (string , list)
#string is preprocessing_name
#list is  parameters_list is [parameter_string , pre_processing_method, parameters[]]
#3 elements in parameters list
#string , method , list of parameters


def original(img , list_of_parameters):
    return img


#import methods of preprocessing
# from scripts.pre_processing_methods_ver_0 import *

#imports done

#now we will run one method for analysis

#blur analysis
def original_analysis():

    #making preprocessing_name string
    preprocessing_name = "violaJones"

    #method as function name
    method = original
    #making initial list
    parameters_list = ['', method, []]


    parameters_string = ''
    parameters_list[0] = parameters_string
    parameters_list[2] = []
    analysis(preprocessing_name, parameters_list)
        
        

original_analysis()




#weiner analysis
