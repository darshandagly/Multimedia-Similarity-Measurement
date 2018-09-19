import time
from bs4 import BeautifulSoup
import numpy
import os
import scipy.spatial.distance
import re
import heapq as hq

# Calculating Euclidean Distance for other Models
def calculate_distance(location, other_location):
    input2darray = numpy.loadtxt(location, delimiter=",").astype('float')
    db2darray = numpy.loadtxt(other_location, delimiter=",").astype('float')
    dist = scipy.spatial.distance.cdist(input2darray[:, 1:], db2darray[:, 1:], metric='euclidean')
    return numpy.median(dist)

# Calculating Euclidean Distance for 3x3 Spatial Pyramid Representation
def calculate_3x3_distance(location, other_location):
    input2darray = numpy.loadtxt(location, delimiter=",").astype('float')
    db2darray = numpy.loadtxt(other_location, delimiter=",").astype('float')
    col = 1
    dist = numpy.zeros(shape=(input2darray.shape[0], db2darray.shape[0]))
    while col < input2darray.shape[1]:
        dist += scipy.spatial.distance.cdist(input2darray[:, col:col + 9], db2darray[:, col:col + 9],
                                             metric='euclidean')
        col += 9
    dist = dist / 9
    return numpy.median(dist)


def main():
    # Setting up dataset directory
    loc_data_dir = os.getcwd() + '\dataset\descvis\img\\'
    devset_topic_file_loc = os.getcwd() + '\dataset\devset_topics.xml'

    models = ['CM', 'CM3x3', 'CN', 'CN3x3', 'CSD', 'GLRLM', 'GLRLM3x3', 'HOG', 'LBP', 'LBP3x3']
    invalid_input_flag = False

    # Taking User Input
    user_input = input('Enter Location ID, and k:')
    start_time = time.time()
    input_location_id = int(user_input.split(' ')[0])
    input_k = int(user_input.split(' ')[1])

    # Mapping Input Location ID to Location Name
    other_loc_vd_fnames = []
    input_loc_vd_fname = []
    output = []
    location_names = []
    with open(devset_topic_file_loc) as file:
        soup = BeautifulSoup(file, 'html.parser')
    for topic in soup.find_all('topic'):
        location_names.append(topic.title.contents[0])
        for model in models:
            if int(topic.number.contents[0]) == input_location_id:
                input_loc_vd_fname.append(loc_data_dir + topic.title.contents[0] + ' ' + model + '.csv')
                other_loc_vd_fnames.append(loc_data_dir + topic.title.contents[0] + ' ' + model + '.csv')
                output.append([topic.title.contents[0] + ' ' + model])
                input_location_name = topic.title.contents[0]
            else:
                other_loc_vd_fnames.append(loc_data_dir + topic.title.contents[0] + ' ' + model + '.csv')
                output.append([topic.title.contents[0] + ' ' + model])

    # Checking for location ID validity
    if 'input_loc_vd_fname' not in locals():
        print('Invalid Image ID Entered. Please enter a valid Image ID')
        invalid_input_flag = True
    else:
        # Calculating Euclidean Distance
        for location in input_loc_vd_fname:
            input2darray = numpy.loadtxt(location, delimiter=",").astype('float')
            model = location.split(' ')[-1]
            for i in range(len(other_loc_vd_fnames)):
                if model in other_loc_vd_fnames[i]:
                    if '3x3' in model:
                        output[i].append(calculate_3x3_distance(location, other_loc_vd_fnames[i]))
                    else:
                        output[i].append(calculate_distance(location, other_loc_vd_fnames[i]))

        # Normalize the output
        model_grouped_output_norm = []
        normalised_output = []
        for model in models:
            output_model_slice = [data for data in output if re.search(r'\b' + model + r'\b', data[0])]
            maximum = max(output_model_slice, key=lambda x: x[1])[1]
            for data in output_model_slice:
                data[1] = data[1] / maximum
                model_grouped_output_norm.append(data)

        #Group output based on locations
        location_grouped_output = []
        for location in location_names:
            output_location_slice = [data for data in output if re.search(r'\b' + location + r'\b', data[0])]
            location_grouped_output.append([input_location_name,location, numpy.mean([dist[1] for dist in output_location_slice]),output_location_slice])

        # Show all locations if k is greater than output size
        if input_k > len(location_grouped_output):
            input_k = len(location_grouped_output)

        #Printing k smallest location pairs
        for data in hq.nsmallest(input_k, location_grouped_output, key=lambda x: x[1]):
            print(data)

        end_time = time.time()
        print('Program Execution Time : ', end_time - start_time)

    if invalid_input_flag is True:
        print('-' * 25)
        time.sleep(0.8)
        main()


if __name__ == '__main__':
    main()
