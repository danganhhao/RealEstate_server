import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


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
            Update Y_data matrix when new ratings come.
            For simplicity, suppose that there is no new user or item.
        """
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
        self.Ybar_data = self.Y_data.copy()
        for i in range(self.Ybar_data.shape[0]):
            mean_value = sum(y for y in self.Ybar_data[i] if y != -1) / (
                    len(self.Ybar_data[i]) - np.count_nonzero(self.Ybar_data[i] == -1))
            for j in range(len(self.Ybar_data[i])):
                if self.Ybar_data[i][j] != -1:
                    self.Ybar_data[i][j] -= mean_value
                else:
                    self.Ybar_data[i][j] = 0

    def similarity(self):
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
        predict the rating of user u for item i (normalized)
        if you need the un
        """
        # Step 1: find all item which rated by user
        c_user_rating = self.Ybar_data[:, c_user_index]
        list_item_idx_rated = np.where(c_user_rating != 0)[0]  # list item_index, which rated by c_user
        # Xác định item được rated bởi những user nào
        similarities_item = self.S[c_item_index][list_item_idx_rated]  # Xác định similarities của i1 với các item khác
        # find the k most similarity items
        a = np.argsort(similarities_item)[-self.k:]
        # # and the corresponding similarity levels
        nearest_s = similarities_item[a]
        # # How did each of 'near' users rated item i
        r = c_user_rating[list_item_idx_rated[a]]
        res = (r * nearest_s).sum() / (np.abs(nearest_s).sum() + 1e-8)
        return res

    def fit_Ybar_data(self):
        self.Ybar_normalized = self.Ybar_data.copy()
        for m_item in range(self.Ybar_data.shape[0]):
            for m_user in range(self.Ybar_data.shape[1]):
                if self.Ybar_data[m_item, m_user] == 0:
                    self.Ybar_normalized[m_item, m_user] = self.pred(m_item, m_user)

    def export_normalized(self):
        pd.DataFrame(self.Ybar_normalized, dtype=np.float).to_csv("cf_data_normalized.csv", index=None, header=None)
        with open("cf_item_id_index.txt", 'w') as f:
            for item in self.item_index:
                f.write("%s\n" % item)
        with open("cf_user_id_index.txt", 'w') as f:
            for user in self.user_index:
                f.write("%s\n" % user)

    def export_added_rating(self):
        pd.DataFrame(self.Y_data, dtype=np.float).to_csv("cf_data.csv", index=None, header=None)
        with open("cf_item_id_index.txt", 'w') as f:
            for item in self.item_index:
                f.write("%s\n" % item)
        with open("cf_user_id_index.txt", 'w') as f:
            for user in self.user_index:
                f.write("%s\n" % user)

    def get_recommend_for_user(self, user_id):
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


def read_data_for_recommend(data_origin_file_name, data_normalized_file_name, item_id_index_file_name, user_id_index_file_name):
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


def get_recommend(user_id):
    data_origin, data_normalized, item_id_index, user_id_index = read_data_for_recommend('cf_data.csv', 'cf_data_normalized.csv', 'cf_item_id_index.txt', 'cf_user_id_index.txt')
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
        return np_item_id_index[res]


def add_rating_data(new_data):
    """
        Update Y_data matrix when new ratings come.
        For simplicity, suppose that there is no new user or item.
    """
    data, item_id_index, user_id_index = read_data_for_train('cf_data.csv', 'cf_item_id_index.txt',
                                                             'cf_user_id_index.txt')
    rs = CF(data, user_id_index, item_id_index, 2)
    rs.add(new_data)
    rs.export_added_rating()


def train():
    data, item_id_index, user_id_index = read_data_for_train('cf_data.csv', 'cf_item_id_index.txt', 'cf_user_id_index.txt')
    rs = CF(data, user_id_index, item_id_index, 2)
    rs.fit()
    rs.export_normalized()

# train()
add_rating_data([200, 100, 56.3333333])
print(get_recommend(201))
# data = np.zeros(shape=(5, 7))
# data[0] = [5, 5, 2, 0, 1, -1, -1]
# data[1] = [4, -1, -1, 0, -1, 2, -1]
# data[2] = [-1, 4, 1, -1, -1, 1, 1]
# data[3] = [2, 2, 3, 4, 4, -1, 4]
# data[4] = [2, 0, 4, -1, -1, -1, 5]
#
# item_id_index = {0: 100, 1: 101, 2: 102, 3: 103, 4: 104}
# user_id_index = {0: 200, 1: 201, 2: 202, 3: 203, 4: 204, 5: 205, 6: 206}
#
# rs = CF(data, user_id_index, item_id_index, 2)
# rs.fit()
# rs.fit_Ybar_data()
# rs.print()
# print(rs.get_recommend_for_user(201))
