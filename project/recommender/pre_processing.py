import csv
import math

from api.models import Estate
import pandas as pd
import numpy as np
from scipy import spatial

ID_IDX = 0
ESTATE_TYPE_IDX = ID_IDX + 1
PROVINCE_IDX = ESTATE_TYPE_IDX + 1
DISTRICT_IDX = PROVINCE_IDX + 1
TRANSACTION_IDX = DISTRICT_IDX + 1

NUM_OF_ROOM_IDX = TRANSACTION_IDX + 1
PRICE_IDX = NUM_OF_ROOM_IDX + 1
AREA_IDX = PRICE_IDX + 1


def check2EstateSameLocation(d1, d2):
    for t in range(0, 4):
        if d1[t] != d2[t]:
            return False
        return True


def euclid_distance(v1, v2):
    l = len(v1)
    sum = 0
    for i in range(0, l):
        sum += (v1[i] - v2[i]) * (v1[i] - v2[i])
    return np.math.sqrt(sum)


def get_estates_from_server():
    return Estate.objects.all()


def convert_estate_to_array(estate):
    item = [None] * (AREA_IDX + 1)
    item[ID_IDX] = estate.id
    item[ESTATE_TYPE_IDX] = estate.estateType.get_id()
    item[PROVINCE_IDX] = estate.province.get_id()
    item[DISTRICT_IDX] = estate.district.get_id()
    item[TRANSACTION_IDX] = estate.transaction.get_id()
    item[NUM_OF_ROOM_IDX] = estate.numberOfRoom
    item[PRICE_IDX] = estate.price
    item[AREA_IDX] = estate.area
    return item


def arrange_estate_to_group(estatesData):
    res = {}
    n_estate = len(estatesData)
    for i in range(0, n_estate):
        estateInArray = convert_estate_to_array(estatesData[i])

        provinceId = estateInArray[PROVINCE_IDX]
        districtId = estateInArray[DISTRICT_IDX]
        estateType = estateInArray[ESTATE_TYPE_IDX]
        transactionType = estateInArray[TRANSACTION_IDX]
        if provinceId not in res:
            res[provinceId] = {}

        if districtId not in res[provinceId]:
            res[provinceId][districtId] = {}

        if estateType not in res[provinceId][districtId]:
            res[provinceId][districtId][estateType] = {}

        if transactionType not in res[provinceId][districtId][estateType]:
            res[provinceId][districtId][estateType][transactionType] = []

        res[provinceId][districtId][estateType][transactionType].append(
            [
                estateInArray[ID_IDX],
                estateInArray[NUM_OF_ROOM_IDX],
                estateInArray[PRICE_IDX],
                estateInArray[AREA_IDX],
            ]
        )

    return res


def get_list_estate_id(estateArraySameLocation):
    res = []
    for i in range(0, len(estateArraySameLocation)):
        res.append(estateArraySameLocation[i].pop(0))
    return res


def calc_sim_matrix(listEstate):
    n_estate = len(listEstate)
    sim_matrix = np.zeros(shape=(n_estate, n_estate))
    for i in range(0, n_estate):
        for j in range(0, n_estate):
            dis = euclid_distance(listEstate[i], listEstate[j])
            sim_matrix[i, j] = dis
    return sim_matrix


def save_object_sim_data_to_file(estatesByLocation):
    # TODO: save object to txt file
    pass


estatesData = get_estates_from_server()
estatesByLocation = arrange_estate_to_group(estatesData)

"""
structure of estatesByLocation:
{
    1: {                            //provinceId
        101: {                      //districtId
            4: {                    //estateType
                0: [                //transactionType
                    [10001, 0, 20000, 8],  //[id, numRoom, price, area]
                    [10002, 0, 20000, 8],
                ]            
            }  
        }
    }
    .
    .
}
"""

