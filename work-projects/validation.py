def main():# coding: utf-8
import numpy as np
import pandas as pd
from datetime import timedelta
import openpyxl
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
from sklearn.metrics import RocCurveDisplay
import matplotlib.pyplot as plt

main_file = ".\\main_file.csv"
result_general = ".\\General.xlsx"
result_gini = ".\\GINI.xlsx"
result_psi = ".\\PSI.xlsx"
df_main = pd.read_csv(main_file, encoding="utf-8", sep=';', decimal='.')

df_main['date'] = \
    pd.to_datetime(df_main['date'])
df_main['date_1'] = \
    pd.to_datetime(df_main['date_1'])

min_data = df_main['date'].min()
max_data = df_main['date'].max()
print(f'Минимальная дата: {min_data}')
print(f'Максимальная дата: {max_data}')

curr = ".\\file.xlsx"
curr_portf = pd.read_excel(curr)


def main():
    df_list = data_prepare()
    gini(df_list[0])
    psi(df_list[0], df_list[1])


def data_prepare():
    # [09.2017 - 08.2020] без ковида

    df = df_main[(df_main['date'] >= '01.09.2017') &
                 (df_main['date'] <= '31.08.2020')]

    df.loc[((df['date_1'] >= '2020-06-01') &
            (df['date_1'] < '2020-08-01')), 'defolt'] = 0

    df_dev = df_main[(df_main['date'] >= '01.06.2015') &
                     (df_main['date'] <= '01.09.2017')]

    df_dev.loc[((df_dev['date_1'] > '01.09.2018') &
                (df_dev['defolt'] == 1)), 'defolt'] = 0

    global curr_portf
    curr_portf = curr_portf.merge(df, on='id', how='left')
    curr_portf = curr_portf[~curr_portf['id_1'].isna()]

    print(df.dtypes)
    print()

    print('ВЫБОРКА ДЛЯ ВАЛИДАЦИИ')
    df_result_general = pd.DataFrame()
    print('Количество строк: {}\n'
          'Количество дефолтов: {}'.format(df.shape[0], df['defolt'].sum()))
    print()

    for i, column in enumerate(df.columns):
        df_result_general.loc[i, 'Столбец'] = column
        df_result_general.loc[i, 'Процент пустот'] = (df[column].isna().sum()) / df.shape[0]

    df_result_general.loc[0, 'Количество строк'] = df.shape[0]
    df_result_general.loc[0, 'Количество дефолтов'] = df['defolt'].sum()

    print('ВЫБОРКА ДЛЯ РАЗРАБОТКИ')
    df_result_dev = pd.DataFrame()
    print('Количество строк: {}\n'
          'Количество дефолтов: {}'.format(df_dev.shape[0], df_dev['defolt'].sum()))
    print()

    for i, column in enumerate(df_dev.columns):
        df_result_dev.loc[i, 'Столбец'] = column
        df_result_dev.loc[i, 'Процент пустот'] = (df_dev[column].isna().sum()) / df_dev.shape[0]

    df_result_dev.loc[0, 'Количество строк'] = df_dev.shape[0]
    df_result_dev.loc[0, 'Количество дефолтов'] = df_dev['defolt'].sum()

    print('ТЕКУЩИЙ СРЕЗ ПОРТФЕЛЯ')
    df_result_curr = pd.DataFrame()
    print('Количество строк: {}\n'
          'Количество дефолтов: {}'.format(curr_portf.shape[0], curr_portf['defolt'].sum()))
    print()

    for i, column in enumerate(curr_portf.columns):
        df_result_curr.loc[i, 'Столбец'] = column
        df_result_curr.loc[i, 'Процент пустот'] = (curr_portf[column].isna().sum()) / curr_portf.shape[0]

    df_result_curr.loc[0, 'Количество строк'] = curr_portf.shape[0]
    df_result_curr.loc[0, 'Количество дефолтов'] = curr_portf['defolt'].sum()

    clmns_for_flag = ['onehalf_years', 'two_years', 'three_years']
    clmns_60_for_flag = ['60+_onehalf_years', '60+_two_years', '60+_three_years']
    years = [1.5, 2, 3]

    for clmn_for_flag, clmn_60_for_flag, year in zip(clmns_for_flag, clmns_60_for_flag, years):
        df[clmn_for_flag] = ((df['date_1'] -
                              df['date']) /
                             timedelta(days=365) < int(year))
        df[clmn_60_for_flag] = np.where(df[clmn_for_flag], 1, 0)
        df.loc[((df['date_1'] >= '2020-06-01') &
                (df['date_1'] < '2020-08-01')), clmn_60_for_flag] = 0

    with pd.ExcelWriter(result_general) as writer:
        df_result_general.to_excel(writer, index=False, sheet_name='Валидация')
        df_result_dev.to_excel(writer, index=False, sheet_name='Разработка')
        df_result_curr.to_excel(writer, index=False, sheet_name='Текущий')

    return df, curr_portf


