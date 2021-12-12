
#this version includes preprocessing of images
#this is the test script to test the performnace of viola jones on our dataset
#we are using opencv cascade classifier to detect faces
#the model is haarcascade_frontalface_default.xml
#the detector is the detectMultiScale function in opencv

#this script is used to test the performance of viola jones on our dataset without any preprocessing

#importing the required libraries


#importing libraries
import cv2

import os ,glob

from os import listdir ,makedirs , walk

from os.path import isfile ,join
import sys
import csv


#making the required paths

model_path = './models/haarcascade_frontalface_default.xml'



#this function is used to calculate the test parameters of the model
#we calculate accuracy ,precision ,recall and f1 score
#time taken to detect the faces
#false positives and false negatives


#this is the gaussian blur function
def gaussian_blur(image , list_of_parameters):
    kernel_size = list_of_parameters[0]
    sigma = list_of_parameters[1]
    image = cv2.GaussianBlur(image, (kernel_size, kernel_size), sigma)
    return image

#function for positive detection
#the positive image directory has 7 subdirectories of face images

#this function calculate metrics of one dataset of positive images
#path name as parameter
def data_set_evaluate(path , path_output_folder, dict, label ,  parameters_list):
    files = list(filter(lambda f: isfile(join(path, f)), listdir(path)))    #all images in this directory

    number_of_images = len(files)
    dict['total'] = number_of_images


    for image in files:

        try:
            img = cv2.imread(os.path.join(path, image))
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            #grayscale image ready


            #loading the classifier
            classifier = cv2.CascadeClassifier(model_path)
            #detecting the faces

            #preprocessing the image
            #strt time
            start_time = cv2.getTickCount()

            #apply preprocessing
            #preprocessing method
            try:
                if parameters_list[1] != None:
                    pre_processing_method = parameters_list[1]
                    #call pre-processing method
                    gray_img = pre_processing_method(gray_img, parameters_list[2])
            except:
                with open(path_output_folder + 'execution_output.txt', 'a+') as f:
                    f.write("{} is not pre_processed".format(image))

            #end time
            end_time = cv2.getTickCount()
            #calculating the time taken
            time_taken = (end_time - start_time) / cv2.getTickFrequency()
            #time taken to apply preprocessing
            dict['pre_processing_time'].append(time_taken)


            #setting minNeighbors as per label
            if label == 1:
                min_neighbors = 5
            else:
                min_neighbors = 3

            #timing
            start = cv2.getTickCount()
            faces, reject_levels, level_weights = classifier.detectMultiScale3(gray_img, scaleFactor=1.0485258,minNeighbors=min_neighbors, outputRejectLevels=True)
            end = cv2.getTickCount()
            time = (end - start) / cv2.getTickFrequency()
            #time taken to detect the faces
            dict['time'].append(time)

            #getting the number of faces detected
            number_of_faces = len(faces)

            if label == 1:  #it is face image
                if number_of_faces == 0:
                    dict['false_negative'] += 1
                else:
                    dict['correct'] += 1
                    # storing the reject levels and level weights
                    dict['reject_levels'].append(reject_levels[0])
                    dict['level_weights'].append(level_weights[0])
                #if more than 1 face detected
                if number_of_faces > 1:
                    dict['false_positive'] += number_of_faces - 1

            else:         #non_face image
                if number_of_faces == 0:
                    dict['correct'] += 1
                else:
                    dict['false_positive'] += number_of_faces
                    # storing the reject levels and level weights

                    dict['reject_levels'].append(reject_levels[0])
                    dict['level_weights'].append(level_weights[0])







        except:
            # print("{} is not converted".format(image))
            with open(path_output_folder  +'execution_output.txt', 'a+') as f:
                f.write("{} is not converted".format(image))
    return dict



def test_positive_unit():
    # print("debugging unit")
    path = "./data/face/mit"
    path_output_folder = './output/original_viola_jones/'
    dict = {'total': 0, 'correct': 0, 'false_positive': 0, 'false_negative': 0, 'reject_levels': [],
                           'level_weights': [], 'time': []}

    data_set_evaluate(path, path_output_folder,  dict)



