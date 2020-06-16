import csv

import pandas as pd
import numpy as np


def load_data(file_name):
    data = pd.read_csv(file_name, header=None)
    return data


def export_csv(data, file_name):
    pd.DataFrame(data, dtype=np.float).to_csv(file_name, index=None, header=None)


def read_idIndex_file(file_name):
    with open(file_name) as csv_file:
        reader = csv.reader(csv_file)
        idIndex = dict(reader)
    return idIndex


def read_sim_matrix_file(file_name):
    data = pd.read_csv(file_name, header=None, float_precision='round_trip')
    return data


# def get_similar_items(item_id, number):
#     idIndex = read_idIndex_file("idIndex.csv")
#     sim_matrix = read_sim_matrix_file("sim_matrix.csv")
#     # idIndex = read_idIndex_file("recommender/idIndex.csv")
#     # sim_matrix = read_sim_matrix_file("recommender/sim_matrix.csv")
#     index = int([k for k, v in idIndex.items() if v == item_id][0])
#     ind = sim_matrix[index].argsort()[:number]
#     res = []
#     for i in ind:
#         res.append(idIndex[str(i)])
#     return res
#

def get_estate_info(item_id):
    """
    get data from server and
    return [province_id, district_id, estate_type, transaction_type] of estate
    """
    return [1,1,1,1]


def get_whole_sim_matrix_from_csv():
    return {}


def get_sim_matrix(estate_location_info):
    """
    estate_location_info: [province_id, district_id, estate_type, transaction_type]
    return: {sim_matrix: 2D array, list_estate_id: []}
    """
    whole_sim_matrix = get_whole_sim_matrix_from_csv()
    province_id = estate_location_info[0]
    district_id = estate_location_info[1]
    estate_type = estate_location_info[2]
    transaction_type = estate_location_info[3]
    return whole_sim_matrix[province_id][district_id][estate_type][transaction_type]

def get_similar_items(item_id, k = 5):
    res = []
    estate_location_info = get_estate_info(item_id)
    sim_matrix_object = get_sim_matrix(estate_location_info)
    sim_matrix = sim_matrix_object["sim_matrix"]
    id_index = sim_matrix_object["list_estate_id"]
    # TODO: select most similar estate
    return res

if __name__ == "__main__":
    res = get_similar_items('68', 5)
    print('res = ', res)

