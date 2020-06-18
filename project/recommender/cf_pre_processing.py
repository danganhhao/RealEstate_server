from api.models import Estate
from user.models import User
import numpy as np
import pandas as pd


def get_estates():
    return Estate.objects.all()


def get_users():
    return User.objects.all()


def get_matrix_data():
    # Initialize data matrix structure
    estates = get_estates()
    users = get_users()
    n_estate = len(estates)
    n_user = len(users)
    data = np.zeros(shape=(n_estate, n_user))
    item_id_index = []
    user_id_index = []
    for j in range(n_user):
        user_id_index.append(users[j].id)
    for i in range(n_estate):
        for j in range(n_user):
            data[i][j] = -1
        item_id_index.append(estates[i].id)
    return data, item_id_index, user_id_index


def export_data(data, item_id_index, user_id_index):
    pd.DataFrame(data, dtype=np.float).to_csv("recommender/cf_data.csv", index=None, header=None)
    with open("recommender/cf_item_id_index.txt", 'w') as f:
        for item in item_id_index:
            f.write("%s\n" % item)
    with open("recommender/cf_user_id_index.txt", 'w') as f:
        for user in user_id_index:
            f.write("%s\n" % user)


data, item_id_index, user_id_index = get_matrix_data()
export_data(data, item_id_index, user_id_index)
# data = np.zeros(shape=(5, 7))
# data[0] = [5, 5, 2, 0, 1, -1, -1]
# data[1] = [4, -1, -1, 0, -1, 2, -1]
# data[2] = [-1, 4, 1, -1, -1, 1, 1]
# data[3] = [2, 2, 3, 4, 4, -1, 4]
# data[4] = [2, 0, 4, -1, -1, -1, 5]
# item_id_index = [100, 101, 102, 103, 104]
# user_id_index = [200, 201, 202, 203, 204, 205, 206]
