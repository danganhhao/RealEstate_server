from api.models import Estate
import numpy as np

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
    item = [None] * 8
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
        estate_in_array = convert_estate_to_array(estatesData[i])
        province_id = estate_in_array[PROVINCE_IDX]
        district_id = estate_in_array[DISTRICT_IDX]
        estate_type = estate_in_array[ESTATE_TYPE_IDX]
        transaction_type = estate_in_array[TRANSACTION_IDX]
        if province_id not in res:
            res[province_id] = {}
        if district_id not in res[province_id]:
            res[province_id][district_id] = {}
        if estate_type not in res[province_id][district_id]:
            res[province_id][district_id][estate_type] = {}
        if transaction_type not in res[province_id][district_id][estate_type]:
            res[province_id][district_id][estate_type][transaction_type] = []
        res[province_id][district_id][estate_type][transaction_type].append(
            [estate_in_array[ID_IDX], estate_in_array[NUM_OF_ROOM_IDX], estate_in_array[PRICE_IDX],
             estate_in_array[AREA_IDX]])
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
    with open('sim_matrix_data.txt', 'w') as f:
        print(estatesByLocation, file=f)


# save_object_sim_data_to_file({3: {10: 11}})

print("\n[Start get data from server]\n")
estatesData = get_estates_from_server()
print("\n------- Done ------------\n")

print("\n[Arrange estate to group]\n")
estatesByLocation = arrange_estate_to_group(estatesData)
print("\n------- Done ------------\n")
# print('estatesByLocation', estatesByLocation)

# structure of estatesByLocation:
# {
#     1: {                            //provinceId
#         101: {                      //districtId
#             4: {                    //estateType
#                 0: [                //transactionType
#                     [10001, 0, 20000, 8],  //[id, numRoom, price, area]
#                     [10002, 0, 20000, 8],
#                 ]
#             }
#         }
#     }
#     .
#     .
# }

print("\n[Calc sim matrix]\n")
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
                estatesByLocation[provinceId][districtId][estateType][transactionType] = {"sim_matrix": simMatrix,"list_estate_id": listEstateIdSameLocation}

print("\n------- Done ------------\n")

print("\n[Save to file]\n")
save_object_sim_data_to_file(estatesByLocation)
print("\n------- Done ------------\n")

# structure of estatesByLocation after process:
# {
#     1: {                            //provinceId
#         101: {                      //districtId
#             4: {                    //estateType
#                 0: {                //transactionType
#                     "sim_matrix": 2D array,
#                     "list_estate_id": array, list estate id in this location
#                 }
#             }
#         }
#     }
#     .
#     .
# }
#
