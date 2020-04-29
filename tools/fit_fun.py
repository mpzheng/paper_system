
import pandas as pd
import math
import numpy as np
from tools import res_initial
'''

1.参与答辩的老师不能作为该老师指导学生所在组的答辩老师。
2.参与答辩学生的老师不作为该老师指导学生的评阅老师。
3.参与答辩的老师最多只能成为一次答辩老师。
4.每组的参与答辩的学生人数尽量相当。
5.每组的学生绩点分布要与所有学生绩点分布相近。


'''

def dist(group_scale, score_scale):
    sum = 0
    for i in range(5):
        sum += (score_scale[i] - group_scale[i]) ** 2
    return math.sqrt(sum)

def worst_f5(lz, score_scale, score_level_num, n):
    group_score_scale = [0, 0, 0, 0, 0]
    sum = 0
    bad_group_score = []
    for group in lz:
        for stu in list(group[0].values())[:-1]:
            sum += stu
    ave_stu = sum / len(lz)
    i = 0
    while i < n:
        for j in range(5):
            if score_level_num[j] > 0:
                if score_level_num[j] < ave_stu:
                    group_score_scale[j] += score_level_num[j]
                    ave_stu -= score_level_num[j]
                    score_level_num[j] = 0
                elif score_level_num[j] >= ave_stu:
                    tem = score_level_num[j]-ave_stu
                    group_score_scale[j] += ave_stu
                    score_level_num[j] = tem
                    ave_stu = 0
                    break
        ave_stu = sum / len(lz)
        for j in range(5):
            group_score_scale[j] = group_score_scale[j] / ave_stu
        bad_group_score.append(dist(group_score_scale, score_scale))
        group_score_scale = [0, 0, 0, 0, 0]
        i += 1
    return np.array(bad_group_score).mean()


def fit_1(lz, same_teacher=[]):
    for group in lz:  # 关于两个老师不能在同一组，若在同一组，则适应度无限大
        for teacher in group[0]["teachers"]:
            for test_teacher in group[0]["teachers"]:
                if test_teacher in res_initial.teacher_teacher[teacher]:
                    return -100
    p = 2
    for group in lz:  # 关于两个老师必须在同一组答辩，若不在同一组，则适应度无限大
        for teacher in group[0]["teachers"]:  ## 改动
            count = 0
            for s_t in same_teacher:
                p = 0
                if teacher in s_t:
                    p = 1
                    count += 1
                    for test_teacher in group[0]["teachers"]:
                        if test_teacher in s_t and test_teacher != teacher:
                            count += 1
                    if count != len(s_t):
                        return -100
                    else:
                        p = 2
    if p != 2:
        return -100

    return 0


def fit_2(res, id_teacher={}, id_score={}):
    # x为允许误差
    point = 0
    for group in res:
        for i in list(group[0].keys())[:-1]:
            while point < group[0][i]:
                if id_teacher[group[1][point]] == i:
                    return -100
                point += 1
    return 0


def fit_3(lz, id_teacher={}):
    dic = {}
    for i in list(set(id_teacher.values())):
        dic[i] = 0
    for group in lz:
        for tea in group[0]["teachers"]:
        # for tea in group[2]:
            if dic[tea] == 1:
                return -100
            else:
                dic[tea] = 1
    return 0

def fit_4(res):
    sum = 0
    for group in res:
        for stu in list(group[0].values())[:-1]:
        # for stu in group[0].values():
            sum += stu

    ave_stu = sum/len(res)
    # print("***{}***".format(ave_stu))

    total = 0
    for group in res:
        sum_1 = 0
        for stu in list(group[0].values())[:-1]:
        # for stu in group[0].values():
            sum_1 += stu
        # print(sum_1)
        total += abs(sum_1-ave_stu)
        # print(total)
    return total / (ave_stu * 2 * len(res))

