import random


# data = pd.read_excel(r"new_list.xlsx")
# data.columns = ["id", "score", "teacher"]
teacher_teacher = {}
student_pingyue = {}


def lzcsh(data, n, x, n_groups, teachers, clash_teacher=[], same_teacher=[], same_teacher_p=[]):
    '''
    data 为数据
    n为组数
    x为每组人数不同的程度
    n_groups为粒子数
    teachers 为答辩老师
    '''
    lzs = []
    id_teacher = dict([*zip(data["id"], data["teacher"])])
    id_score = dict([*zip(data["id"], data["score"])])
    teacher_statu = {}
    for teacher in list(id_teacher.values()):
        teacher_statu[teacher] = []
    for student, teacher in id_teacher.items():
        # teacher_statu[teacher].append(str.lower(teacher.split("老师")[0]))
        teacher_statu[teacher].append(student)
    teacher_stu_count = {}
    #     *******************
    # 先把老师按照指导学生数排序
    for a, b in teacher_statu.items():
        teacher_stu_count[a] = len(b)
    temp_ans = dict(sorted(teacher_stu_count.items(), key=lambda teacher_stu_count: teacher_stu_count[1]))

    # print(temp_ans)
    temp_ans = list(temp_ans)
    # **************************
    if len(temp_ans) % 2 != 0:  # 如果老师数目是奇数的话 就最后俩个互换，再前n-1个老师互换
        teacher_statu[temp_ans[-1]], teacher_statu[temp_ans[-2]] = teacher_statu[temp_ans[-2]], teacher_statu[
            temp_ans[-1]]
        teacher_teacher[temp_ans[-1]] = [temp_ans[-3]]      #将互相交换的老师也纳入不能在一起的老师列表
        teacher_teacher[temp_ans[-3]] = [temp_ans[-1]]
    for i in range(int(len(temp_ans) / 2)):  # 前n（n-1）个老师学生互换
        teacher_statu[temp_ans[i * 2]], teacher_statu[temp_ans[i * 2 + 1]] = teacher_statu[temp_ans[i * 2 + 1]], \
                                                                             teacher_statu[temp_ans[i * 2]]
        teacher_teacher[temp_ans[i * 2]] = [temp_ans[i * 2 + 1]]    #将互相交换的老师也纳入不能在一起的老师列表
        teacher_teacher[temp_ans[i * 2 + 1]] = [temp_ans[i * 2]]
    if len(clash_teacher) > 0:
        for c_t in clash_teacher:
            for ct in c_t:
                for c in c_t:
                    if c != ct:
                        if c not in teacher_teacher[ct]:
                            teacher_teacher[ct].append(c)  # 将用户设定的不在一组的老师设置在冲突老师列表
                        if ct not in teacher_teacher[c]:
                            teacher_teacher[c].append(ct)
    for i in list(teacher_statu.keys()):
        for j in teacher_statu[i]:
            student_pingyue[j] = i
    # print(student_pingyue)

    stu_sums = 0
    for num in teacher_statu.values():
        stu_sums += len(num)
    # print("ave_stu:", stu_sums / n)
    ave_stu = stu_sums / n  # 每组平均学生数

    n_group = 0
    count_unusual = 0
    while n_group < n_groups:
        lz = []
        # print("第{}个粒子".format(n_group))
        teacher_temp = temp_ans.copy()
        n_count = 0
        cnt = 0
        while (n_count < n):
            cnt += 1
            lz_group = []
            if count_unusual >= (650/n):
                print("无法初始化")
                return -2
            if cnt >= 10:  # cnt是阈值 如果到阈值某个粒子还没被初始化出来 就重新初始化
                # print("new_lizi")
                teacher_temp = temp_ans.copy()
                lz = []
                cnt = 0
                n_count = 0
                count_unusual += 1
                continue

            teacher_copy = teacher_temp.copy()
            point = len(teacher_temp)
            point_copy = point

            # print("第0组：")
            for iters in range(10000):  # 每组i个老师，每次重复试10000次的随机
                lz = []
                teacher_copy = teacher_temp.copy()
                point_copy = point
                num_count = 0
                final_group = {}
                final_group.clear()
                teacher_except = []

                while num_count < ave_stu - x:
                    if len(teacher_temp) == 0:
                        break
                    temp = random.sample(teacher_temp, 1).copy()

                    if temp[0] in same_teacher:  # 选择一个老师时，若有必须在一起答辩的老师则同样把该老师纳入该组
                        for tea in same_teacher:
                            if tea != temp[0] and tea in teacher_temp:
                                temp.append(tea)

                    if temp[0] in same_teacher_p:  # 选择一个老师时，若有必须在一起评阅的老师则同样把该老师纳入该组
                        for tea in same_teacher_p:
                            if tea != temp[0] and tea in teacher_temp:
                                temp.append(tea)


                    for tea in temp:
                        if teacher_temp.index(tea) < point:

                            for except_teacher in teacher_teacher[tea]:  #选择一个老师时，将不能在一起的老师在选该组时除外
                                if teacher_temp.count(except_teacher) != 0:
                                    if except_teacher in same_teacher:
                                        for t in same_teacher:
                                            teacher_except.append(t)
                                            teacher_temp.pop(teacher_temp.index(t))
                                    else:
                                        teacher_except.append(except_teacher)
                                        teacher_temp.pop(teacher_temp.index(except_teacher))

                                point -= 1
                            num_count += len(teacher_statu[tea])
                            final_group[tea] = teacher_statu[tea]
                            point -= 1
                            teacher_temp.pop(teacher_temp.index(tea))

                        else:
                            num_count += len(teacher_statu[tea])
                            final_group[tea] = teacher_statu[tea]
                            teacher_temp.pop(teacher_temp.index(tea))
                #                     print("----------{}------".format(num_count))

                if num_count < ave_stu - x:
                    break

                if num_count > (ave_stu + x) or len(final_group) < teachers:
                    num_count = 0
                    teacher_temp = teacher_copy.copy()
                    point = point_copy
                    teacher_except.clear()
                    continue

                n_count += 1
                # print(final_group)

                teacher_temp = teacher_temp + teacher_except
                keys = []
                keys = final_group.keys()
                teacher_stu_num = {}
                teacher_stu_list = []
                for key in keys:
                    teacher_stu_num[key] = len(teacher_statu[key])
                for key in keys:
                    teacher_stu_list = teacher_stu_list + teacher_statu[key]
                lz.append(teacher_stu_num)
                lz.append(teacher_stu_list)
                lz_group.append(lz)
                if len(teacher_temp) == 0:
                    break
                # print("第%d组：" % n_count)
        lz_sum = 0
        for g in lz_group:
            lz_sum += len(g[1])
        if lz_sum != stu_sums:
            continue
        lzs.append(lz_group)
        n_group += 1
        # print("******" * 20)


        for lz in lzs:
            # print(lz)
            for group in lz:
                temp_tea = list(group[0])[:teachers]
                group[0]["teachers"] = temp_tea
                # print(group)

            #     group.append("666")
            #     print(group)
            #     print('---' * 20)
    # print(lzs)
    # print(teacher_teacher)
    return lzs,teacher_statu




