import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from user.helper.string import ITEMS_PER_PAGE

FILE_PATH_CF_DATA = "recommender/cf_data.csv"
FILE_PATH_CF_DATA_NORMALIZED = "recommender/cf_data_normalized.csv"
FILE_PATH_CF_ITEM_ID_INDEX = "recommender/cf_item_id_index.txt"
FILE_PATH_CF_USER_ID_INDEX = "recommender/cf_user_id_index.txt"


class CF(object):
    """
    Description: ......
    """

    def __init__(self, Y_data, user_index, item_index, k, dist_func=cosine_similarity):
        self.Y_data = Y_data  # if uuCF else Y_data[:, [1, 0, 2]]
        self.user_index = user_index
        self.item_index = item_index
        self.k = k  # number of neighbor points
        self.dist_func = dist_func
        self.Ybar_data = None
        self.Ybar_normalized = None
        self.S = None
        self.n_items, self.n_users = Y_data.shape  # int(np.max(self.Y_data[:, 0])) + 1

    def add(self, new_data):
        """
            Param: new_data is a list (new_data = [user_id, item_id, rating])
            Update Y_data matrix when new ratings come.
            Update item_index, user_index if have new user/item rating.
        """
        self.Y_data = self.Y_data.to_numpy()
        user_id = new_data[0]
        item_id = new_data[1]
        rating = new_data[2]
        m_user_index = self.check_user_exist(user_id)
        m_item_index = self.check_item_exist(item_id)
        if m_item_index == -1 and m_user_index == -1:
            self.Y_data = np.lib.pad(self.Y_data, ((0, 1), (0, 1)), 'constant', constant_values=(-1))
            self.n_items, self.n_users = self.Y_data.shape
            self.Y_data[self.n_items - 1, self.n_users - 1] = rating
            self.item_index.append(item_id)
            self.user_index.append(user_id)
        if m_item_index != -1 and m_user_index == -1:
            self.Y_data = np.lib.pad(self.Y_data, ((0, 0), (0, 1)), 'constant', constant_values=(-1))
            self.n_items, self.n_users = self.Y_data.shape
            self.Y_data[m_item_index, self.n_users - 1] = rating
            self.user_index.append(user_id)

        if m_item_index == -1 and m_user_index != -1:
            self.Y_data = np.lib.pad(self.Y_data, ((0, 1), (0, 0)), 'constant', constant_values=(-1))
            self.n_items, self.n_users = self.Y_data.shape
            self.Y_data[self.n_items - 1, m_user_index] = rating
            self.item_index.append(item_id)

        if m_item_index != -1 and m_user_index != -1:
            self.Y_data[m_item_index, m_user_index] = rating

    def normalize_Y(self):
        """
            Normalize origin matrix to Y_bar_data
        """
        self.Y_data = self.Y_data.to_numpy()
        self.Ybar_data = self.Y_data.copy()
        for i in range(self.Ybar_data.shape[0]):
            temp = (len(self.Ybar_data[i]) - np.count_nonzero(self.Ybar_data[i] == -1))
            if temp != 0 and temp != 1:
                mean_value = sum(y for y in self.Ybar_data[i] if y != -1) / temp
            elif temp == 1:
                mean_value = 2.5
            else:
                mean_value = 0
            for j in range(len(self.Ybar_data[i])):
                if self.Ybar_data[i][j] != -1:
                    self.Ybar_data[i][j] -= mean_value
                else:
                    self.Ybar_data[i][j] = 0

    def similarity(self):
        """
            Calculate item-item similarity matrix S
        """
        self.S = self.dist_func(self.Ybar_data, self.Ybar_data)

    def refresh(self):
        """
        Normalize data and calculate similarity matrix again (after
        some few ratings added)
        """
        self.normalize_Y()
        self.similarity()

    def fit(self):
        self.refresh()
        self.fit_Ybar_data()

    def pred(self, c_item_index, c_user_index):
        """
            predict the rating of item i, which rated by user u (normalized)
        """
        # Step 1: find all item which rated by user
        c_user_rating_value = self.Ybar_data[:, c_user_index]
        c_user_rating = self.Y_data[:, c_user_index]
        list_item_idx_rated = np.where(c_user_rating != -1)[0]  # list item_index, which rated by c_user
        # Xác định item được rated bởi những user nào
        similarities_item = self.S[c_item_index][list_item_idx_rated]  # Xác định similarities của i1 với các item khác
        # find the k most similarity items
        a = np.argsort(similarities_item)[-self.k:]
        # # and the corresponding similarity levels
        nearest_s = similarities_item[a]
        # # How did each of 'near' users rated item i
        r = c_user_rating_value[list_item_idx_rated[a]]
        res = (r * nearest_s).sum() / (np.abs(nearest_s).sum() + 1e-8)
        return res

    def fit_Ybar_data(self):
        """
            Fit Ybar_matrix with predict value.
            Storage to Ybar_normalized
        """
        self.Ybar_normalized = self.Ybar_data.copy()
        for m_item in range(self.Ybar_data.shape[0]):
            for m_user in range(self.Ybar_data.shape[1]):
                if self.Ybar_data[m_item, m_user] == 0:
                    self.Ybar_normalized[m_item, m_user] = self.pred(m_item, m_user)

    def export_normalized(self):
        """
            Export Ybar_normalized matrix to csv file.
            When want to get recommend estates for special user, you load this file and handle.
        """
        pd.DataFrame(self.Ybar_normalized, dtype=np.float).to_csv(FILE_PATH_CF_DATA_NORMALIZED, index=None, header=None)
        with open(FILE_PATH_CF_ITEM_ID_INDEX, 'w') as f:
            for item in self.item_index:
                f.write("%s\n" % item)
        with open(FILE_PATH_CF_USER_ID_INDEX, 'w') as f:
            for user in self.user_index:
                f.write("%s\n" % user)

    def export_added_rating(self):
        """
            Export Y_data (base matrix) to csv file. This file only contain rating of all user.
        """
        pd.DataFrame(self.Y_data, dtype=np.float).to_csv(FILE_PATH_CF_DATA, index=None, header=None)
        with open(FILE_PATH_CF_ITEM_ID_INDEX, 'w') as f:
            for item in self.item_index:
                f.write("%s\n" % item)
        with open(FILE_PATH_CF_USER_ID_INDEX, 'w') as f:
            for user in self.user_index:
                f.write("%s\n" % user)

    def get_recommend_for_user(self, user_id):
        """
            Unused function
        """
        index = self.check_user_exist(user_id)
        res = []
        if index != -1:
            c_user_rating = self.Ybar_data[:, index]
            list_item_idx_rated = np.where(c_user_rating != 0)[0]
            list_rating = self.Ybar_normalized[:, index]
            for i in range(self.n_items):
                if i not in list_item_idx_rated and list_rating[i] > 0:
                    res.append(i)
            return self.item_index[res]

    def check_user_exist(self, user_id):
        """
        If exist return index, else return -1
        """
        try:
            return self.user_index.index(user_id)
        except:
            return -1

    def check_item_exist(self, item_id):
        """
        If exist return index, else return -1
        """
        try:
            return self.item_index.index(item_id)
        except:
            return -1

    def print(self):
        print("Y_data", self.Y_data)
        print("Ybar_data", self.Ybar_data)
        print("Ybar_normalized", self.Ybar_normalized)
        print("S_matrix", self.S)


