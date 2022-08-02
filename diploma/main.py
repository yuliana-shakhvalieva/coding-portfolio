import pandas as pd
import numpy as np
import copy
import locale
from statsmodels.tsa.stattools import adfuller, kpss
import statsmodels.api as sm
from johansen import coint_johansen

locale.setlocale(locale.LC_ALL, '')
df_main = pd.read_excel("Начальные данные.xlsx")
a = [0, 7, 15, 35, 63, 91, 126, 154, 182, 217, 364]


def float_format(x, digits_count=2):
    return ("{:." + str(digits_count) + "f}").format(x)


def diapozons(x):
    try:
        x = np.float(x)
        selector = {a[i] + 1 <= x <= a[i + 1]: (a[i] + 1, a[i + 1]) for i in range(len(a) - 1)}
    except:
        return 0
    return selector.get(True, 0)


def alpha(x):
    selector = {x > i: i * 100 for i in (0.01, 0.05, 0.1)}
    alpha = selector.get(True, 0)
    if alpha == 0:
        return '-'
    return alpha


def aggregate(key):
    df = copy.deepcopy(df_main)
    if key in ('w', 'W'):
        df['Дата'] = pd.to_datetime(df['Дата']) - pd.to_timedelta(1, unit=key)
    df['Произведение'] = df['Оборот на торгах по деньгам (млн. руб.)'] * df['Доходность непрерывная']
    multy_sum = df.groupby(['Начало/Конец диапазона дней до погашения',
                            pd.Grouper(key='Дата', freq=key)])['Произведение'] \
        .sum() \
        .reset_index() \
        .sort_values('Дата') \
        .sort_values('Начало/Конец диапазона дней до погашения', kind='mergesort')
    div_sum = df.groupby(['Начало/Конец диапазона дней до погашения',
                          pd.Grouper(key='Дата', freq=key)])['Оборот на торгах по деньгам (млн. руб.)'] \
        .sum(). \
        reset_index(). \
        sort_values('Дата'). \
        sort_values('Начало/Конец диапазона дней до погашения', kind='mergesort')
    profit = multy_sum['Произведение'] / div_sum['Оборот на торгах по деньгам (млн. руб.)']
    diap_date = multy_sum.drop('Произведение', axis=1)
    profit = pd.concat([diap_date, profit], axis=1)
    list_of_profits = [profit[profit['Начало/Конец диапазона дней до погашения'].isin([diap])] for diap in
                 profit['Начало/Конец диапазона дней до погашения'].unique()]
    list_of_profits = [
        profit.rename(columns={profit.columns[2]: str(profit['Начало/Конец диапазона дней до погашения'].unique()[0])})
        for profit in list_of_profits]
    list_of_profits = [profit.drop('Начало/Конец диапазона дней до погашения', axis=1) for profit in list_of_profits]
    return list_of_profits


def write_excel(list_of_profits, diap_letter):
    file_names = [diap_letter + '_' + by_key.columns[1] + '.xlsx' for by_key in list_of_profits]
    for list_of_profits, file_name in zip(list_of_profits, file_names):
        list_of_profits.to_excel(file_name, index=False)


def merge_all(list_of_profits):
    df_of_profits = list_of_profits[0]
    for i in range(1, len(list_of_profits)):
        df_of_profits = df_of_profits.merge(list_of_profits[i], how='outer', on='Дата')
    return df_of_profits.sort_values('Дата')


def interpolation(df_interpolate):
    date_column = df_interpolate['Дата']
    df_interpolate = df_interpolate.drop('Дата', axis=1)
    df_interpolate = df_interpolate.interpolate(method='linear', limit_area='inside', axis=1)
    df_interpolate = df_interpolate.interpolate(method='linear', limit_area='inside', axis=0)
    df_interpolate = pd.concat([date_column, df_interpolate], axis=1)
    return df_interpolate


def characteristic(df_origin, df_interpolatated):
    list_count, list_mean, list_std = [], [], []
    list_a1, list_a2, list_a3 = [], [], []
    for df in df_origin:
        column = df.drop('Дата', axis=1).iloc[:, 0]
        list_count.append(column.size)
        list_mean.append(float_format(column.mean()) + '%')
        list_std.append(float_format(column.std()) + '%')
    for column in df_interpolatated.drop('Дата', axis=1):
        df_column = df_interpolatated[column].to_frame().dropna()
        a = sm.tsa.acf(df_column, nlags=3)
        list_a1.append(float_format(a[1], 3))
        list_a2.append(float_format(a[2], 3))
        list_a3.append(float_format(a[3], 3))

    table_lst = [list_count,
           list_mean,
           list_std,
           list_a1,
           list_a2,
           list_a3]
    column_names_w = [str(index) + 'W' for index in range(1, 3)]
    column_names_m = [str(index) + 'M' for index in range(1, len(list_count) - 1)]
    indexes = ['Число наблюдений', 'Среднее значение', 'Стандартное отклонение',
               'AR(1)', 'AR(2)', 'AR(3)']
    return pd.DataFrame(table_lst, index=indexes, columns=column_names_w + column_names_m, dtype=float)