def fit_5(lz, id_score={}, score_scale=[], n=0):
    lz_group_score = []
    score_level_num = [0, 0, 0, 0, 0]
    # print('id_score',id_score)
    for group in lz:
        group_score_scale = [0, 0, 0, 0, 0]
        for stu_id in group[1]:
            #             print(stu_id)
            if id_score[stu_id] < 2.0:
                group_score_scale[0] += 1
                score_level_num[0] += 1
            elif id_score[stu_id] < 2.5:
                group_score_scale[1] += 1
                score_level_num[1] += 1
            elif id_score[stu_id] < 3.0:
                group_score_scale[2] += 1
                score_level_num[2] += 1
            elif id_score[stu_id] < 3.5:
                group_score_scale[3] += 1
                score_level_num[3] += 1
            else:
                group_score_scale[4] += 1
                score_level_num[4] += 1
        for i in range(5):
            # if len(group[1])==0:
            #     print(lz)
            group_score_scale[i] = group_score_scale[i] / len(group[1])
        lz_group_score.append(dist(group_score_scale, score_scale))
    # print('new_f5:', np.array(lz_group_score).mean()/worst_f5(lz, score_scale, score_level_num, n))
    return np.array(lz_group_score).mean()/worst_f5(lz, score_scale, score_level_num, n)


def fit_all(lz, id_teacher, id_score, score_scale, n, s_teacher=[]):
    f1 = fit_1(lz, s_teacher)
    f2 = 0
    f3 = fit_3(lz, id_teacher)
    f4 = fit_4(lz)
    f5 = fit_5(lz, id_score, score_scale, n)
    sum = 0
    for i in lz:
        sum += len(i[1])

    # print(f1, "---", f2,"---", f3, "---", f4, "---", f5)
    # print('适应度：',f1+f2+f3+f4*0.5+f5*0.5)

    # print("学生数：",(1-f4)*0.5)
    # print("分布：",(1-f5)*0.5)
    #调整比重
    return f1+f2+f3+(1-f4)*0.5+(1-f5)*0.5

def show_fit(lz, id_teacher, id_score, score_scale, n, s_teacher=[]):
    f1 = fit_1(lz, s_teacher)
    f2 = 0
    f3 = fit_3(lz, id_teacher)
    f4 = fit_4(lz)
    f5 = fit_5(lz, id_score, score_scale, n)
    sum = 0
    for i in lz:
        sum += len(i[1])

    # print(f1, "---", f2,"---", f3, "---", f4, "---", f5)
    # print('适应度：',f1+f2+f3+f4*0.5+f5*0.5)

    # print("学生数：",(1-f4)*0.5)
    # print("分布：",(1-f5)*0.5)

    return ((1 - f4) * 0.5 , (1 - f5) * 0.5)

# *******************************************************