def read_data_for_train(data_file_name, item_id_index_file_name, user_id_index_file_name):
    """
        Load data to do train model.
    """
    m_data = pd.read_csv(data_file_name, header=None, float_precision='round_trip')
    with open(item_id_index_file_name, 'r') as f:
        m_item_id_index = f.readlines()
        m_item_id_index = list(map(int, m_item_id_index))
    with open(user_id_index_file_name, 'r') as f:
        m_user_id_index = f.readlines()
        m_user_id_index = list(map(int, m_user_id_index))
    return m_data, m_item_id_index, m_user_id_index
    # data = np.zeros(shape=(5, 7))
    # data[0] = [5, 5, 2, 0, 1, -1, -1]
    # data[1] = [4, -1, -1, 0, -1, 2, -1]
    # data[2] = [-1, 4, 1, -1, -1, 1, 1]
    # data[3] = [2, 2, 3, 4, 4, -1, 4]
    # data[4] = [2, 0, 4, -1, -1, -1, 5]
    #
    # item_id_index = [100, 101, 102, 103, 104]
    # user_id_index = [200, 201, 202, 203, 204, 205, 206]
    # return data, item_id_index, user_id_index


def read_data_for_recommend(data_origin_file_name, data_normalized_file_name, item_id_index_file_name,
                            user_id_index_file_name):
    """
        Load data to do get recommend for user.
    """
    m_data_origin_file_name = pd.read_csv(data_origin_file_name, header=None, float_precision='round_trip')
    m_data_normalized_file_name = pd.read_csv(data_normalized_file_name, header=None, float_precision='round_trip')
    with open(item_id_index_file_name, 'r') as f:
        m_item_id_index = f.readlines()
        m_item_id_index = list(map(int, m_item_id_index))
    with open(user_id_index_file_name, 'r') as f:
        m_user_id_index = f.readlines()
        m_user_id_index = list(map(int, m_user_id_index))
    return m_data_origin_file_name, m_data_normalized_file_name, m_item_id_index, m_user_id_index


