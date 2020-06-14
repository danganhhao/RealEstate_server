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


def get_similar_items(item_id, number):
    idIndex = read_idIndex_file("idIndex.csv")
    sim_matrix = read_sim_matrix_file("sim_matrix.csv")
    # idIndex = read_idIndex_file("recommender/idIndex.csv")
    # sim_matrix = read_sim_matrix_file("recommender/sim_matrix.csv")
    index = int([k for k, v in idIndex.items() if v == item_id][0])
    ind = sim_matrix[index].argsort()[-number:][::-1]
    res = []
    for i in ind:
        res.append(idIndex[str(i)])
    return ind


if __name__ == "__main__":
    get_similar_items('68', 5)

