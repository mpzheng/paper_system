import pandas as pd
from tools import res_initial

def to_CSV(g_best,name,id_score,id_teacher,id_name,id_title):
    '''
    将解写成CSV格式
    :param g_best: 最终粒子解
    :param name: 算法名称
    :param id_score:
    :param id_teacher:
    :return:
    '''
    pd_data = {'姓名': [], '学号': [], '绩点': [], '论文题目': [], '指导老师': [], '评阅老师': [], '答辩老师': []}
    for i in g_best:
        # jg.write(str('{'))
        p_l = list(i[0].keys())

        # for j in p_l[:-1]:
        #     jg.write(str('"'+j+'":'+str(i[0][j])+','))
        # jg.write(str('"dabian_Teachers":['))
        # for j in i[0]['teachers']:
        #     if i[0]['teachers'].index(j) != 0:
        #         jg.write(str(','))
        #     jg.write(str('"' + j + '"'))
        # jg.write(str('],'))
        # jg.write(str('"Student":['))
        for student in i[1]:
            # if i[1].index(student) != 0:
                # jg.write(str(','))
            # jg.write(str(student))
            pd_data['姓名'].append(id_name[student])
            pd_data['学号'].append(student)
            pd_data['绩点'].append(id_score[student])
            pd_data['论文题目'].append(id_title[student])
            pd_data['指导老师'].append(id_teacher[student])
            pd_data['评阅老师'].append(res_initial.student_pingyue[student])
            temp = ""
            for te in i[0]['teachers']:
                temp = temp + te + ",\n"
            pd_data['答辩老师'].append(temp)
        pd_data['姓名'].append(' ')
        pd_data['学号'].append(' ')
        pd_data['绩点'].append(' ')
        pd_data['论文题目'].append(' ')
        pd_data['指导老师'].append(' ')
        pd_data['评阅老师'].append(' ')
        pd_data['答辩老师'].append(' ')
        # jg.write(']}\n')
    # jg.close()
    pd_df = pd.DataFrame(pd_data)
    # pd_df.to_excel(r'C:\Users\44540\Desktop\结果表格.xlsx')
    pd_df.to_excel('../output/'+name+'result.xlsx')