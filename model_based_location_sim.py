from bs4 import BeautifulSoup
import numpy
import heapq as hq
import time
import scipy.spatial.distance
import os


# Calculating Euclidean Distance for other Models
def calculate_distance(input_loc_vd_fname, other_loc_vd_fnames, output, input_k):
    input2darray = numpy.loadtxt(input_loc_vd_fname, delimiter=",").astype('float')
    for i in range(len(other_loc_vd_fnames)):
        images = []
        db2darray = numpy.loadtxt(other_loc_vd_fnames[i], delimiter=",").astype('float')
        dist = scipy.spatial.distance.cdist(input2darray[:, 1:], db2darray[:, 1:], metric='euclidean')
        min_dist = numpy.sort(dist.flatten())[:3]
        for x in min_dist:
            idx1, idx2 = numpy.where(dist == x)
            images.append([int(input2darray[idx1, 0]), int(db2darray[idx2, 0])])
        output[i].append(numpy.median(dist))
        output[i].append(images)
    return hq.nsmallest(input_k, output, key=lambda x: x[1])

# Calculating Euclidean Distance for 3x3 Spatial Pyramid Representation
def calculate_3x3_distance(input_loc_vd_fname, other_loc_vd_fnames, output, input_k):
    input2darray = numpy.loadtxt(input_loc_vd_fname, delimiter=",").astype('float')
    for i in range(len(other_loc_vd_fnames)):
        images = []
        db2darray = numpy.loadtxt(other_loc_vd_fnames[i], delimiter=",").astype('float')
        col = 1
        dist = numpy.zeros(shape=(input2darray.shape[0], db2darray.shape[0]))
        while col < input2darray.shape[1]:
            dist += scipy.spatial.distance.cdist(input2darray[:, col:col + 9], db2darray[:, col:col + 9],
                                                 metric='euclidean')
            col += 9
        dist = dist / 9
        min_dist = numpy.sort(dist.flatten())[:3]
        for x in min_dist:
            idx1, idx2 = numpy.where(dist == x)
            images.append([int(input2darray[idx1, 0]), int(db2darray[idx2, 0])])
        output[i].append(numpy.median(dist))
        output[i].append(images)

    return hq.nsmallest(input_k, output, key=lambda x: x[1])


def main():
    # Setting up dataset directory
    loc_data_dir = os.getcwd() + '\dataset\descvis\img\\'
    devset_dir = os.getcwd() + '\dataset\\'
    invalid_input_flag = False

    # Taking User Input
    user_input = input('Enter Location ID, Model and k:')
    start_time = time.time()
    input_location_id = int(user_input.split(' ')[0])
    input_model = user_input.split(' ')[1]
    input_k = int(user_input.split(' ')[2])

    # Mapping Input Location ID to Location Name
    devset_topic_file_loc = devset_dir + 'devset_topics.xml'
    output = []
    with open(devset_topic_file_loc) as file:
        soup = BeautifulSoup(file, 'html.parser')
        other_loc_vd_fnames = []
    for topic in soup.find_all('topic'):
        location_id = int(topic.number.contents[0])
        location_name = topic.title.contents[0]
        if location_id == input_location_id:
            input_loc_vd_fname = loc_data_dir + location_name + ' ' + input_model + '.csv'
        else:
            other_loc_vd_fnames.append(loc_data_dir + location_name + ' ' + input_model + '.csv')
            output.append([topic.title.contents[0]])

    # Checking for location ID validity
    if 'input_loc_vd_fname' not in locals():
        print('Invalid Image ID Entered. Please enter a valid Image ID')
        invalid_input_flag = True
    else:
        # Calculating Euclidean Distance
        if '3x3' in input_loc_vd_fname:
            k_output = calculate_3x3_distance(input_loc_vd_fname, other_loc_vd_fnames, output,
                                              input_k)
        else:
            k_output = calculate_distance(input_loc_vd_fname, other_loc_vd_fnames, output,
                                          input_k)
        #Printing Output
        for data in k_output:
            print(data)
        end_time = time.time()
        print('Program Execution Time : ', end_time - start_time)

    if invalid_input_flag is True:
        print('-' * 25)
        time.sleep(0.8)
        main()


if __name__ == '__main__':
    main()
