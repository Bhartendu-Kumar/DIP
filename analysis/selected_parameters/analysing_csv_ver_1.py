

#this script is used to read the csv files and do further analysis on them

#importing libraries
import cv2

import os ,glob
import ast
from os import listdir ,makedirs , walk

from os.path import isfile ,join
import sys
import csv

import numpy as np

import re





########################################
#this code block will be changed as per file name signature
def parameters_header():
    return ['PreProcessing']

def string_to_parameters(name):
    list = name.split('_')
    return  ['MSR']

def pre_processing_name():
    return 'MSR'







#############################################################



#reading viola jones parameters from csv file
def reading_viola_jones(path = '../'):

    #file name : ViolaJones_analysis_results.csv
    with open(join(path, 'ViolaJones_analysis_results.csv'), 'r') as csvfile:
        reader = csv.DictReader(csvfile)


        data_dict = {}
        data_set_names = []

        for row in reader:
            data_dict[row['dataset']] = row
            data_set_names.append(row['dataset'])

        # print(data_set_names)
        # print(data_dict)

        return data_dict , data_set_names





def augment_parameters_columns(dictionary , parameter_name):

    parameter_h = parameters_header()
    parameters = string_to_parameters(parameter_name)
    for index in range(len(parameter_h)):
        dictionary[parameter_h[index]] = parameters[index]

    return dictionary
    # dictionary[]


#this function reads all the csv files in current directory

def csv_file_iterator(path_to_directory = '.'):
    files = list(filter(lambda f: isfile(join(path_to_directory, f)), listdir(path_to_directory)))  # all files in this directory
    files = list(filter(lambda f: f.endswith('_non_face_results.csv'), files))  # only csv files
    #pass to csv_processing
    for file in files:
        csv_processing(file , path_to_directory)

        #####!IMP remove break
        # break
        #

    # files_path = list(map(lambda f: join(path_to_directory, f), files))  # full path

    # return files , path_to_directory

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def is_float(element):
    try:
        float(element)
        return True
    except ValueError:
        return False

def is_number(s):
    return  is_int(s) or is_float(s)


# True Positive calculation
def f1_true_positive(correct , total):
    return correct / total


#False Positive calculation
def f1_false_positive(false_positive , total):
    return false_positive / total

#False Negative calculation
def f1_false_negative(false_negative , total):
    return false_negative / total

#precision
def f1_precision(correct , false_positive):
    return correct / (correct + false_positive)

#recall
def f1_recall(correct , false_negative):
    return correct / (correct + false_negative)