for provinceId in estatesByLocation:
    estateInProvince = estatesByLocation[provinceId]
    for districtId in estateInProvince:
        estateInDistrict = estateInProvince[districtId]
        for estateType in estateInDistrict:
            estateSameType = estateInDistrict[estateType]
            for transactionType in estateSameType:
                estateArraySameLocation = estateSameType[transactionType]  # [[id, numRoom, price, area]]

                listEstateIdSameLocation = get_list_estate_id(estateArraySameLocation)  # pop first element of each estate
                simMatrix = calc_sim_matrix(estateArraySameLocation)
                estateSameType[transactionType] = {
                    "sim_matrix": simMatrix,
                    "list_estate_id": listEstateIdSameLocation
                }

save_object_sim_data_to_file(estatesByLocation)
"""
structure of estatesByLocation after process:
{
    1: {                            //provinceId
        101: {                      //districtId
            4: {                    //estateType
                0: {                //transactionType
                    "sim_matrix": 2D array,
                    "list_estate_id": array, list estate id in this location
                }            
            }  
        }
    }
    .
    .
}
"""
#
# print('start pre_processing')
# table = []
# idIndex = {}
# estates = Estate.objects.all()
# for idx in range(0, len(estates)):
#     item = [None] * (AREA_IDX + 1)
#     item[ID_IDX] = estates[idx].id
#     item[ESTATE_TYPE_IDX] = estates[idx].estateType.get_id()
#     item[PROVINCE_IDX] = estates[idx].province.get_id()
#     item[DISTRICT_IDX] = estates[idx].district.get_id()
#     item[TRANSACTION_IDX] = estates[idx].transaction.get_id()
#     item[NUM_OF_ROOM_IDX] = estates[idx].numberOfRoom
#     item[PRICE_IDX] = estates[idx].price
#     item[AREA_IDX] = estates[idx].area
#     table.append(item)
#
# data = np.asarray(table)
# max_in_col = np.amax(data, axis=0)
#
# data[:, NUM_OF_ROOM_IDX] = np.true_divide(data[:, NUM_OF_ROOM_IDX], max_in_col[NUM_OF_ROOM_IDX])
# data[:, AREA_IDX] = np.true_divide(data[:, AREA_IDX], max_in_col[AREA_IDX])
# data[:, PRICE_IDX] = np.true_divide(data[:, PRICE_IDX], max_in_col[PRICE_IDX])
#
# n_estate = len(table)
# sim_matrix_object = {}
#
# sim_matrix = np.zeros(shape=(n_estate, n_estate))
# for i in range(0, n_estate):
#     for j in range(0, n_estate):
#         if check2EstateSameLocation(data[i], data[j]):
#             provinceId = data[i][PROVINCE_IDX]
#             districtId = data[i][DISTRICT_IDX]
#             estateType = data[i][ESTATE_TYPE_IDX]
#             transactionType = data[i][TRANSACTION_IDX]
#             if provinceId not in sim_matrix_object:
#                 sim_matrix_object[provinceId] = {}
#
#             if districtId not in sim_matrix_object[provinceId]:
#                 sim_matrix_object[provinceId][districtId] = {}
#
#             if estateType not in sim_matrix_object[provinceId][districtId]:
#                 sim_matrix_object[provinceId][districtId][estateType] = {}
#
#             if transactionType not in sim_matrix_object[provinceId][districtId][estateType]:
#                 sim_matrix_object[provinceId][districtId][estateType][transactionType] = []
#
#             # dis = spatial.distance.cosine(data[i], data[j])
#             dis = euclid_distance(data[i], data[j])
#         else:
#             dis = float('inf')
#         sim_matrix[i, j] = dis
#
# pd.DataFrame(sim_matrix, dtype=np.float).to_csv("recommender/sim_matrix.csv", index=None, header=None)
# with open('recommender/idIndex.csv', 'w') as csv_file:
#     writer = csv.writer(csv_file)
#     for key, value in idIndex.items():
#         writer.writerow([key, value])
