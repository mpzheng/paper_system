def Diversity(lzs=[]):
    n = len(lzs[0])
    diversity = 0
    i = 0
    while i < len(lzs):
        j = 0
        diversity_i = 0
        while j < len(lzs):
            if j == i:
                j += 1
                continue
            # print(i, j)
            sum = 0
            for group in range(n):
                # print(set(lzs[i][group][0]['teachers']).intersection(set(lzs[j][group][0]['teachers'])))
                len_max = max(len(list(lzs[i][group][0].keys())[0:-1]), len(list(lzs[j][group][0].keys())[0:-1]))
                # print(len_max)
                # print(list(lzs[i][group][0].keys())[0:-1], list(lzs[j][group][0].keys())[0:-1])
                sum += (len_max - len(set(lzs[i][group][0]['teachers']).intersection(set(lzs[j][group][0]['teachers'])))) / len_max
            sum = sum / n
            # print('两个粒子差异性', sum)
            diversity_i += sum
            j += 1
            if i == len(lzs):
                break
        diversity += diversity_i / (len(lzs)-1)
        # print('一个粒子与总体的差异性', diversity_i / (len(lzs)-1))
        i += 1
    # print("diversity", diversity/len(lzs))
    return diversity/len(lzs)

# def Diversity(lzs=[]):
#     diversity = 0
#     i = 0
#     n = len(lzs[0])
#     # print(lzs[0][0])
#     while i < len(lzs):
#         j = 0
#         diversity_i = 0
#         while j < len(lzs):
#             if j == i:
#                 j += 1
#                 continue
#             # print(i, j)
#             sum = 0
#
#             for group in range(n):
#                 # print(lzs[i][group][0])
#                 # print(set(lzs[i][group][0]['teachers']).intersection(set(lzs[j][group][0]['teachers'])))
#                 len_max = max(len(lzs[i][group][0]['teachers']),len(lzs[i][group][0]['teachers']))
#                 sum += (len_max - len(set(lzs[i][group][0]['teachers']).intersection(set(lzs[j][group][0]['teachers'])))) / len_max
#             # print(111111)
#             # print(n)
#             sum = sum / n
#             # print('两个粒子差异性', sum)
#             diversity_i += sum
#             j += 1
#             if i == len(lzs):
#                 break
#         diversity += diversity_i / (len(lzs)-1)
#         # print('一个粒子与总体的差异性', diversity_i / (len(lzs)-1))
#         i += 1
#     # print("diversity", diversity/len(lzs))
#     return diversity/len(lzs)