def gini(df):
    var = ['60+_onehalf_years', '60+_two_years', '60+_three_years', 'defolt']
    df_result_gini = pd.DataFrame()
    for i, column in enumerate(var):
        print('Gini = ', roc_auc_score(df[column], -df['SCORE']) * 2 - 1)
        print('Количество дефолтов = ', df[column].sum())
        df_result_gini.loc[i, 'Горизонт'] = column
        df_result_gini.loc[i, 'Gini'] = roc_auc_score(df[column], -df['SCORE']) * 2 - 1
        df_result_gini.loc[i, 'Количество дефолтов'] = df[column].sum()
        fpr, tpr, _ = roc_curve(df[column], -df['SCORE'])
        roc_display = RocCurveDisplay(fpr=fpr, tpr=tpr).plot()
    plt.show()

    variables = ['factor_1_score', 'factor_2_score', 'factor_3_score', 'factor_4_score', 'factor_5_score',
                 'factor_6_score', 'factor_7_score', 'factor_8_score', 'factor_9_score', 'factor_10_score']

    ginis = pd.DataFrame(index=['60+_onehalf_years', '60+_two_years', '60+_three_years', 'defolt'], columns=variables)
    df_count = pd.DataFrame()

    for i, column in enumerate(variables):
        gini_60_1y = abs(roc_auc_score(df['60+_onehalf_years'], df[column]) * 2 - 1)
        gini_60_2y = abs(roc_auc_score(df['60+_two_years'], df[column]) * 2 - 1)
        gini_60_3y = abs(roc_auc_score(df['60+_three_years'], df[column]) * 2 - 1)
        gini_60 = abs(roc_auc_score(df['defolt'], df[column]) * 2 - 1)
        ginis[column] = [gini_60_1y, gini_60_2y, gini_60_3y, gini_60]

    print(ginis)

    columns = ['factor_1', 'factor_2', 'factor_3', 'factor_4', 'factor_5',
               'factor_6', 'factor_7', 'factor_8', 'factor_9', 'factor_10']

    for i, column in enumerate(columns):
        df_count.loc[i, 'Фактор'] = column
        df_count.loc[i, 'Количество'] = df.shape[0] - df[column].isnull().sum()

    with pd.ExcelWriter(result_gini) as writer:
        df_result_gini.to_excel(writer, index=False, sheet_name='По модели')
        ginis.to_excel(writer, index=True, sheet_name='По факторам')
        df_count.to_excel(writer, index=False, sheet_name='Количество')


