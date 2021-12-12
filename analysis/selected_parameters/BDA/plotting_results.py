
#this script will read a csv file into a dict
#and then plot the results
#importing libraries
import pathlib

import cv2

import os ,glob
import ast
from os import listdir ,makedirs , walk

from os.path import isfile ,join
import sys
import csv

import numpy as np

import csv
import matplotlib.pyplot as plt





########################################
#this part to change for each file

def pre_processing_name_return():
    return 'gaussian_blur'




################################

#read the csv file into a dict

def read_analysis_csv(csv_file_name = None , path = '.'):

    if csv_file_name == None:
        files = list(filter(lambda f: isfile(join(path, f)), listdir(path)))  # all files in this directory

        #if ends with _analysis_results.csv
        csv_file_name = list(filter(lambda f: f.endswith('_analysis_results.csv'), files))
        if len(csv_file_name) == 0 or len(csv_file_name) > 1:
            print("Error: No or more than one csv file found")
        csv_file_name = csv_file_name[0]


    reader = []

    with open(join(path, csv_file_name), 'r') as csvfile:
        reader_d = csv.DictReader(csvfile)
        field_names = reader_d.fieldnames

        for row in reader_d:
            reader.append(row)


    # print(reader)



    return reader , field_names
    # refactor_dict_object(reader , field_names)



        # data_dict = {}
        # data_set_names = []
        #
        # for row in reader:
        #     data_dict[row['dataset']] = row
        #     data_set_names.append(row['dataset'])
        #
        # # print(data_set_names)
        # # print(data_dict)
        #
        # return data_dict , data_set_names

    # return reader



#plot metrics
# def plot_metrics(reader ):
#     metrics_list = ['TP']




#this will create plotting_dict for each parameter

def create_plotting_dict(reader , field_name , first_column):
    list_of_datasets = [ 'BioID','orl','mit_cbcl','yale' , 'caltech','SoF' , 'TotalFace'  ]

    plotting_dict = {}
    for data_set in list_of_datasets:

        #
        # print("data_set: " , data_set)
        #
        plotting_dict[data_set] = {'parameter' :[] , field_name  : []}

        for row in reader:
            if row['dataset'] == data_set:
                plotting_dict[data_set]['parameter'].append(row[first_column])
                plotting_dict[data_set][field_name].append(row[field_name])
        #
        # print(plotting_dict[data_set])
        #

    # print(plotting_dict)

    return plotting_dict
    #
    # for row in reader:
    #     plotting_dict[row['dataset']] = row[field_name]
    #
    # return plotting_dict


def refactor_dict_object(reader , field_names):

    metrics_list = ['TP' ,'FP', 'FN' , 'precision' , 'recall' , 'avg_pre_processing_time' , 'avg_classification_time'  , 'avg_total_time'  , 'avg_level_weights'  , 'std_level_weights']

    #testing
    # metrics_list = ['TP']

    ##

    metric_dict = {}
    for metric in metrics_list:
        metric_dict[metric] = create_plotting_dict(reader , metric , field_names[0])

    # print(metric_dict)

    return metric_dict

def save_plot():
    plt.plot(x_axis, y_axis, label=dataset, color=colors[keys.index(dataset)])
    plt.xlabel('parameter')
    plt.ylabel(metric)
    plt.title(pre_processing_name_return())
    plt.legend()
    plt.tight_layout()
    # print(pathlib.Path.home())
    # plt.savefig(str(pathlib.Path.home()) +'/aaaaGraphs/' + metric + '.png')


def plot_given_metric(dict , metric):
    #extract keys of dict
    keys = list(dict.keys())
    # print(keys)

    #extract x axis values
    x_axis = dict[keys[0]]['parameter']
    # print(type(x_axis))
    # print(type(x_axis[0]))
    # print(x_axis)
    #convert to float
    x_axis = list(map(float , x_axis))
    # print(type(x_axis))
    # print(type(x_axis[0]))
    # print(x_axis)


    #create a list of colors as per the number of datasets
    colors = ['b' , 'g' , 'r' , 'c' , 'm' , 'y' , 'k' ]
    #for y axis looping over datasets
    for dataset in keys:
        y_axis = dict[dataset][metric]

        #sorting y_axis based on x_axis and then sorting x axis

        x_axis , y_axis = (list(t) for t in zip(*sorted(zip(x_axis , y_axis))))

        #convert to float
        y_axis = list(map(float , y_axis))
        #plot with label and color of dataset
        plt.plot(x_axis , y_axis , label = dataset , color = colors[keys.index(dataset)])

    plt.xlabel('parameter')
    plt.ylabel(metric)
    plt.title(pre_processing_name_return())
    plt.legend()
    plt.tight_layout()
    # print(pathlib.Path.home())
    # plt.savefig(str(pathlib.Path.home()) +'/aaaaGraphs/' + metric + '.png')
    # plt.savefig('./graplot.png')
    plt.show()




        ##



def plotting():
    reader, field_names = read_analysis_csv()
    metric_dict = refactor_dict_object(reader, field_names)

    metrics_list = ['TP', 'FP', 'FN', 'precision', 'recall', 'avg_pre_processing_time', 'avg_classification_time',
                    'avg_total_time', 'avg_level_weights', 'std_level_weights']

    #plotting a metric
    #TP
    # metric = 'FP'
    metric_to_plot = ['TP', 'FP', 'FN', 'precision', 'recall' ,'avg_total_time', 'avg_level_weights',]
    for metric in metric_to_plot:
        plot_given_metric(metric_dict[metric] , metric )

    # metric = 'FN'
    # plot_given_metric(metric_dict[metric] , metric )










def test_csv_reader():
    print()
    plotting()



if __name__ == '__main__':
    test_csv_reader()