# res = lzcsh(data, 6, 2, 50, 3)
#     '''
#     data 为数据
#     n为组数
#     x为每组人数不同的程度
#     n_groups为粒子数
#     teachers为答辩老师数目
#     '''

# valid_count = 0
# valid_lz = []
# for r in res:
#     flag = 0
#     print("*" * 20)
#     for j, k in enumerate(r):
#         flg = 0
#         for te in k[0].keys():
#             for su in k[1]:
#                 # if (te.split("老师")[0] == str.upper(su)):
#                 if (te == id_teacher[su]):
#                     flg = 1
#                     flag = 1
#
#         print("该{}组老师人数：{}，分别为{}  - 学生人数：{} - 答辩老师：{}".format(j, len(k[0].keys()), list(k[0]), len(k[1]), k[-1]),
#               "该组是否有冲突：{}".format(bool(flg)))
#     print()
#
#     for g in r:
#         print(g)
#     if flag == 0:
#         valid_count += 1
#         valid_lz.append(r)
#     print(bool(flag))
#     print()
#     print()
#
# print("合法的粒子数：{}".format(valid_count))
#
# print()

# for r in valid_lz:
#     flag = 0
#     print("*" * 20)
#     for j, k in enumerate(r):
#         flg = 0
#         for te in k[0].keys():
#             for su in k[1]:
#                 if (te.split("老师")[0] == str.upper(su)):
#                     flg = 1
#                     flag = 1
#
#         print("该{}组老师人数：{}，分别为{}  - 学生人数：{} - 答辩老师：{}".format(j, len(k[0].keys()), list(k[0]), len(k[1]), k[-1]),
#               "该组是否有冲突：{}".format(bool(flg)))
#     print()
#     for g in r:
#         print(g)
# with open("res_initial.txt","w") as f:
#     f.write("生成解时间：{}".format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))+"\n\n")
#     for d,r in enumerate(valid_lz):
#         flag = 0
#         f.write("第{}个可行解".format(d))
#         f.write("*"*20+"\n")
#     #     print("*"*20)
#     #     for j,k in enumerate(r) :
#     #         flg = 0
#     #         for te in k[0].keys():
#     #             for su in k[1]:
#     #                 if(te.split("老师")[0]==str.upper(su)):
#     #                     flg=1
#     #                     flag = 1
#
#     #         print("第{}组老师人数：{}，分别为{}  - 学生人数：{} - 答辩老师：{}".format(j,len(k[0].keys()),list(k[0]),len(k[1]),k[-1]),"该组是否有冲突：{}".format(bool(flg)))
#     #     print()
#         for g in r:
#             f.write(json.dumps(g,ensure_ascii=False)+"\n")
#     #         print(g)
#         f.write("\n\n")



