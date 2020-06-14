import csv

from api.models import Estate
import pandas as pd
import numpy as np
from scipy import spatial


def check2EstateSameLocation(d1, d2):
    for t in range(0, 5):
        if d1[t] != d2[t]:
            return False
        return True

table = []
idIndex = {}
estates = Estate.objects.all()
for idx in range(0, len(estates)):
    item = []
    idIndex[idx] = estates[idx].id
    item.append(estates[idx].estateType.get_id())
    item.append(estates[idx].province.get_id())
    item.append(estates[idx].district.get_id())
    item.append(estates[idx].transaction.get_id())
    item.append(estates[idx].numberOfRoom)
    item.append(estates[idx].price)
    item.append(estates[idx].area)
    table.append(item)

data = np.asarray(table)
max_in_col = np.amax(data, axis=0)
start = 4
data[:, start] = np.true_divide(data[:, start], max_in_col[start])
data[:, start + 1] = np.true_divide(data[:, start + 1], max_in_col[start + 1])
data[:, start + 2] = np.true_divide(data[:, start + 2], max_in_col[start + 2])

n_estate = len(table)
sim_matrix = np.zeros(shape=(n_estate, n_estate))
for i in range(0, n_estate):
    for j in range(0, n_estate):
        if check2EstateSameLocation(data[i], data[j]):
            dis = 1 - spatial.distance.cosine(data[i], data[j])
        else:
            dis = -float('inf')
        sim_matrix[i, j] = dis

pd.DataFrame(sim_matrix, dtype=np.float).to_csv("recommender/sim_matrix.csv", index=None, header=None)
with open('recommender/idIndex.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in idIndex.items():
        writer.writerow([key, value])