def adf_kpss_alpha(df_column):
    adf_test = adfuller(df_column, regression="c", autolag="AIC")
    kpss_test = kpss(df_column, regression="c", nlags="auto")
    alpha_test = (alpha(adf_test[1]), alpha(kpss_test[1]))
    return adf_test, kpss_test, alpha_test


def adf_kpss_test(df_column, diff_on=False):
    adf_test, kpss_test, alpha_test = adf_kpss_alpha(df_column)
    if diff_on:
        df_column = df_column.diff(periods=1).dropna()
        adf_test, kpss_test, alpha_test = adf_kpss_alpha(df_column)
    return adf_test[0:2] + kpss_test[0:2] + alpha_test


def get_adf_kpss_table(adf_kpss_result_list):
    indexes = ["Статистика ADF", "p-значение ADF",
               "Статистика KPSS", "p-значение KPSS",
               "Принимаем Н0 ADF", "Принимаем Н0 KPSS"]
    column_names_w = [str(index) + 'W' for index in range(1, 3)]
    column_names_m = [str(index) + 'M' for index in range(1, len(adf_kpss_result_list) - 1)]

    adf_kpss_table = pd.DataFrame(adf_kpss_result_list).transpose()
    adf_kpss_table.columns = column_names_w + column_names_m
    adf_kpss_table.index = indexes
    return adf_kpss_table


def adf_kpss(df_interpolatated):
    adf_kpss_result_list = []
    adf_kpss_diff_result_list = []
    for column in df_interpolatated.drop('Дата', axis=1):
        df_column = df_interpolatated[column].to_frame().dropna()
        adf_kpss_result_list.append(adf_kpss_test(df_column))
        adf_kpss_diff_result_list.append(adf_kpss_test(df_column, diff_on=True))
    adf_kpss_table = get_adf_kpss_table(adf_kpss_result_list)
    adf_kpss_diff_table = get_adf_kpss_table(adf_kpss_diff_result_list)
    return adf_kpss_table, adf_kpss_diff_table


def cointegration(df_inter):
    df_ipc = pd.read_excel("ИПЦ.xlsx")
    df_inter_ipc = df_inter.merge(df_ipc, how='outer', on='Дата')
    for inter_column in df_inter.drop('Дата', axis=1):
        for ipc_column in df_ipc.drop('Дата', axis=1):
            inter_ipc_columns = [inter_column, ipc_column]
            print(inter_ipc_columns)
            df_inter_ipc_columns = df_inter_ipc[inter_ipc_columns].dropna()
            coint_johansen(df_inter_ipc_columns, 0, 2)

def main():
    df_main['Доходность непрерывная'] = (np.log(1 / (df_main['Цена закрытия (%)'] / 100)) / (
            df_main['Дней до погашения'] / 365)) * 100
    df_main['Начало/Конец диапазона дней до погашения'] = [diapozons(x) for x in df_main['Дней до погашения']]

    list_of_profits_w = aggregate('w')
    list_of_profits_m = aggregate('m')
    df_of_profits_w = merge_all(list_of_profits_w)
    df_of_profits_m = merge_all(list_of_profits_m)
    df_of_profits_w_int = interpolation(df_of_profits_w)
    df_of_profits_m_int = interpolation(df_of_profits_m)
    characteristic_table_w = characteristic(list_of_profits_w, df_of_profits_w_int)
    characteristic_table_m = characteristic(list_of_profits_m, df_of_profits_m_int)
    adf_kpss_table_w, adf_kpss_diff_table_w = adf_kpss(df_of_profits_w_int)
    adf_kpss_table_m, adf_kpss_diff_table_m = adf_kpss(df_of_profits_m_int)
    cointegration(df_of_profits_m_int)

    characteristic_table_w.to_excel("Таблица с характеристиками_неделя.xlsx")
    characteristic_table_m.to_excel("Таблица с характеристиками_месяц.xlsx")
    write_excel(list_of_profits_w, 'w')
    write_excel(list_of_profits_m, 'm')
    adf_kpss_table_w.to_excel("Тесты единичного корня неделя.xlsx")
    adf_kpss_table_m.to_excel("Тесты единичного корня месяц.xlsx")
    adf_kpss_diff_table_w.to_excel("Тесты единичного корня первой разности неделя.xlsx")
    adf_kpss_diff_table_m.to_excel("Тесты единичного корня первой разности месяц.xlsx")
    df_of_profits_w_int.to_excel("Данные недельные интерполированные.xlsx")
    df_of_profits_m_int.to_excel("Данные месячные интерполированные.xlsx")


if __name__ == '__main__':
    main()
