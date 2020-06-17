import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


class CF(object):
    """
    Description: ......
    """

    def __init__(self, Y_data, user_index, item_index, k, dist_func=cosine_similarity, uuCF=1):
        self.uuCF = uuCF  # user-user (1) or item-item (0) CF
        self.Y_data = Y_data  # if uuCF else Y_data[:, [1, 0, 2]]
        self.user_index = user_index
        self.item_index = item_index
        self.k = k  # number of neighbor points
        self.dist_func = dist_func
        self.Ybar_data = None
        self.S = None
        # number of users and items. Remember to add 1 since id starts from 0
        self.n_items, self.n_users = Y_data.shape  # int(np.max(self.Y_data[:, 0])) + 1

    def add(self, new_data):
        """
            Update Y_data matrix when new ratings come.
            For simplicity, suppose that there is no new user or item.
        """
        m_user_index = self.check_user_exist(new_data[0])
        m_item_index = self.check_item_exist(new_data[1])
        rating = new_data[2]
        if m_item_index == -1 and m_user_index == -1:
            self.Y_data = np.lib.pad(self.Y_data, ((0, 1), (0, 1)), 'constant', constant_values=(-1))
            self.n_items, self.n_users = self.Y_data.shape
            self.Y_data[self.n_items - 1, self.n_users - 1] = rating

        if m_item_index != -1 and m_user_index == -1:
            self.Y_data = np.lib.pad(self.Y_data, ((0, 0), (0, 1)), 'constant', constant_values=(-1))
            self.n_items, self.n_users = self.Y_data.shape
            self.Y_data[m_item_index, self.n_users - 1] = rating

        if m_item_index == -1 and m_user_index != -1:
            self.Y_data = np.lib.pad(self.Y_data, ((0, 1), (0, 0)), 'constant', constant_values=(-1))
            self.n_items, self.n_users = self.Y_data.shape
            self.Y_data[self.n_items - 1, m_user_index] = rating

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

    def __pred(self, u, i, normalized=1):
        """
        predict the rating of user u for item i (normalized)
        if you need the un
        """
        # Step 1: find all users who rated i
        ids = np.where(self.Y_data[:, 1] == i)[0].astype(np.int32)
        # Step 2:
        users_rated_i = (self.Y_data[ids, 0]).astype(np.int32)
        # Step 3: find similarity btw the current user and others
        # who already rated i
        sim = self.S[u, users_rated_i]
        # Step 4: find the k most similarity users
        a = np.argsort(sim)[-self.k:]
        # and the corresponding similarity levels
        nearest_s = sim[a]
        # How did each of 'near' users rated item i
        r = self.Ybar[i, users_rated_i[a]]
        if normalized:
            # add a small number, for instance, 1e-8, to avoid dividing by 0
            return (r * nearest_s)[0] / (np.abs(nearest_s).sum() + 1e-8)

        return (r * nearest_s)[0] / (np.abs(nearest_s).sum() + 1e-8) + self.mu[u]

    def pred(self, u, i, normalized=1):
        """
        predict the rating of user u for item i (normalized)
        if you need the un
        """
        if self.uuCF: return self.__pred(u, i, normalize)
        return self.__pred(i, u, normalize)

    def check_user_exist(self, user_id):
        """
        If exist return index, else return -1
        """
        for key, value in self.user_index.items():
            if user_id == value:
                return key
        return -1

    def check_item_exist(self, item_id):
        """
        If exist return index, else return -1
        """
        for key, value in self.item_index.items():
            if item_id == value:
                return key
        return -1
