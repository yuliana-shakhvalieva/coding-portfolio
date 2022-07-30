# -*- coding: utf-8 -*-
import math
import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.metrics import roc_auc_score
import openpyxl
from sklearn.metrics import precision_recall_curve

main_file = ".\\main_file.csv"
model_file = ".\\model.xlsx"
score_file = ".\\score_file.csv"

factors = ['woe_factor_1', 'woe_factor_2', 'woe_factor_3', 'woe_factor_4', 'woe_factor_5',
           'woe_factor_6', 'woe_factor_7', 'woe_factor_8', 'woe_factor_9', 'woe_factor_10']


def main():
    df_score_card = woe('2017-09-01', '2020-08-31')

    # Все факторы
    start_regression(None, df_score_card)

    # Без прироста Gini <0.5% = <1%
    start_regression(['woe_factor_1', 'woe_factor_3', 'woe_factor_7', 'woe_factor_9'])


def woe(start_date, final_date):
    def woe_factor_1(df_score_card):
        a = [0, 1, 2]
        clm_name = 'factor_1'
        clm = df.loc[:, clm_name]

        up = []
        dw = []
        for i in range(5):
            up.append(0)
            dw.append(0)

        for row, i in zip(clm, flag):
            while True:
                try:
                    row = float(row)
                    if i == 1:
                        if row <= float(a[0]):
                            up[0] += 1
                        if row == float(a[1]):
                            up[1] += 1
                        if row >= float(a[2]):
                            up[2] += 1
                        if math.isnan(row):
                            up[3] += 1
                    if i == 0:
                        if row <= float(a[0]):
                            dw[0] += 1
                        if row == float(a[1]):
                            dw[1] += 1
                        if row >= float(a[2]):
                            dw[2] += 1
                        if math.isnan(row):
                            dw[3] += 1
                    break
                except ValueError:
                    if i == 1:
                        up[4] += 1
                    if i == 0:
                        dw[4] += 1
                    break

        woe = []
        for u, d in zip(range(len(up)), range(len(dw))):
            if (dw[d] == 0) | (up[u] == 0):
                woe.append(0)
            else:
                woe.append(math.log((up[u] / bad) / (dw[d] / good)))

        for i in range(len(woe)):
            df_score_card.loc[i, 'factor_1_woe'] = woe[i]
        print(df_score_card)

        for i, row in main_df.iterrows():
            row1 = row[clm_name]
            while True:
                try:
                    row1 = float(row1)
                    if row1 <= float(a[0]):
                        val = woe[0]
                    if row1 == float(a[1]):
                        val = woe[1]
                    if row1 >= float(a[2]):
                        val = woe[2]
                    if math.isnan(row1):
                        val = woe[3]
                    main_df.loc[i, 'woe_factor_1'] = val
                    break
                except ValueError:
                    val = woe[4]
                main_df.loc[i, 'woe_factor_1'] = val
                break

        print('woe 1/10')
        return df_score_card

    def woe_factor_2(df_score_card):
        a = [0, 1, 4, 5]
        clm_name = 'factor_2'
        clm = df.loc[:, clm_name]

        up = []
        dw = []
        for i in range(5):
            up.append(0)
            dw.append(0)

        for row, i in zip(clm, flag):
            while True:
                try:
                    row = float(row)
                    if i == 1:
                        if row <= float(a[0]):
                            up[0] += 1
                        if (row >= float(a[1])) & (row <= float(a[2])):
                            up[1] += 1
                        if row >= float(a[3]):
                            up[2] += 1
                        if math.isnan(row):
                            up[3] += 1
                    if i == 0:
                        if row <= float(a[0]):
                            dw[0] += 1
                        if (row >= float(a[1])) & (row <= float(a[2])):
                            dw[1] += 1
                        if row >= float(a[3]):
                            dw[2] += 1
                        if math.isnan(row):
                            dw[3] += 1
                    break
                except ValueError:
                    if i == 1:
                        up[4] += 1
                    if i == 0:
                        dw[4] += 1
                    break

        woe = []
        for u, d in zip(range(len(up)), range(len(dw))):
            if (dw[d] == 0) | (up[u] == 0):
                woe.append(0)
            else:
                woe.append(math.log((up[u] / bad) / (dw[d] / good)))

        for i in range(len(woe)):
            df_score_card.loc[i, 'factor_2_woe'] = woe[i]
        print(df_score_card)

        for i, row in main_df.iterrows():
            row1 = row[clm_name]
            while True:
                try:
                    row1 = float(row1)
                    if row1 <= float(a[0]):
                        val = woe[0]
                    if (row1 >= float(a[1])) & (row1 <= float(a[2])):
                        val = woe[1]
                    if row1 >= float(a[3]):
                        val = woe[2]
                    if math.isnan(row1):
                        val = woe[3]
                    main_df.loc[i, 'woe_factor_2'] = val
                    break
                except ValueError:
                    val = woe[4]
                main_df.loc[i, 'woe_factor_2'] = val
                break

        print('woe 2/10')
        return df_score_card

    def woe_factor_3(df_score_card):
        a = [0, 1]
        clm_name = 'factor_3'
        clm = df.loc[:, clm_name]

        up = []
        dw = []
        for i in range(4):
            up.append(0)
            dw.append(0)

        for row, i in zip(clm, flag):
            while True:
                try:
                    row = float(row)
                    if i == 1:
                        if row <= float(a[0]):
                            up[0] += 1
                        if row >= float(a[1]):
                            up[1] += 1
                        if math.isnan(row):
                            up[2] += 1
                    if i == 0:
                        if row <= float(a[0]):
                            dw[0] += 1
                        if row >= float(a[1]):
                            dw[1] += 1
                        if math.isnan(row):
                            dw[2] += 1
                    break
                except ValueError:
                    if i == 1:
                        up[3] += 1
                    if i == 0:
                        dw[3] += 1
                    break

        woe = []
        for u, d in zip(range(len(up)), range(len(dw))):
            if (dw[d] == 0) | (up[u] == 0):
                woe.append(0)
            else:
                woe.append(math.log((up[u] / bad) / (dw[d] / good)))

        for i in range(len(woe)):
            df_score_card.loc[i, 'factor_3_woe'] = woe[i]
        print(df_score_card)

        for i, row in main_df.iterrows():
            row1 = row[clm_name]
            while True:
                try:
                    row1 = float(row1)
                    if row1 <= float(a[0]):
                        val = woe[0]
                    if row1 >= float(a[1]):
                        val = woe[1]
                    if math.isnan(row1):
                        val = woe[2]
                    main_df.loc[i, 'woe_factor_3'] = val
                    break
                except ValueError:
                    val = woe[3]
                main_df.loc[i, 'woe_factor_3'] = val
                break

        print('woe 3/10')
        return df_score_card

    def woe_factor_4(df_score_card):
        a1 = ['0']
        a2 = ['A', '1']
        a3 = ['2', '3', '4', 'L']

        clm_name = 'factor_4'
        clm = df.loc[:, clm_name]

        up = []
        dw = []
        for i in range(5):
            up.append(0)
            dw.append(0)

        for row, i in zip(clm, flag):
            if i == 1:
                if row in a1:
                    up[0] += 1
                elif row in a2:
                    up[1] += 1
                elif row in a3:
                    up[2] += 1
                elif row == "":
                    up[3] += 1
                else:
                    up[4] += 1
            if i == 0:
                if row in a1:
                    dw[0] += 1
                elif row in a2:
                    dw[1] += 1
                elif row in a3:
                    dw[2] += 1
                elif row == "":
                    dw[3] += 1
                else:
                    dw[4] += 1

        woe = []
        for u, d in zip(range(len(up)), range(len(dw))):
            if (dw[d] == 0) | (up[u] == 0):
                woe.append(0)
            else:
                woe.append(math.log((up[u] / bad) / (dw[d] / good)))

        for i in range(len(woe)):
            df_score_card.loc[i, 'factor_4_woe'] = woe[i]
        print(df_score_card)

        for i, row in main_df.iterrows():
            row1 = row[clm_name]
            if row1 in a1:
                val = woe[0]
            elif row1 in a2:
                val = woe[1]
            elif row1 in a3:
                val = woe[2]
            elif row1 == "":
                val = woe[3]
            else:
                val = woe[4]
            main_df.loc[i, 'woe_factor_4'] = val

        print('woe 4/10')
        return df_score_card

    def woe_factor_5(df_score_card):
        a1 = ['0']
        a2 = ['A']
        a3 = ['1', '2', '3', '4', 'L']

        clm_name = 'factor_5'
        clm = df.loc[:, clm_name]

        up = []
        dw = []
        for i in range(4):
            up.append(0)
            dw.append(0)

        for row, i in zip(clm, flag):
            if i == 1:
                if (row in a1) | (row == ""):
                    up[0] += 1
                elif row in a2:
                    up[1] += 1
                elif row in a3:
                    up[2] += 1
                else:
                    up[3] += 1
            if i == 0:
                if (row in a1) | (row == ""):
                    dw[0] += 1
                elif row in a2:
                    dw[1] += 1
                elif row in a3:
                    dw[2] += 1
                else:
                    dw[3] += 1

        woe = []
        for u, d in zip(range(len(up)), range(len(dw))):
            if (dw[d] == 0) | (up[u] == 0):
                woe.append(0)
            else:
                woe.append(math.log((up[u] / bad) / (dw[d] / good)))

        for i in range(len(woe)):
            df_score_card.loc[i, 'factor_5_woe'] = woe[i]
        print(df_score_card)

        for i, row in main_df.iterrows():
            row1 = row[clm_name]
            if (row1 in a1) | (row1 == ""):
                val = woe[0]
            elif row1 in a2:
                val = woe[1]
            elif row1 in a3:
                val = woe[2]
            else:
                val = woe[3]
            main_df.loc[i, 'woe_factor_5'] = val

        print('woe 5/10')
        return df_score_card

    def woe_factor_6(df_score_card):
        a1 = ['0']
        a2 = ['A', '1', '2', 'L']

        clm_name = 'factor_6'
        clm = df.loc[:, clm_name]

        up = []
        dw = []
        for i in range(4):
            up.append(0)
            dw.append(0)

        for row, i in zip(clm, flag):
            if i == 1:
                if row in a1:
                    up[0] += 1
                elif row in a2:
                    up[1] += 1
                elif row == "":
                    up[2] += 1
                else:
                    up[3] += 1
            if i == 0:
                if row in a1:
                    dw[0] += 1
                elif row in a2:
                    dw[1] += 1
                elif row == "":
                    dw[2] += 1
                else:
                    dw[3] += 1

        woe = []
        for u, d in zip(range(len(up)), range(len(dw))):
            if (dw[d] == 0) | (up[u] == 0):
                woe.append(0)
            else:
                woe.append(math.log((up[u] / bad) / (dw[d] / good)))

        for i in range(len(woe)):
            df_score_card.loc[i, 'factor_6_woe'] = woe[i]
        print(df_score_card)

        for i, row in main_df.iterrows():
            row1 = row[clm_name]
            if row1 in a1:
                val = woe[0]
            elif row1 in a2:
                val = woe[1]
            elif row1 == "":
                val = woe[2]
            else:
                val = woe[3]
            main_df.loc[i, 'woe_factor_6'] = val

        print('woe 6/10')
        return df_score_card

    def woe_factor_7(df_score_card):
        a = [0, 21, 33, 42, 50]
        clm_name = 'factor_7'
        clm = df.loc[:, clm_name]

        up = []
        dw = []
        for i in range(7):
            up.append(0)
            dw.append(0)

        for row, i in zip(clm, flag):
            while True:
                try:
                    row = float(row)
                    if i == 1:
                        if (row <= float(a[0])) | (math.isnan(row)):
                            up[0] += 1
                        if (row > float(a[0])) & (row < float(a[1])):
                            up[1] += 1
                        if (row >= float(a[1])) & (row < float(a[2])):
                            up[2] += 1
                        if (row >= float(a[2])) & (row < float(a[3])):
                            up[3] += 1
                        if (row >= float(a[3])) & (row < float(a[4])):
                            up[4] += 1
                        if row >= float(a[4]):
                            up[5] += 1
                    if i == 0:
                        if (row <= float(a[0])) | (math.isnan(row)):
                            dw[0] += 1
                        if (row >= float(a[0])) & (row < float(a[1])):
                            dw[1] += 1
                        if (row >= float(a[1])) & (row < float(a[2])):
                            dw[2] += 1
                        if (row >= float(a[2])) & (row < float(a[3])):
                            dw[3] += 1
                        if (row >= float(a[3])) & (row < float(a[4])):
                            dw[4] += 1
                        if row >= float(a[4]):
                            dw[5] += 1
                    break
                except ValueError:
                    if i == 1:
                        up[6] += 1
                    if i == 0:
                        dw[6] += 1
                    break

        woe = []
        for u, d in zip(range(len(up)), range(len(dw))):
            if (dw[d] == 0) | (up[u] == 0):
                woe.append(0)
            else:
                woe.append(math.log((up[u] / bad) / (dw[d] / good)))

        for i in range(len(woe)):
            df_score_card.loc[i, 'factor_7_woe'] = woe[i]
        print(df_score_card)

        for i, row in main_df.iterrows():
            row1 = row[clm_name]
            val = 0
            while True:
                try:
                    row1 = float(row1)
                    if (row1 <= float(a[0])) | (math.isnan(row1)):
                        val = woe[0]
                    if (row1 >= float(a[0])) & (row1 < float(a[1])):
                        val = woe[1]
                    if (row1 >= float(a[1])) & (row1 < float(a[2])):
                        val = woe[2]
                    if (row1 >= float(a[2])) & (row1 < float(a[3])):
                        val = woe[3]
                    if (row1 >= float(a[3])) & (row1 < float(a[4])):
                        val = woe[4]
                    if row1 >= float(a[4]):
                        val = woe[5]
                    main_df.loc[i, 'woe_factor_7'] = val
                    break
                except ValueError:
                    val = woe[6]
                main_df.loc[i, 'woe_factor_7'] = val
                break

        print('woe 7/10')
        return df_score_card

    def woe_factor_8(df_score_card):
        a1 = ['0']
        a2 = ['A']

        clm_name = 'factor_8'
        clm = df.loc[:, clm_name]

        up = []
        dw = []
        for i in range(4):
            up.append(0)
            dw.append(0)

        for row, i in zip(clm, flag):
            if i == 1:
                if row in a1:
                    up[0] += 1
                elif row in a2:
                    up[1] += 1
                elif row == "":
                    up[2] += 1
                else:
                    up[3] += 1
            if i == 0:
                if row in a1:
                    dw[0] += 1
                elif row in a2:
                    dw[1] += 1
                elif row == "":
                    dw[2] += 1
                else:
                    dw[3] += 1

        woe = []
        for u, d in zip(range(len(up)), range(len(dw))):
            if (dw[d] == 0) | (up[u] == 0):
                woe.append(0)
            else:
                woe.append(math.log((up[u] / bad) / (dw[d] / good)))

        for i in range(len(woe)):
            df_score_card.loc[i, 'factor_8_woe'] = woe[i]
        print(df_score_card)

        for i, row in main_df.iterrows():
            row1 = row[clm_name]
            if row1 in a1:
                val = woe[0]
            elif row1 in a2:
                val = woe[1]
            elif row1 == "":
                val = woe[2]
            else:
                val = woe[3]
            main_df.loc[i, 'woe_factor_8'] = val

        print('woe 8/10')
        return df_score_card

    def woe_factor_9(df_score_card):
        a = [0, 1, 6, 7, 12, 13, 36, 37, 54, 55, 102, 103, 120, 121]
        clm_name = 'factor_9'
        clm = df.loc[:, clm_name]

        up = []
        dw = []
        for i in range(9):
            up.append(0)
            dw.append(0)

        for row, i in zip(clm, flag):
            while True:
                try:
                    row = float(row)
                    if i == 1:
                        if (row <= float(a[0])) | (math.isnan(row)):
                            up[0] += 1
                        if (row >= float(a[1])) & (row <= float(a[2])):
                            up[1] += 1
                        if (row >= float(a[3])) & (row <= float(a[4])):
                            up[2] += 1
                        if (row >= float(a[5])) & (row <= float(a[6])):
                            up[3] += 1
                        if (row >= float(a[7])) & (row <= float(a[8])):
                            up[4] += 1
                        if (row >= float(a[9])) & (row <= float(a[10])):
                            up[5] += 1
                        if (row >= float(a[11])) & (row <= float(a[12])):
                            up[6] += 1
                        if row >= float(a[13]):
                            up[7] += 1
                    if i == 0:
                        if (row <= float(a[0])) | (math.isnan(row)):
                            dw[0] += 1
                        if (row >= float(a[1])) & (row <= float(a[2])):
                            dw[1] += 1
                        if (row >= float(a[3])) & (row <= float(a[4])):
                            dw[2] += 1
                        if (row >= float(a[5])) & (row <= float(a[6])):
                            dw[3] += 1
                        if (row >= float(a[7])) & (row <= float(a[8])):
                            dw[4] += 1
                        if (row >= float(a[9])) & (row <= float(a[10])):
                            dw[5] += 1
                        if (row >= float(a[11])) & (row <= float(a[12])):
                            dw[6] += 1
                        if row >= float(a[13]):
                            dw[7] += 1
                    break
                except ValueError:
                    if i == 1:
                        up[8] += 1
                    if i == 0:
                        dw[8] += 1
                    break

        woe = []
        for u, d in zip(range(len(up)), range(len(dw))):
            if (dw[d] == 0) | (up[u] == 0):
                woe.append(0)
            else:
                woe.append(math.log((up[u] / bad) / (dw[d] / good)))

        for i in range(len(woe)):
            df_score_card.loc[i, 'factor_9_woe'] = woe[i]
        print(df_score_card)

        for i, row in main_df.iterrows():
            row1 = row[clm_name]
            val = 0
            while True:
                try:
                    row1 = float(row1)
                    if (row1 < float(a[0])) | (math.isnan(row1)):
                        val = woe[0]
                    if (row1 >= float(a[1])) & (row1 <= float(a[2])):
                        val = woe[1]
                    if (row1 >= float(a[3])) & (row1 <= float(a[4])):
                        val = woe[2]
                    if (row1 >= float(a[5])) & (row1 <= float(a[6])):
                        val = woe[3]
                    if (row1 >= float(a[7])) & (row1 <= float(a[8])):
                        val = woe[4]
                    if (row1 >= float(a[9])) & (row1 <= float(a[10])):
                        val = woe[5]
                    if (row1 >= float(a[11])) & (row1 <= float(a[12])):
                        val = woe[6]
                    if row1 >= float(a[13]):
                        val = woe[7]
                    main_df.loc[i, 'woe_factor_9'] = val
                    break
                except ValueError:
                    val = woe[8]
                main_df.loc[i, 'woe_factor_9'] = val
                break

        print('woe 9/10')
        return df_score_card

    def woe_factor_10(df_score_card):
        a = [-1, 3, 12, 21, 33, 46]
        clm_name = 'factor_10'
        clm = df.loc[:, clm_name]

        up = []
        dw = []
        for i in range(9):
            up.append(0)
            dw.append(0)

        for row, i in zip(clm, flag):
            while True:
                try:
                    row = float(row)
                    if i == 1:
                        if row == float(a[0]):
                            up[0] += 1
                        if (row > float(a[0])) & (row < float(a[1])):
                            up[1] += 1
                        if (row >= float(a[1])) & (row < float(a[2])):
                            up[2] += 1
                        if (row >= float(a[2])) & (row < float(a[3])):
                            up[3] += 1
                        if (row >= float(a[3])) & (row < float(a[4])):
                            up[4] += 1
                        if (row >= float(a[4])) & (row < float(a[5])):
                            up[5] += 1
                        if row >= float(a[5]):
                            up[6] += 1
                        if math.isnan(row):
                            up[7] += 1
                    if i == 0:
                        if row == float(a[0]):
                            dw[0] += 1
                        if (row > float(a[0])) & (row < float(a[1])):
                            dw[1] += 1
                        if (row >= float(a[1])) & (row < float(a[2])):
                            dw[2] += 1
                        if (row >= float(a[2])) & (row < float(a[3])):
                            dw[3] += 1
                        if (row >= float(a[3])) & (row < float(a[4])):
                            dw[4] += 1
                        if (row >= float(a[4])) & (row < float(a[5])):
                            dw[5] += 1
                        if row >= float(a[5]):
                            dw[6] += 1
                        if math.isnan(row):
                            dw[7] += 1
                    break
                except ValueError:
                    if i == 1:
                        up[8] += 1
                    if i == 0:
                        dw[8] += 1
                    break

        woe = []
        for u, d in zip(range(len(up)), range(len(dw))):
            if (dw[d] == 0) | (up[u] == 0):
                woe.append(0)
            else:
                woe.append(math.log((up[u] / bad) / (dw[d] / good)))

        for i in range(len(woe)):
            df_score_card.loc[i, 'factor_10_woe'] = woe[i]
        print(df_score_card)

        for i, row in main_df.iterrows():
            row1 = row[clm_name]
            val = 0
            while True:
                try:
                    row1 = float(row1)
                    if row1 == float(a[0]):
                        val = woe[0]
                    if (row1 > float(a[0])) & (row1 < float(a[1])):
                        val = woe[1]
                    if (row1 >= float(a[1])) & (row1 < float(a[2])):
                        val = woe[2]
                    if (row1 >= float(a[2])) & (row1 < float(a[3])):
                        val = woe[3]
                    if (row1 >= float(a[3])) & (row1 < float(a[4])):
                        val = woe[4]
                    if (row1 >= float(a[4])) & (row1 < float(a[5])):
                        val = woe[5]
                    if row1 >= float(a[5]):
                        val = woe[6]
                    if math.isnan(row1):
                        val = woe[7]
                    main_df.loc[i, 'woe_factor_10'] = val
                    break
                except ValueError:
                    val = woe[8]
                main_df.loc[i, 'woe_factor_10'] = val
                break

        print('woe 10/10')
        return df_score_card

    main_df = pd.read_csv(main_file, encoding="utf-8", sep=';', decimal='.')

    main_df['date'] = pd.to_datetime(main_df['date'])

    df = main_df[(main_df['date'] >= start_date) &
                 (main_df['date'] <= final_date)]

    df.loc[((df['date_1'] >= '2020-06-01') &
            (df['date_1'] < '2020-08-01')), 'defolt'] = 0

    bad = len(df[(df['defolt'] == 1)])
    good = len(df[(df['defolt'] == 0)])
    flag = df.loc[:, 'defolt']

    df_score_card = pd.DataFrame()
    df_score_card = woe_factor_1(df_score_card)
    df_score_card = woe_factor_2(df_score_card)
    df_score_card = woe_factor_3(df_score_card)
    df_score_card = woe_factor_4(df_score_card)
    df_score_card = woe_factor_5(df_score_card)
    df_score_card = woe_factor_6(df_score_card)
    df_score_card = woe_factor_7(df_score_card)
    df_score_card = woe_factor_8(df_score_card)
    df_score_card = woe_factor_9(df_score_card)
    df_score_card = woe_factor_10(df_score_card)

    main_df.to_csv(main_file, index=False, encoding="utf-8", sep=';', decimal='.')
    return df_score_card