#
# for i in res:
#     ans = fit_fun.fit(i)
#     ans.append(np.array(ans).mean())
#     print("--------:".format(i), ans)

# =================================================分隔符=======================================================================
# import random
# # data = pd.read_excel(r"new_list.xlsx")
# # data.columns = ["id", "score", "teacher"]
# teacher_teacher = {}
# student_pingyue = {}
# clash_teacher = ['A老师', 'Y老师']           #不能在一起的老师列表
# same_teacher = ['B老师', 'T老师', 'S老师']      #在一起的老师列表
# def lzcsh(data, n, x, n_groups, teachers):
#     '''
#     data 为数据
#     n为组数
#     x为每组人数不同的程度
#     n_groups为粒子数
#     teachers 为答辩老师
#     '''
#     lzs = []
#     id_teacher = dict([*zip(data["id"], data["teacher"])])
#     id_score = dict([*zip(data["id"], data["score"])])
#     teacher_statu = {}
#     for teacher in list(id_teacher.values()):
#         teacher_statu[teacher] = []
#     for student, teacher in id_teacher.items():
#         # teacher_statu[teacher].append(str.lower(teacher.split("老师")[0]))
#         teacher_statu[teacher].append(student)
#     teacher_stu_count = {}
#     #     *******************
#     # 先把老师按照指导学生数排序
#     for a, b in teacher_statu.items():
#         teacher_stu_count[a] = len(b)
#     temp_ans = dict(sorted(teacher_stu_count.items(), key=lambda teacher_stu_count: teacher_stu_count[1]))
#
#     # print(temp_ans)
#     temp_ans = list(temp_ans)
#     # **************************
#     if len(temp_ans) % 2 != 0:  # 如果老师数目是奇数的话 就最后俩个互换，再前n-1个老师互换
#         teacher_statu[temp_ans[-1]], teacher_statu[temp_ans[-2]] = teacher_statu[temp_ans[-2]], teacher_statu[
#             temp_ans[-1]]
#         teacher_teacher[temp_ans[-1]] = [temp_ans[-3]]      #将互相交换的老师也纳入不能在一起的老师列表
#         teacher_teacher[temp_ans[-3]] = [temp_ans[-1]]
#     for i in range(int(len(temp_ans) / 2)):  # 前n（n-1）个老师学生互换
#         teacher_statu[temp_ans[i * 2]], teacher_statu[temp_ans[i * 2 + 1]] = teacher_statu[temp_ans[i * 2 + 1]], \
#                                                                              teacher_statu[temp_ans[i * 2]]
#         teacher_teacher[temp_ans[i * 2]] = [temp_ans[i * 2 + 1]]    #将互相交换的老师也纳入不能在一起的老师列表
#         teacher_teacher[temp_ans[i * 2 + 1]] = [temp_ans[i * 2]]
#     if len(clash_teacher) > 0:
#         teacher_teacher[clash_teacher[0]].append(clash_teacher[1])      #将用户设定的不在一组的老师设置在冲突老师列表
#         teacher_teacher[clash_teacher[1]].append(clash_teacher[0])
#     for i in list(teacher_statu.keys()):
#         for j in teacher_statu[i]:
#             student_pingyue[j] = i
#     print(student_pingyue)
#
#     stu_sums = 0
#     for num in teacher_statu.values():
#         stu_sums += len(num)
#     # print("ave_stu:", stu_sums / n)
#     ave_stu = stu_sums / n  # 每组平均学生数
#
#     n_group = 0
#     while n_group < n_groups:
#         lz = []
#         # print("第{}个粒子".format(n_group))
#         teacher_temp = temp_ans.copy()
#         n_count = 0
#         cnt = 0
#         while (n_count < n):
#             cnt += 1
#             lz_group = []
#             if cnt >= 10:  # cnt是阈值 如果到阈值某个粒子还没被初始化出来 就重新初始化
#                 # print("new_lizi")
#                 teacher_temp = temp_ans.copy()
#                 lz = []
#                 cnt = 0
#                 n_count = 0
#                 continue
#
#             teacher_copy = teacher_temp.copy()
#             point = len(teacher_temp)
#             point_copy = point
#
#             # print("第0组：")
#             for iters in range(10000):  # 每组i个老师，每次重复试10000次的随机
#                 lz = []
#                 teacher_copy = teacher_temp.copy()
#                 point_copy = point
#                 num_count = 0
#                 final_group = {}
#                 final_group.clear()
#                 teacher_except = []
#
#                 while num_count < ave_stu - x:
#                     if len(teacher_temp) == 0:
#                         break
#                     temp = random.sample(teacher_temp, 1).copy()
#
#                     if temp[0] in same_teacher:     #选择一个老师时，若有必须在一起的老师则同样把该老师纳入该组
#                         for tea in same_teacher:
#                             if tea != temp[0] and tea in teacher_temp:
#                                 temp.append(tea)
#
#                     for tea in temp:
#                         if teacher_temp.index(tea) < point:
#
#                             for except_teacher in teacher_teacher[tea]:  #选择一个老师时，将不能在一起的老师在选该组时除外
#                                 if teacher_temp.count(except_teacher) != 0:
#                                     if except_teacher in same_teacher:
#                                         for t in same_teacher:
#                                             teacher_except.append(t)
#                                             teacher_temp.pop(teacher_temp.index(t))
#                                     else:
#                                         teacher_except.append(except_teacher)
#                                         teacher_temp.pop(teacher_temp.index(except_teacher))
#
#                                 point -= 1
#                             num_count += len(teacher_statu[tea])
#                             final_group[tea] = teacher_statu[tea]
#                             point -= 1
#                             teacher_temp.pop(teacher_temp.index(tea))
#
#                         else:
#                             num_count += len(teacher_statu[tea])
#                             final_group[tea] = teacher_statu[tea]
#                             teacher_temp.pop(teacher_temp.index(tea))
#                 #                     print("----------{}------".format(num_count))
#
#                 if num_count < ave_stu - x:
#                     break
#
#                 if num_count > (ave_stu + x) or len(final_group) < teachers:
#                     num_count = 0
#                     teacher_temp = teacher_copy.copy()
#                     point = point_copy
#                     teacher_except.clear()
#                     continue
#
#                 n_count += 1
#                 # print(final_group)
#
#                 teacher_temp = teacher_temp + teacher_except
#                 keys = []
#                 keys = final_group.keys()
#                 teacher_stu_num = {}
#                 teacher_stu_list = []
#                 for key in keys:
#                     teacher_stu_num[key] = len(teacher_statu[key])
#                 for key in keys:
#                     teacher_stu_list = teacher_stu_list + teacher_statu[key]
#                 lz.append(teacher_stu_num)
#                 lz.append(teacher_stu_list)
#                 lz_group.append(lz)
#                 if len(teacher_temp) == 0:
#                     break
#                 # print("第%d组：" % n_count)
#         lz_sum = 0
#         for g in lz_group:
#             lz_sum += len(g[1])
#         if lz_sum != stu_sums:
#             continue
#         lzs.append(lz_group)
#         n_group += 1
#         # print("******" * 20)
#
#
#         for lz in lzs:
#             # print(lz)
#             for group in lz:
#                 temp_tea = list(group[0])[:teachers]
#                 group[0]["teachers"] = temp_tea
#                 # print(group)
#
#             #     group.append("666")
#             #     print(group)
#             #     print('---' * 20)
#     print(lzs)
#     return lzs,teacher_statu
#
#
#
#
# # res = lzcsh(data, 6, 2, 50, 3)
# #     '''
# #     data 为数据
# #     n为组数
# #     x为每组人数不同的程度
# #     n_groups为粒子数
# #     teachers为答辩老师数目
# #     '''
#
# # valid_count = 0
# # valid_lz = []
# # for r in res:
# #     flag = 0
# #     print("*" * 20)
# #     for j, k in enumerate(r):
# #         flg = 0
# #         for te in k[0].keys():
# #             for su in k[1]:
# #                 # if (te.split("老师")[0] == str.upper(su)):
# #                 if (te == id_teacher[su]):
# #                     flg = 1
# #                     flag = 1
# #
# #         print("该{}组老师人数：{}，分别为{}  - 学生人数：{} - 答辩老师：{}".format(j, len(k[0].keys()), list(k[0]), len(k[1]), k[-1]),
# #               "该组是否有冲突：{}".format(bool(flg)))
# #     print()
# #
# #     for g in r:
# #         print(g)
# #     if flag == 0:
# #         valid_count += 1
# #         valid_lz.append(r)
# #     print(bool(flag))
# #     print()
# #     print()
# #
# # print("合法的粒子数：{}".format(valid_count))
# #
# # print()
#
# # for r in valid_lz:
# #     flag = 0
# #     print("*" * 20)
# #     for j, k in enumerate(r):
# #         flg = 0
# #         for te in k[0].keys():
# #             for su in k[1]:
# #                 if (te.split("老师")[0] == str.upper(su)):
# #                     flg = 1
# #                     flag = 1
# #
# #         print("该{}组老师人数：{}，分别为{}  - 学生人数：{} - 答辩老师：{}".format(j, len(k[0].keys()), list(k[0]), len(k[1]), k[-1]),
# #               "该组是否有冲突：{}".format(bool(flg)))
# #     print()
# #     for g in r:
# #         print(g)
# # with open("res_initial.txt","w") as f:
# #     f.write("生成解时间：{}".format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))+"\n\n")
# #     for d,r in enumerate(valid_lz):
# #         flag = 0
# #         f.write("第{}个可行解".format(d))
# #         f.write("*"*20+"\n")
# #     #     print("*"*20)
# #     #     for j,k in enumerate(r) :
# #     #         flg = 0
# #     #         for te in k[0].keys():
# #     #             for su in k[1]:
# #     #                 if(te.split("老师")[0]==str.upper(su)):
# #     #                     flg=1
# #     #                     flag = 1
# #
# #     #         print("第{}组老师人数：{}，分别为{}  - 学生人数：{} - 答辩老师：{}".format(j,len(k[0].keys()),list(k[0]),len(k[1]),k[-1]),"该组是否有冲突：{}".format(bool(flg)))
# #     #     print()
# #         for g in r:
# #             f.write(json.dumps(g,ensure_ascii=False)+"\n")
# #     #         print(g)
# #         f.write("\n\n")
#
#
#
# #
# # for i in res:
# #     ans = fit_fun.fit(i)
# #     ans.append(np.array(ans).mean())
# #     print("--------:".format(i), ans)
