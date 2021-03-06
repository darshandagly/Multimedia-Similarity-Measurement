import pymongo as pm
import math
import os
import time


# Calculating  Cosine Similarity
def cosine_similarity(db_image_data, input_image_data, k, collection, model):
    cosine_sim_output = []
    for record in db_image_data:
        sumxx, sumxy, sumyy = 0, 0, 0
        v_mul = []
        y_square = 0
        for db_data in collection.find({'_id': record[0][0]}):
            for data in db_data['DATA']:
                y_square += data[model] * data[model]
        for i in range(1, len(input_image_data[1][1:]) + 1):
            x = input_image_data[1][i]
            y = record[1][i]
            sumxx += x * x
            sumyy += y * y
            sumxy += x * y
            v_mul.append(x * y)
        cosine_sim_output.append([record[0][0], sumxy / math.sqrt(sumxx * y_square), record[0], v_mul])
    cosine_sim_output = sorted(cosine_sim_output, key=lambda z: z[1], reverse=True)
    if k > len(cosine_sim_output):
        k = len(cosine_sim_output)
    for item in range(0, k):
        top_three_terms_list = []
        for item1 in sorted(zip(cosine_sim_output[item][3], cosine_sim_output[item][2][1:]), reverse=True)[:3]:
            top_three_terms_list.append(item1[1])
        del cosine_sim_output[item][2:]
        cosine_sim_output[item].append(top_three_terms_list)
        print(cosine_sim_output[item])


def main():
    start_time = time.time()
    # Connecting to Database and Creating Collection
    database_name = 'image_data'
    collection_name = 'image_text_descriptors'
    try:
        db_client = pm.MongoClient('localhost', 27017)
    except pm.errors.ConnectionFailure:
        print('Could not connect to the database. Please re-start the program!')
    db = db_client[database_name]
    collection = db[collection_name]

    # Loading data in MongoDB
    img_text_desc_path = os.getcwd() + '\dataset\desctxt\devset_textTermsPerImage.txt'
    with open(img_text_desc_path, 'r', encoding='UTF-8') as fileobject:
        for line in fileobject:
            data = line.split(' ')
            num = 1
            data_list = []
            while num < len(data) - 3:
                data_dict = {}
                data_dict['TERM'] = data[num].strip('\"')
                data_dict['TF'] = int(data[num + 1])
                data_dict['DF'] = int(data[num + 2])
                data_dict['TF-IDF'] = float(data[num + 3])
                num += 4
                data_list.append(data_dict)
            collection.insert_one({'_id': int(data[0]), 'DATA': data_list})

    # Taking user Input
    user_input = input('Please enter the image id, model and k : ')
    input_image_id = int(user_input.split(' ')[0])
    model = user_input.split(' ')[1]
    k = int(user_input.split(' ')[2])

    # Creating Input Image Vector
    input_image_data_terms = []
    input_image_data_freq = []
    for record in collection.find({'_id': input_image_id}).sort('DATA.TERM', pm.ASCENDING):
        input_image_data_terms.append(record['_id'])
        input_image_data_freq.append(record['_id'])
        for data in sorted(record['DATA'], key=lambda z: z['TERM']):
            input_image_data_terms.append(data['TERM'])
            input_image_data_freq.append(data[model])
    input_image_data = [input_image_data_terms, input_image_data_freq]

    # Creating a Vector of all other database images
    db_image_data = []
    for records in collection.find({'DATA.TERM': {'$in': input_image_data_terms[1:]}}):
        db_image_data_terms = []
        db_image_data_freq = []
        x = []
        db_image_data_terms.append(records['_id'])
        db_image_data_freq.append(records['_id'])
        for i in range(1, len(input_image_data_terms)):
            term_found = False
            for data in sorted(records['DATA'], key=lambda z: z['TERM']):
                if data['TERM'] == input_image_data_terms[i]:
                    db_image_data_terms.append(data['TERM'])
                    db_image_data_freq.append(data[model])
                    term_found = True
                    break
            if term_found is False:
                db_image_data_terms.append(0)
                db_image_data_freq.append(0)
        while len(db_image_data_terms) < len(input_image_data_terms):
            db_image_data_terms.append(0)
            db_image_data_freq.append(0)
        x.append(db_image_data_terms)
        x.append(db_image_data_freq)
        db_image_data.append(x)

    # Passing Input User Vector and Database User Vectors for Cosine Similarity Calculations
    cosine_similarity(db_image_data, input_image_data, k, collection, model)
    end_time = time.time()
    print('Execution Time : ',end_time-start_time)
    # Post Run Cleanup
    collection.drop()
    db_client.drop_database(database_name)


if __name__ == '__main__':
    main()