def start_regression(extra_factors, df_score_card):
    if extra_factors is not None:
        for extra_factor in extra_factors:
            factors.remove(extra_factor)
    regression(factors, df_score_card)


def regression(factors, df_score_card):
    df = pd.read_csv(main_file, encoding="utf-8", sep=';', decimal='.')

    df['date'] = pd.to_datetime(df['date'])

    develop_df = df[(df['date'] >= '2017-09-01') &
                    (df['date'] <= '2020-08-31')]

    develop_df.loc[((develop_df['date_1'] >= '2020-06-01') &
                    (develop_df['date_1'] < '2020-08-01')), 'defolt'] = 0

    b_dev = develop_df['defolt']
    reg_dev = develop_df[factors]

    logit_model = sm.Logit(b_dev, reg_dev).fit()
    print(logit_model.summary2())

    b_dev_pred = logit_model.predict(exog=reg_dev)

    print(f'Количество строк: {len(b_dev_pred)}')
    print(f'Количество дефолтов фактически: {b_dev[b_dev == 1].count()}')

    precision_test, recall_test, thresholds_test = precision_recall_curve(b_dev, b_dev_pred)
    board = np.argmin(np.abs(np.array(precision_test) - np.array(recall_test)))
    print(f'Количество дефолтов предсказано: {(b_dev_pred > thresholds_test[board]).sum()}')
    print(f'Threshold: {thresholds_test[board]}')

    logit_roc_auc = roc_auc_score(b_dev, b_dev_pred)
    gini_dev = 2 * logit_roc_auc - 1
    print(f'GINI на выборке разработки: {gini_dev}')

    df_statistics = pd.DataFrame()
    if len(factors) == 1:
        df_statistics.loc[0, 'Фактор'] = factors[0]
        df_statistics.loc[0, 'Коэффициент'] = logit_model.params[0]
        df_statistics.loc[0, 'P-value'] = logit_model.pvalues[0]
        df_statistics.loc[0, 'Коэффициент норм'] = logit_model.params[0] / logit_model.bse[0]
        df_statistics.loc[0, 'Важность'] = 1

    else:
        for i, factor in enumerate(factors):
            df_statistics.loc[i, 'Фактор'] = factors[i]
            df_statistics.loc[i, 'Коэффициент'] = logit_model.params[i]
            df_statistics.loc[i, 'P-value'] = logit_model.pvalues[i]
            df_statistics.loc[i, 'Коэффициент норм'] = logit_model.params[i] / logit_model.bse[i]

        for i in range(len(factors)):
            df_statistics.loc[i, 'Важность'] = df_statistics.loc[i, 'Коэффициент норм'] / \
                                               df_statistics['Коэффициент норм'].sum()

        for i in range(len(factors)):
            factors_cut = factors[:i] + factors[i + 1:]
            reg_dev_cut = develop_df[factors_cut]

            logit_model_cut = sm.Logit(b_dev, reg_dev_cut).fit()

            b_dev_pred_cut = logit_model_cut.predict(exog=reg_dev_cut)

            logit_roc_auc_cut = roc_auc_score(b_dev, b_dev_pred_cut)
            gini_cut = 2 * logit_roc_auc_cut - 1
            df_statistics.loc[i, 'Прирост GINI dev'] = gini_dev - gini_cut

    df_statistics.loc[0, 'GINI dev'] = gini_dev
    df_statistics.to_excel(model_file, index=False, sheet_name='Statistics')

    # Расчет новых скоров
    for i in range(df.shape[0]):
        number = 0
        for x in range(len(factors)):
            number += logit_model.params[x] * df.loc[i, factors[x]]
        df.loc[i, 'Score_new_model'] = number

    df.to_csv(score_file, encoding="utf-8", sep=';', decimal='.')

    factors_woe = ['factor_1_woe', 'factor_2_woe', 'factor_3_woe', 'factor_4_woe', 'factor_5_woe', 
                   'factor_6_woe', 'factor_7_woe', 'factor_8_woe', 'factor_9_woe', 'factor_10_woe']

    for i, factor_woe in enumerate(factors_woe):
        df_score_card[factor_woe] = df_score_card[factor_woe] * logit_model.params[i]

    df_score_card.to_excel(".\\final.xlsx", index=False)


if __name__ == '__main__':
    main()
