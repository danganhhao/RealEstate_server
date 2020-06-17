from api.models import Estate
from user.models import User
import numpy as np


def get_estates():
    return Estate.objects.all()


def get_users():
    return User.objects.all()


def get_matrix_data():
    # TODO: Initialize data matrix structure
    data = np.zeros(shape=(5, 7))
    data[0] = [5, 5, 2, 0, 1, -1, -1]
    data[1] = [4, -1, -1, 0, -1, 2, -1]
    data[2] = [-1, 4, 1, -1, -1, 1, 1]
    data[3] = [2, 2, 3, 4, 4, -1, 4]
    data[4] = [2, 0, 4, -1, -1, -1, 5]

    return data, {0: 100, 1: 101, 2: 102, 3: 103, 4: 104}, \
           {0: 200, 1: 201, 2: 202, 3: 203, 4: 204, 5: 205, 6: 206}
    # data, item_id_index, user_id_index


get_matrix_data()