#label variable has label: 1 for face    and 0 for non face
def probe_all_datasets(path , path_output_folder, parameters_list, label ):
    # getting the names of subdirectories
    data_sets = list(filter(lambda f: os.path.isdir(join(path ,f)), listdir(path)))

    # print(data_sets)

    data_dict = {}
    # data_element_dict = { }
    for data_set in data_sets:
            data_dict[data_set] = {'dataset':data_set,'total': 0 ,'correct':0, 'false_positive': 0 , 'false_negative': 0, 'reject_levels' : [] , 'level_weights' : [], 'time':[]  , 'pre_processing_time':[]  }

    #created a dictionary for each subdirectory
    #applying analysis to each subdirectory
    for data_set in data_sets:
        data_set_path = os.path.join(path , data_set)
        data_dict[data_set] = data_set_evaluate(data_set_path, path_output_folder, data_dict[data_set] , label,parameters_list)

    if label == 1:
        label_name = 'face'
    else:
        label_name = 'non_face'

    #writing the results to a csv file
    with open(path_output_folder + parameters_list[0]+'_'+label_name+'_results.csv', 'w') as csvfile:
        fieldnames = ['dataset','total', 'correct', 'false_positive', 'false_negative', 'reject_levels', 'level_weights', 'time', 'pre_processing_time']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for data_set in data_sets:
            writer.writerow(data_dict[data_set])



#name is a string

def test_evaluation(preprocessing_name ,parameters_list):
    face_path = './data/face/'
    non_face_path = './data/non_face/'

    #making the output directory
    path_output_folder = './output/'+preprocessing_name+'/'
    # making text output file

    try:
        makedirs(path_output_folder)
    except:
        pass

    with open(path_output_folder  +'execution_output.txt', 'a+') as f:
        f.write('\n writing outputs of '+preprocessing_name+'_'+parameters_list[0]+'\n')

    # try:
    #     makedirs(path_output_folder)
    # except:
    #     with open(path_output_folder + 'execution_output.txt', 'a+') as f:
    #         f.write("Directory already exist, images will be written in same folder")

    # Folder won't used

    #starting the timer cv2
    start = cv2.getTickCount()

    #analysis on face images
    probe_all_datasets('./data/face/', path_output_folder,parameters_list, 1)
    #analysis on non face images
    probe_all_datasets('./data/non_face/', path_output_folder  ,parameters_list, 0)

    #end timer
    end = cv2.getTickCount()
    #calculating the time taken
    time = (end - start) / cv2.getTickFrequency()

    with open(path_output_folder + 'execution_output.txt', 'a+') as f:
        f.write('Total time ' + preprocessing_name + parameters_list[0] +' = '+str(time) +'\n')







#be careful in list of parameters
#structure of parameters_list is [parameter_string , pre_processing_method, parameters[]]
#3 elements in parameters list
#string , method , list of parameters
def analysis(preprocessing_name , parameters_list = ['', None]):
    test_evaluation(preprocessing_name , parameters_list)



















if __name__ == '__main__':
    # testing_pos()

    start = cv2.getTickCount()
    ksize = 3
    sigma = 1
    parameters_string = 'ksize_' + str(ksize) + '_sigma_' + str(sigma)
    pre_processing_list = [parameters_string , gaussian_blur , [ksize, sigma]]
    analysis("blur" ,pre_processing_list)
    end = cv2.getTickCount()
    time = (end - start) / cv2.getTickFrequency()
    print(time)

    start = cv2.getTickCount()
    ksize = 5
    sigma = 10
    parameters_string = 'ksize_' + str(ksize) + '_sigma_' + str(sigma)
    pre_processing_list = [parameters_string, gaussian_blur, [ksize, sigma]]
    analysis("blur", pre_processing_list)
    end = cv2.getTickCount()
    time = (end - start) / cv2.getTickFrequency()
    print(time)