# data = pd.read_excel(r"new_list.xlsx")
# data.columns = ["id", "score", "teacher"]
#
# id_teacher = dict([*zip(data["id"], data["teacher"])])
# id_score = dict([*zip(data["id"], data["score"])])
#
# score_scale = [0, 0, 0, 0, 0]
# for i in data["score"]:
#     if i < 2.0:
#         score_scale[0] += 1
#     elif i < 2.5:
#         score_scale[1] += 1
#     elif i < 3.0:
#         score_scale[2] += 1
#     elif i < 3.5:
#         score_scale[3] += 1
#     else:
#         score_scale[4] += 1
#
# for i in range(5):
#     score_scale[i] = score_scale[i] / data.shape[0]
#
#
# def dist(group_scale):
#     sum = 0
#     for i in range(5):
#         sum += (score_scale[i] - group_scale[i]) ** 2
#     return math.sqrt(sum)
#
# def fit_1(lz):
#     for group in lz:
#         for stu in group[1]:
#             if id_teacher[stu] in group[0]['teachers']:
#                 return 100000
#     return 0
#
# def fit_2(lz):
#     lz_group_score = []
#     for group in lz:
#         group_score_scale = [0, 0, 0, 0, 0]
#         for stu_id in group[1]:
#             #             print(stu_id)
#             if id_score[stu_id] < 2.0:
#                 group_score_scale[0] += 1
#             elif id_score[stu_id] < 2.5:
#                 group_score_scale[1] += 1
#             elif id_score[stu_id] < 3.0:
#                 group_score_scale[2] += 1
#             elif id_score[stu_id] < 3.5:
#                 group_score_scale[3] += 1
#             else:
#                 group_score_scale[4] += 1
#         for i in range(5):
#             group_score_scale[i] = group_score_scale[i] / len(group[1])
#         lz_group_score.append(dist(group_score_scale))
#     return np.array(lz_group_score).mean()
#
# def fit_3(res):
#     # x为允许误差
#     id_teacher = dict([*zip(data["id"], data["teacher"])])
#     id_score = dict([*zip(data["id"], data["score"])])
#     teacher_statu = {}
#     for teacher in list(id_teacher.values()):
#         teacher_statu[teacher] = []
#     for student, teacher in id_teacher.items():
#         teacher_statu[teacher].append(id_score[student])
#     sum = 0
#     for i in res:
#         for j in list(i[0].keys())[:-1]:
#             #print(j, i[0][j], len(teacher_statu[j]))
#             sum += abs(i[0][j] - len(teacher_statu[j]))
#     # print(sum)
#     return sum
#
#
# def fit_4(lz):
#     dic = {}
#     for i in list(set(id_teacher.values())):
#         dic[i] = 0
#     for group in lz:
#         for tea in group[0]["teachers"]:
#             if dic[tea] == 1:
#                 return 100000
#             else:
#                 dic[tea] = 1
#     return 0
#
# def fit_5(res):
#     sum = 0
#     for group in res:
#         for stu in list(group[0].values())[:-1]:
#             sum += stu
#
#     ave_stu = sum / len(res)
#     #print("***{}***".format(ave_stu))
#
#     total = 0
#     for group in res:
#         sum_1 = 0
#         for stu in list(group[0].values())[:-1]:
#             sum_1 += stu
#         #print(sum_1)
#         total += abs(sum_1 - ave_stu)
#         #print(total)
#     return total
#
# def fit_cal(lz):
#     # f1 = fit_1(lz)
#     # f2 = fit_2(lz)
#     f3 = fit_3(lz)
#     # f4 = fit_4(lz)
#     f5 = fit_5(lz)
#     return (f3, f5)