def performance_analysis_face(dataset_dict , dataset_name , parameter_name):
    #calculating total number of images
    total_images = int(dataset_dict['total'])


    correct = int(dataset_dict['correct'])
    false_negative = int(dataset_dict['false_negative'])
    false_positive = int(dataset_dict['false_positive'])
    TP = f1_true_positive(correct , total_images)
    FP = f1_false_positive(false_positive , total_images)
    FN = f1_false_negative(false_negative , total_images)
    precision = f1_precision(correct , false_positive)
    recall = f1_recall(correct , false_negative)


    #time metrics

    #pre-processing time
    pre_processing_time = ast.literal_eval(dataset_dict['pre_processing_time'])
    pre_processing_time = np.array(pre_processing_time)
    pre_processing_time = pre_processing_time.astype(float)

    avg_pre_processing_time = np.sum(pre_processing_time) / total_images
    # std_pre_processing_time = np.std(pre_processing_time)

    #classification time
    classification_time = ast.literal_eval(dataset_dict['time'])
    classification_time = np.array(classification_time)
    classification_time = classification_time.astype(float)
    avg_classification_time = np.sum(classification_time)/ total_images

    #total time
    total_time = pre_processing_time + classification_time
    avg_total_time = np.sum(total_time)/ total_images

    ##
    #confidence scores
    level_weights = [float(s) for s in re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", dataset_dict['level_weights'])]
    level_weights = np.array(level_weights)
    level_weights = level_weights.astype(float)
    avg_level_weights = np.sum(level_weights) / total_images
    len_level_weights = len(level_weights)
    level_weights = np.pad(level_weights, (0, total_images - len_level_weights), 'constant', constant_values=(0, 0))
    std_level_weights = np.std(level_weights)

    # data_set_name = dataset_dict['data_set_name']

    dictionary = {}
    # adding parameters columns
    dictionary = augment_parameters_columns(dictionary, parameter_name)
    # dictionary = {'dataset' :  dataset_name, 'TP' : TP , 'FP' : FP , 'FN' : FN , 'precision' : precision , 'recall' : recall , 'avg_pre_processing_time' : avg_pre_processing_time , 'avg_classification_time' : avg_classification_time , 'avg_total_time' : avg_total_time , 'avg_level_weights' : avg_level_weights , 'std_level_weights' : std_level_weights}

    #augumenting all analysis columns
    dictionary['dataset'] = dataset_name
    dictionary['TP'] = TP
    dictionary['FP'] = FP
    dictionary['FN'] = FN
    dictionary['precision'] = precision
    dictionary['recall'] = recall
    dictionary['avg_pre_processing_time'] = avg_pre_processing_time
    dictionary['avg_classification_time'] = avg_classification_time
    dictionary['avg_total_time'] = avg_total_time
    dictionary['avg_level_weights'] = avg_level_weights
    dictionary['std_level_weights'] = std_level_weights

    return dictionary


#over all face datasets

def performance_analysis_face_all_datasets(data_dict ,data_set_names , parameter_name):

    #initializing the variables
    total_images = 0
    correct = 0
    false_negative = 0
    false_positive = 0
    pre_processing_time = []
    classification_time = []
    total_time = []
    level_weights = []

    for data_set in data_set_names:
        dataset_dict = data_dict[data_set]
        #calculating total number of images
        total_images += int(dataset_dict['total'])


        correct += int(dataset_dict['correct'])
        false_negative += int(dataset_dict['false_negative'])
        false_positive += int(dataset_dict['false_positive'])
        pre_processing_time += ast.literal_eval(dataset_dict['pre_processing_time'])
        classification_time += ast.literal_eval(dataset_dict['time'])
        level_weights += [float(s) for s in re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", dataset_dict['level_weights'])]

    TP = f1_true_positive(correct , total_images)
    FP = f1_false_positive(false_positive , total_images)
    FN = f1_false_negative(false_negative , total_images)
    precision = f1_precision(correct , false_positive)
    recall = f1_recall(correct , false_negative)


    #time metrics

    #pre-processing time

    pre_processing_time = np.array(pre_processing_time)
    pre_processing_time = pre_processing_time.astype(float)

    avg_pre_processing_time = np.sum(pre_processing_time) / total_images
    # std_pre_processing_time = np.std(pre_processing_time)

    #classification time

    classification_time = np.array(classification_time)
    classification_time = classification_time.astype(float)
    avg_classification_time = np.sum(classification_time) / total_images

    #total time
    total_time = pre_processing_time + classification_time
    avg_total_time = np.sum(total_time) / total_images

    ##
    #confidence scores

    level_weights = np.array(level_weights)
    level_weights = level_weights.astype(float)
    avg_level_weights = np.sum(level_weights) / total_images
    len_level_weights = len(level_weights)
    level_weights = np.pad(level_weights, (0, total_images - len_level_weights), 'constant', constant_values=(0, 0))

    std_level_weights = np.std(level_weights)

    # data_set_name = dataset_dict['data_set_name']

    dictionary = {}
    # adding parameters columns
    dictionary = augment_parameters_columns(dictionary, parameter_name)
    # dictionary = {'dataset' :  dataset_name, 'TP' : TP , 'FP' : FP , 'FN' : FN , 'precision' : precision , 'recall' : recall , 'avg_pre_processing_time' : avg_pre_processing_time , 'avg_classification_time' : avg_classification_time , 'avg_total_time' : avg_total_time , 'avg_level_weights' : avg_level_weights , 'std_level_weights' : std_level_weights}

    #augumenting all analysis columns
    dictionary['dataset'] = 'TotalFace'
    dictionary['TP'] = TP
    dictionary['FP'] = FP
    dictionary['FN'] = FN
    dictionary['precision'] = precision
    dictionary['recall'] = recall
    dictionary['avg_pre_processing_time'] = avg_pre_processing_time
    dictionary['avg_classification_time'] = avg_classification_time
    dictionary['avg_total_time'] = avg_total_time
    dictionary['avg_level_weights'] = avg_level_weights
    dictionary['std_level_weights'] = std_level_weights

    return dictionary


#performance analysis for non face over all datasets
def performance_analysis_non_face_all_datasets(data_dict ,data_set_names , parameter_name):

    #initializing the variables
    total_images = 0
    correct = 0
    false_negative = 0
    false_positive = 0
    pre_processing_time = []
    classification_time = []
    total_time = []
    level_weights = []

    for data_set in data_set_names:
        dataset_dict = data_dict[data_set]
        #calculating total number of images
        total_images += int(dataset_dict['total'])


        correct += int(dataset_dict['correct'])
        false_negative += int(dataset_dict['false_negative'])
        false_positive += int(dataset_dict['false_positive'])
        pre_processing_time += ast.literal_eval(dataset_dict['pre_processing_time'])
        classification_time += ast.literal_eval(dataset_dict['time'])
        level_weights += [float(s) for s in re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", dataset_dict['level_weights'])]

    TP = f1_true_positive(correct , total_images)       #true negative
    FP = f1_false_positive(false_positive , total_images)
    FN = 0
    precision = 1                                       #no positive samples
    recall = f1_recall(correct , false_positive)


    #time metrics

    #pre-processing time

    pre_processing_time = np.array(pre_processing_time)
    pre_processing_time = pre_processing_time.astype(float)

    avg_pre_processing_time = np.sum(pre_processing_time)   / total_images
    # std_pre_processing_time = np.std(pre_processing_time)

    #classification time

    classification_time = np.array(classification_time)
    classification_time = classification_time.astype(float)
    avg_classification_time = np.sum(classification_time) / total_images

    #total time
    total_time = pre_processing_time + classification_time
    avg_total_time = np.sum(total_time) / total_images

    ##
    # confidence scores

    level_weights = np.array(level_weights)
    level_weights = level_weights.astype(float)
    avg_level_weights = np.sum(level_weights)   / total_images
    len_level_weights = len(level_weights)
    level_weights = np.pad(level_weights, (0, total_images - len_level_weights), 'constant', constant_values=(0, 0))

    std_level_weights = np.std(level_weights)

    # data_set_name = dataset_dict['data_set_name']

    dictionary = {}
    # adding parameters columns
    dictionary = augment_parameters_columns(dictionary, parameter_name)
    # dictionary = {'dataset' :  dataset_name, 'TP' : TP , 'FP' : FP , 'FN' : FN , 'precision' : precision , 'recall' : recall , 'avg_pre_processing_time' : avg_pre_processing_time , 'avg_classification_time' : avg_classification_time , 'avg_total_time' : avg_total_time , 'avg_level_weights' : avg_level_weights , 'std_level_weights' : std_level_weights}

    # augumenting all analysis columns
    dictionary['dataset'] = 'NonFace'
    dictionary['TP'] = TP
    dictionary['FP'] = FP
    dictionary['FN'] = FN
    dictionary['precision'] = precision
    dictionary['recall'] = recall
    dictionary['avg_pre_processing_time'] = avg_pre_processing_time
    dictionary['avg_classification_time'] = avg_classification_time
    dictionary['avg_total_time'] = avg_total_time
    dictionary['avg_level_weights'] = avg_level_weights
    dictionary['std_level_weights'] = std_level_weights

    return dictionary


def percentage_increase(old_value , new_value):
    old_value = float(old_value)
    new_value = float(new_value)
    return  (new_value - old_value)

def perc_inc(old_value , new_value):
    old_value = float(old_value)
    new_value = float(new_value)
    return  ((new_value - old_value) / old_value ) * 100
#this function converts absolute metrics to percentage relative to viola_data_dict
def absolute_metrics_to_relative_metrics(dictionary):

    viola_data_dict , viola_data_set_names = reading_viola_jones()
    relative_dictionary = dictionary.copy()     #will save in this dictionary

    for data_set in viola_data_set_names:
        viola_dataset_dict = viola_data_dict[data_set]
        current_dataset_dict = dictionary[data_set]
        final_dataset_dict = relative_dictionary[data_set]
        #convert all absolute metrics to relative in final_dataset_dict
        final_dataset_dict['TP'] = percentage_increase((viola_dataset_dict['TP']) , (current_dataset_dict['TP']))
        final_dataset_dict['FP'] = percentage_increase((viola_dataset_dict['FP']) , (current_dataset_dict['FP']))
        final_dataset_dict['FN'] = percentage_increase((viola_dataset_dict['FN']) , (current_dataset_dict['FN']))
        final_dataset_dict['precision'] = percentage_increase((viola_dataset_dict['precision']) , (current_dataset_dict['precision']))
        final_dataset_dict['recall'] = percentage_increase((viola_dataset_dict['recall']) , (current_dataset_dict['recall']))
        final_dataset_dict['avg_pre_processing_time'] = perc_inc((viola_dataset_dict['avg_pre_processing_time']) , (current_dataset_dict['avg_pre_processing_time']))
        final_dataset_dict['avg_classification_time'] = perc_inc((viola_dataset_dict['avg_classification_time']) , (current_dataset_dict['avg_classification_time']))
        final_dataset_dict['avg_total_time'] = perc_inc((viola_dataset_dict['avg_total_time']) , (current_dataset_dict['avg_total_time']))
        final_dataset_dict['avg_level_weights'] = perc_inc((viola_dataset_dict['avg_level_weights']) , (current_dataset_dict['avg_level_weights']))
        final_dataset_dict['std_level_weights'] = perc_inc((viola_dataset_dict['std_level_weights']) , (current_dataset_dict['std_level_weights']))

    return relative_dictionary










def csv_processing(file , path_to_directory):
    #file is _non_face_results.csv
    # parameter_headers = parameters_header()

    parameter_name = file.replace('_non_face_results.csv', '')

    #face results file
    face_file = parameter_name + '_face_results.csv'

    #non face results file
    non_face_file = file

    # parameters = string_to_parameters(name)

    #opening the file for face results in dictionary
    with open(join(path_to_directory, face_file), 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        data_dict = {}
        data_set_names = []

        for row in reader:
            data_dict[row['dataset']] = row
            data_set_names.append(row['dataset'])




    #file closed

    #create analysis dict
    analysis_dict = {}
    for dataset_name in data_set_names:
        analysis_dict[dataset_name] = performance_analysis_face(data_dict[dataset_name] , dataset_name , parameter_name )

    # print(analysis_dict)

    #total metrics face analysis
    analysis_dict['TotalFace'] = performance_analysis_face_all_datasets(data_dict ,data_set_names , parameter_name)
    # print(analysis_dict)

    #send dict for each dataset to

    #non face
    #openinng the file for non face results in dictionary
    with open(join(path_to_directory, non_face_file), 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        non_face_data_dict = {}
        non_face_data_set_names = []

        for row in reader:
            non_face_data_dict[row['dataset']] = row
            non_face_data_set_names.append(row['dataset'])

    #file closed
    analysis_dict['NonFace'] = performance_analysis_non_face_all_datasets(non_face_data_dict , non_face_data_set_names , parameter_name)
    # print(analysis_dict)
    # print(list(analysis_dict.keys()))


    #relative analysis
    analysis_dict = absolute_metrics_to_relative_metrics(analysis_dict)




    pre_processing = pre_processing_name()
    csv_file_name = pre_processing+'_analysis_results.csv'
    #check if csv file exists
    if os.path.isfile(join(path_to_directory, csv_file_name)):
        csv_exists = True
    else:
        csv_exists = False

    #fieldnames
    fieldnames = list(analysis_dict['TotalFace'].keys())
    #if not exists create csv file
    if not csv_exists:
        with open(join(path_to_directory, csv_file_name), 'w') as csvfile:

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()



    #
    # #write analysis dict to csv
    with open(join(path_to_directory, csv_file_name), 'a+') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        for data_set in list(analysis_dict.keys()):
            writer.writerow(analysis_dict[data_set])










#os join
# def extract_parameters_from_file_names(files , path_to_directory):
#     #creating list of parameters
#     parameters = []
#     parameter_headers = []
#
#     #extracting the names of the parameters
#     for file in files:
#
#         #
#         print("file",file)
#         #
#         if file.endswith('_face_results.csv'):
#
#             #
#             print("file.endswith('_face_results.csv')",file)
#             #
#             parameter_string = file.replace('_face_results.csv', '')
#             parameter_string_list = parameter_string.split('_')
#
#             #
#             print("parameter_string",parameter_string)
#             print("parameter_string_list",parameter_string_list)
#             #
#             count = 0
#             while count < len(parameter_string_list):
#
#                 print("count",count)
#                 if is_number(parameter_string_list[count]):
#                     print("in if num para ", parameter_string_list[count])
#
#                     count += 1
#                 else:
#
#                     print("in else num para ", parameter_string_list[count])
#                     parameter_headers.append(parameter_string_list[count])
#                     count += 2
#
#             break
#     #if parameter_headers is empty
#     if len(parameter_headers) == 0:
#         print("parameter_headers is empty")
#         parameter_headers.append('name')
#
#     # print("parameter headers",parameter_headers)
#
#     for file in files:
#         if file.endswith('_face_results.csv'):
#
#             print("file.endswith('_face_results.csv')",file)
#             parameter_part = file.replace('_face_results.csv', '')
#             parameter_part_list = parameter_part.split('_')
#
#             #
#             print("parameter_part",parameter_part)
#             print("parameter_part_list",parameter_part_list)
#             #
#             count = 0
#             while count < len(parameter_part_list):
#
#                 #
#                 print("while loop :count ",count)
#                 if parameter_part_list[count] in parameter_headers:
#
#                     print("in if para ", parameter_part_list[count])
#                     count += 1
#                     temp_count  = count
#
#                     while temp_count < len(parameter_part_list):
#
#                         print("inner while loop :temp_count ",temp_count)
#                         if parameter_part_list[temp_count] not in parameter_headers:
#
#                             print("inner if para ", parameter_part_list[temp_count])
#                             parameters.append(parameter_part_list[temp_count])
#                             temp_count += 1
#                         else:
#
#                             print("inner else para ", parameter_part_list[temp_count])
#                             count = temp_count
#                             break
#                 else:
#
#                     print("outer else ", parameter_part_list[count])
#                     if len(parameter_headers) == 1  and parameter_headers[0] == 'name':
#                         parameters.append(parameter_part_list[count])
#
#                         print("parameters",parameters)
#                         count += 1
#         #parameters have been extracted for the first file
#
#         #process this file
#         csv_processing(os.path.join(path_to_directory, file) , parameter_headers , parameters)
#         #
#         parameters = []
#
#
#
#
#
#
#
#
#
#
#







def test_csv_file_iterator():
    csv_file_iterator()



    # extract_parameters_from_file_names(files , files_path)

def test_viola_reading():
     a , b = reading_viola_jones()

def test_general_func():
    print()

if __name__ == '__main__':
    test_csv_file_iterator()

    # test_viola_reading()
    # test_viola_reading()
    # test_general_func()
