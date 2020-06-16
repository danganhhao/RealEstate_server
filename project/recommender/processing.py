import numpy as np


def read_sim_matrix_file(file_name):
    file = open(file_name, "r")
    contents = file.read()
    dictionary = eval(contents)
    file.close()
    return dictionary


def get_sim_matrix(estate_location_info):
    """
    estate_location_info: [province_id, district_id, estate_type, transaction_type]
    return: {sim_matrix: 2D array, list_estate_id: []}
    """
    whole_sim_matrix = read_sim_matrix_file("sim_matrix_data.txt")
    province_id = estate_location_info[0]
    district_id = estate_location_info[1]
    estate_type = estate_location_info[2]
    transaction_type = estate_location_info[3]
    return whole_sim_matrix[province_id][district_id][estate_type][transaction_type]


def get_similar_items(item_id, item_info, k=5):
    sim_matrix_info = get_sim_matrix(item_info)
    sim_matrix = sim_matrix_info["sim_matrix"]
    id_index = sim_matrix_info["list_estate_id"]
    cur_id_index = id_index.index(item_id)
    ind = np.array(sim_matrix[cur_id_index]).argsort()[:k]
    id_index = np.asarray(id_index, dtype=np.int)
    result = id_index[ind]
    return result


if __name__ == "__main__":
    res = get_similar_items(483, [5, 71, 5, 6], 5)
    # print('res = ', res)