# ===================================================================分隔符==============================================
# import pandas as pd
# import math
# import numpy as np
# import tools.res_initial as res_initial
# '''
#
# 1.参与答辩的老师不能作为该老师指导学生所在组的答辩老师。
# 2.参与答辩学生的老师不作为该老师指导学生的评阅老师。
# 3.参与答辩的老师最多只能成为一次答辩老师。
# 4.每组的参与答辩的学生人数尽量相当。
# 5.每组的学生绩点分布要与所有学生绩点分布相近。
#
#
# '''
#
# def dist(group_scale, score_scale):
#     sum = 0
#     for i in range(5):
#         sum += (score_scale[i] - group_scale[i]) ** 2
#     return math.sqrt(sum)
#
# def worst_f5(lz, score_scale, score_level_num, n):
#     group_score_scale = [0, 0, 0, 0, 0]
#     sum = 0
#     bad_group_score = []
#     for group in lz:
#         for stu in list(group[0].values())[:-1]:
#             sum += stu
#     ave_stu = sum / len(lz)
#     i = 0
#     while i < n:
#         for j in range(5):
#             if score_level_num[j] > 0:
#                 if score_level_num[j] < ave_stu:
#                     group_score_scale[j] += score_level_num[j]
#                     ave_stu -= score_level_num[j]
#                     score_level_num[j] = 0
#                 elif score_level_num[j] >= ave_stu:
#                     tem = score_level_num[j]-ave_stu
#                     group_score_scale[j] += ave_stu
#                     score_level_num[j] = tem
#                     ave_stu = 0
#                     break
#         ave_stu = sum / len(lz)
#         for j in range(5):
#             group_score_scale[j] = group_score_scale[j] / ave_stu
#         bad_group_score.append(dist(group_score_scale, score_scale))
#         group_score_scale = [0, 0, 0, 0, 0]
#         i += 1
#     return np.array(bad_group_score).mean()
# def fit_1(lz):
#     for group in lz:            # 关于两个老师不能在同一组，若在同一组，则适应度无限大
#         for teacher in group[0]['teachers']:
#             for test_teacher in group[0]['teachers']:
#                 if test_teacher in res_initial.teacher_teacher[teacher]:
#                     return -100
#     for group in lz:            # 关于两个老师必须在同一组，若不在同一组，则适应度无限大
#         for teacher in group[0]['teachers']:
#             count = 0
#             if teacher in res_initial.same_teacher:
#                 count += 1
#                 for test_teacher in group[0]['teachers']:
#                     if test_teacher in res_initial.same_teacher and test_teacher != teacher:
#                         count += 1
#                 if count != len(res_initial.same_teacher):
#                     return -100
#     return 0
#
#
# def fit_2(res, id_teacher={}, id_score={}):
#     # x为允许误差
#     point = 0
#     for group in res:
#         for i in list(group[0].keys())[:-1]:
#             while point < group[0][i]:
#                 if id_teacher[group[1][point]] == i:
#                     return -100
#                 point += 1
#     return 0
#
#
# def fit_3(lz, id_teacher={}):
#     dic = {}
#     for i in list(set(id_teacher.values())):
#         dic[i] = 0
#     for group in lz:
#         for tea in group[0]["teachers"]:
#         # for tea in group[2]:
#             if dic[tea] == 1:
#                 return -100
#             else:
#                 dic[tea] = 1
#     return 0
#
# def fit_4(res):
#     sum = 0
#     for group in res:
#         for stu in list(group[0].values())[:-1]:
#         # for stu in group[0].values():
#             sum += stu
#
#     ave_stu = sum/len(res)
#     # print("***{}***".format(ave_stu))
#
#     total = 0
#     for group in res:
#         sum_1 = 0
#         for stu in list(group[0].values())[:-1]:
#         # for stu in group[0].values():
#             sum_1 += stu
#         # print(sum_1)
#         total += abs(sum_1-ave_stu)
#         # print(total)
#     return total / (ave_stu * 2 * len(res))
#
# def fit_5(lz, id_score={}, score_scale=[], n=0):
#     lz_group_score = []
#     score_level_num = [0, 0, 0, 0, 0]
#     # print('id_score',id_score)
#     for group in lz:
#         group_score_scale = [0, 0, 0, 0, 0]
#         for stu_id in group[1]:
#             #             print(stu_id)
#             if id_score[stu_id] < 2.0:
#                 group_score_scale[0] += 1
#                 score_level_num[0] += 1
#             elif id_score[stu_id] < 2.5:
#                 group_score_scale[1] += 1
#                 score_level_num[1] += 1
#             elif id_score[stu_id] < 3.0:
#                 group_score_scale[2] += 1
#                 score_level_num[2] += 1
#             elif id_score[stu_id] < 3.5:
#                 group_score_scale[3] += 1
#                 score_level_num[3] += 1
#             else:
#                 group_score_scale[4] += 1
#                 score_level_num[4] += 1
#         for i in range(5):
#             group_score_scale[i] = group_score_scale[i] / len(group[1])
#         lz_group_score.append(dist(group_score_scale, score_scale))
#     # print('new_f2:', np.array(lz_group_score).mean()/worst_f5(lz, score_scale, score_level_num, n))
#     return np.array(lz_group_score).mean()/worst_f5(lz, score_scale, score_level_num, n)
#
#
# def fit_all(lz, id_teacher, id_score, score_scale, n):
#     f1 = fit_1(lz)
#     f2 = 0
#     f3 = fit_3(lz, id_teacher)
#     f4 = fit_4(lz)
#     f5 = fit_5(lz, id_score, score_scale, n)
#     sum = 0
#     for i in lz:
#         sum += len(i[1])
#
#     # print(f1, "---", f2,"---", f3, "---", f4, "---", f5)
#     # print('适应度：',f1+f2+f3+f4*0.5+f5*0.5)
#
#     return f1+f2+f3+(1-f4)*0.5+(1-f5)*0.5
#
# # *******************************************************
#
#
# # data = pd.read_excel(r"new_list.xlsx")
# # data.columns = ["id", "score", "teacher"]
# #
# # id_teacher = dict([*zip(data["id"], data["teacher"])])
# # id_score = dict([*zip(data["id"], data["score"])])
# #
# # score_scale = [0, 0, 0, 0, 0]
# # for i in data["score"]:
# #     if i < 2.0:
# #         score_scale[0] += 1
# #     elif i < 2.5:
# #         score_scale[1] += 1
# #     elif i < 3.0:
# #         score_scale[2] += 1
# #     elif i < 3.5:
# #         score_scale[3] += 1
# #     else:
# #         score_scale[4] += 1
# #
# # for i in range(5):
# #     score_scale[i] = score_scale[i] / data.shape[0]
# #
# #
# # def dist(group_scale):
# #     sum = 0
# #     for i in range(5):
# #         sum += (score_scale[i] - group_scale[i]) ** 2
# #     return math.sqrt(sum)
# #
# # def fit_1(lz):
# #     for group in lz:
# #         for stu in group[1]:
# #             if id_teacher[stu] in group[0]['teachers']:
# #                 return 100000
# #     return 0
# #
# # def fit_2(lz):
# #     lz_group_score = []
# #     for group in lz:
# #         group_score_scale = [0, 0, 0, 0, 0]
# #         for stu_id in group[1]:
# #             #             print(stu_id)
# #             if id_score[stu_id] < 2.0:
# #                 group_score_scale[0] += 1
# #             elif id_score[stu_id] < 2.5:
# #                 group_score_scale[1] += 1
# #             elif id_score[stu_id] < 3.0:
# #                 group_score_scale[2] += 1
# #             elif id_score[stu_id] < 3.5:
# #                 group_score_scale[3] += 1
# #             else:
# #                 group_score_scale[4] += 1
# #         for i in range(5):
# #             group_score_scale[i] = group_score_scale[i] / len(group[1])
# #         lz_group_score.append(dist(group_score_scale))
# #     return np.array(lz_group_score).mean()
# #
# # def fit_3(res):
# #     # x为允许误差
# #     id_teacher = dict([*zip(data["id"], data["teacher"])])
# #     id_score = dict([*zip(data["id"], data["score"])])
# #     teacher_statu = {}
# #     for teacher in list(id_teacher.values()):
# #         teacher_statu[teacher] = []
# #     for student, teacher in id_teacher.items():
# #         teacher_statu[teacher].append(id_score[student])
# #     sum = 0
# #     for i in res:
# #         for j in list(i[0].keys())[:-1]:
# #             #print(j, i[0][j], len(teacher_statu[j]))
# #             sum += abs(i[0][j] - len(teacher_statu[j]))
# #     # print(sum)
# #     return sum
# #
# #
# # def fit_4(lz):
# #     dic = {}
# #     for i in list(set(id_teacher.values())):
# #         dic[i] = 0
# #     for group in lz:
# #         for tea in group[0]["teachers"]:
# #             if dic[tea] == 1:
# #                 return 100000
# #             else:
# #                 dic[tea] = 1
# #     return 0
# #
# # def fit_5(res):
# #     sum = 0
# #     for group in res:
# #         for stu in list(group[0].values())[:-1]:
# #             sum += stu
# #
# #     ave_stu = sum / len(res)
# #     #print("***{}***".format(ave_stu))
# #
# #     total = 0
# #     for group in res:
# #         sum_1 = 0
# #         for stu in list(group[0].values())[:-1]:
# #             sum_1 += stu
# #         #print(sum_1)
# #         total += abs(sum_1 - ave_stu)
# #         #print(total)
# #     return total
# #
# # def fit_cal(lz):
# #     # f1 = fit_1(lz)
# #     # f2 = fit_2(lz)
# #     f3 = fit_3(lz)
# #     # f4 = fit_4(lz)
# #     f5 = fit_5(lz)
# #     return (f3, f5)