def check_user_exist_for_recommend(list_user, user_id):
    """
    If exist return index, else return -1
    """
    try:
        return list_user.index(user_id)
    except:
        return -1


def get_top_popular_items(data_origin):
    times_rating_of_each_item = []
    total_users = data_origin.shape[1]
    for i in range(data_origin.shape[0]):
        temp = (len(data_origin.iloc[i]) - np.count_nonzero(data_origin.iloc[i] == -1.0))
        if temp != 0:
            mean_value = sum(y for y in data_origin.iloc[i] if y != -1.0) / temp
        else:
            mean_value = 0

        if mean_value >= 2.5:  # Chỉ chọn lọc những bất động sản có rating cao
            value = total_users - list(data_origin.iloc[i]).count(-1.0)  # tính số lượng rating của 1 bất động sản
            times_rating_of_each_item.append(value)
        else:
            times_rating_of_each_item.append(-1)
    list_index = np.argsort(times_rating_of_each_item)[-ITEMS_PER_PAGE:]  # get top
    return list_index


def get_recommend(user_id, isGetPopularItem=False):
    """
        Return list item_id, it recommend for user_id
    """
    data_origin, data_normalized, item_id_index, user_id_index = read_data_for_recommend(FILE_PATH_CF_DATA,
                                                                                         FILE_PATH_CF_DATA_NORMALIZED,
                                                                                         FILE_PATH_CF_ITEM_ID_INDEX,
                                                                                         FILE_PATH_CF_USER_ID_INDEX)
    index = check_user_exist_for_recommend(user_id_index, user_id)
    res = []
    if index != -1:
        np_item_id_index = np.asarray(item_id_index, dtype=np.int)
        c_user_rating = data_origin[index]
        list_item_idx_rated = np.where(c_user_rating != -1)[0]
        list_rating = data_normalized[index]
        for i in range(data_normalized.shape[0]):
            if i not in list_item_idx_rated and list_rating[i] > 0:
                res.append(i)
        if len(res) != 0:
            return np_item_id_index[res]
        if len(res) == 0 and isGetPopularItem:  # get popular item
            return get_top_popular_items(data_origin)
        return res

    else:
        if len(res) == 0 and isGetPopularItem:  # get popular item
            return get_top_popular_items(data_origin)


def add_rating_data(new_data):
    """
        Param: new_data is a list (new_data = [user_id, item_id, rating])
        Add data and export to Y_data (base_matrix) csv file
    """
    data, item_id_index, user_id_index = read_data_for_train(FILE_PATH_CF_DATA, FILE_PATH_CF_ITEM_ID_INDEX,
                                                             FILE_PATH_CF_USER_ID_INDEX)
    rs = CF(data, user_id_index, item_id_index, 2)
    rs.add(new_data)
    rs.export_added_rating()


def train():
    """
        Train models when have new information.
    """
    data, item_id_index, user_id_index = read_data_for_train(FILE_PATH_CF_DATA, FILE_PATH_CF_ITEM_ID_INDEX,
                                                             FILE_PATH_CF_USER_ID_INDEX)
    rs = CF(data, user_id_index, item_id_index, 2)
    rs.fit()
    rs.export_normalized()


train()
# add_rating_data([200, 100, 56.3333333])
# print(get_recommend(205))