def psi(df, curr_portf):
    df_psi_curr = curr_portf.groupby('Group', as_index=False).agg({'id_1': 'count'})
    curr = ".\\curr.xlsx"
    df_psi_curr.to_excel(curr, index=False)

    df_psi_val = df.groupby('Group', as_index=False).agg({'id_1': 'count', 'defolt': 'sum'})
    val = ".\\val.xlsx"
    df_psi_val.to_excel(val, index=False)

    df_psi = df_psi_curr.merge(df_psi_val, on='Group')

    df_psi = df_psi.rename(columns={'id_1_x': 'Curr_portf', 'id_1_y': 'Val_sample'})

    df_psi['PSI_val'] = (
                                df_psi['Curr_portf'] / df_psi['Curr_portf'].sum() -
                                df_psi['Val_sample'] / df_psi['Val_sample'].sum()) * \
                        np.log(
                            (df_psi['Curr_portf'] / df_psi['Curr_portf'].sum()) /
                            (df_psi['Val_sample'] / df_psi['Val_sample'].sum())
                        )

    psi = df_psi['PSI_val'].sum()
    df_ = pd.DataFrame()
    df_.loc[0, 'PSI curr VS val'] = psi
    print(f'PSI curr VS val: {psi}')

    def factor_1(x):
        try:
            x = np.float64(x)
            selector = {
                x <= 0: '[Low : 0]',
                x == 1: '[1 : 1]',
                x >= 2: '[2 : High]',
            }
        except:
            return 0
        return selector.get(True, 0)

    def factor_2(x):
        try:
            x = np.float64(x)
            selector = {
                x <= 0: '[Low : 0]',
                1 <= x <= 4: '[1 : 4]',
                x >= 5: '[5 : High)',
            }
        except:
            return 0
        return selector.get(True, 0)

    def factor_3(x):
        try:
            x = np.float64(x)
            selector = {
                x <= 0: '[Low : 0]',
                x >= 1: '[1 : High]',
            }
        except:
            return 0
        return selector.get(True, 0)

    def factor_4(x):
        try:
            x = str(x).lower().strip()
            selector = {
                x == "0": '"0"',
                x in ["a", "1"]: 'A ; 1',
                x in ["2", "3", "4", "l"]: '2 ; 3 ; 4 ; L',
                x == 'nan': 'Missing Value'
            }
        except:
            return 0
        return selector.get(True, 0)

    def factor_5(x):
        try:
            x = str(x).lower().strip()
            selector = {
                (x == "0") | (x == 'nan'): '0 or Missing Value',
                x == "a": '"A"',
                x in ["1", "2", "3", "4", "l"]: '1 ; 2 ; 3 ; 4 ; L',
            }
        except:
            return 0
        return selector.get(True, 0)

    def factor_6(x):
        try:
            x = str(x).lower().strip()
            selector = {
                x == "0": '"0"',
                x in ["a", "1", "2", "l"]: 'A ; 1 ; 2 ; L',
                x == "nan": 'Missing Value'
            }
        except:
            return 0
        return selector.get(True, 0)

    def factor_7(x):
        try:
            x = np.float64(x)
            selector = {
                (x <= 0) | (np.isnan(x)): '[Low : 0] or Missing Value',
                0 < x < 21: '(0 : 21)',
                21 <= x < 33: '[21 : 33)',
                33 <= x <= 42: '[33 : 42]',
                42 <= x < 50: '[42 : 50)',
                x >= 50: '[50 : High)',
            }
        except:
            return 0
        return selector.get(True, 0)

    def factor_8(x):
        try:
            x = str(x).lower().strip()
            selector = {
                x == "0": '"0"',
                x == "a": '"A"',
                x == "nan": 'Missing Value',
            }
        except:
            return 0
        return selector.get(True, 0)

    def factor_9(x):
        try:
            x = np.float64(x)
            selector = {
                (x <= 0) | np.isnan(x): '[Low : 0] or Missing Value',
                1 <= x <= 6: '[1 : 6]',
                7 <= x <= 12: '[7 : 12]',
                13 <= x <= 36: '[13 : 36]',
                37 <= x <= 54: '[37 : 54]',
                55 <= x <= 102: '[55 : 102]',
                103 <= x <= 120: '[103 : 120]',
                x >= 121: '[121 : High)',
            }
        except:
            return 0
        return selector.get(True, 0)

    def factor_10(x):
        try:
            x = np.float64(x)
            selector = {
                x == np.float64(-1): '"-1.0"',
                -1 < x < 3: '(-1 : 3)',
                3 <= x < 12: '[3 : 12)',
                12 <= x < 21: '[12 : 21)',
                21 <= x < 33: '[21 : 33)',
                33 <= x < 46: '[33 : 46)',
                x >= 46: '[46 : High)',
                np.isnan(x): 'Missing Value',
            }
        except:
            return 0
        return selector.get(True, 0)

    df_val = df.copy().reset_index(drop=True)
    df_curr = curr_portf.reset_index(drop=True)

    clmns_bin = ['factor_1_bin', 'factor_2_bin', 'factor_3_bin', 'factor_4_bin', 'factor_5_bin',
                 'factor_6_bin', 'factor_7_bin', 'factor_8_bin', 'factor_9_bin', 'factor_10_bin']

    functions = [factor_1, factor_2, factor_3, factor_4, factor_5,
                 factor_6, factor_7, factor_8, factor_9, factor_10]

    clmns = ['factor_1', 'factor_2', 'factor_3', 'factor_4', 'factor_5',
             'factor_6', 'factor_7', 'factor_8', 'factor_9', 'factor_10']

    for clmn_bin, function, clmn in zip(clmns_bin, functions, clmns):
        df_val[clmn_bin] = [function(val) for val in df_val[clmn]]
        df_curr[clmn_bin] = [function(val) for val in df_curr[clmn]]

    all_df = []
    for clmn in clmns_bin:
        df_graph = df_val.groupby(clmn, as_index=False).agg({'id_1': 'count'})
        all_df.append(df_graph)
        print(df_graph)

    psis = []
    for clmn_bin in clmns_bin:
        psis.append(df_val.groupby(clmn_bin, as_index=False).agg(
            {
                'id_1': 'count',
                '60+_onehalf_years': 'sum',
                '60+_two_years': 'sum',
                '60+_three_years': 'sum',
                'defolt': 'sum'
            }
        ).merge(df_curr.groupby(clmn_bin, as_index=False).agg(
            {
                'id_1': 'count'
            }
        ), on=clmn_bin, how='outer'))

    psis_val = pd.DataFrame(columns=['characteristic', 'PSI_val'])

    for dataframe in psis:
        dataframe = dataframe.fillna(0.0)
        dataframe['PSI_val'] = ((dataframe['id_1_x'] / dataframe['id_1_x'].sum()) -
                                (dataframe['id_1_y'] / dataframe['id_1_y'].sum())) \
                               * np.log(
                                (dataframe['id_1_x'] / dataframe['id_1_x'].sum()) /
                                (dataframe['id_1_y'] / dataframe['id_1_y'].sum()))
        t = pd.DataFrame(columns=['characteristic', 'PSI_val'])
        t = t.append({'characteristic': dataframe.columns[0], 'PSI_val': dataframe['PSI_val'].sum()}, ignore_index=True)
        psis_val = pd.concat([psis_val, t], ignore_index=True)

    print(psis_val)

    with pd.ExcelWriter(result_psi) as writer:
        df_.to_excel(writer, index=False, sheet_name='По модели')
        psis_val.to_excel(writer, index=False, sheet_name='По факторам')
        for i in range(len(all_df)):
            all_df[i].to_excel(writer, index=False, sheet_name='Для гист', startrow=i*7)


if __name__ == "__main__":
    main()
