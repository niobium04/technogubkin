import pandas as pd
import math

from matplotlib import pyplot as plt
import matplotlib.patches as patches


def f(your_choice, your_choice_year, df, df1):
    your_choice2 = []
    a = ''
    for i in range(len(str(your_choice))):
        if str(your_choice)[i] != '/' and str(your_choice)[i] != '-':
            a += str(your_choice)[i]
        else:
            your_choice2.append(a)
            a = ''
    your_choice2.append(a)
    for i in your_choice2:
        if i in df1.iloc[[1]]:
            remember = i
            break
        else:
            remember = 'else'
    remember = 'else'
    if remember != 'else':
        plotnost = df1.loc["Плотность", remember]
    else:
        plotnost = df1.loc["Плотность", remember]

    for i in your_choice2:
        if i in df1.iloc[[1]]:
            remember = i
            break
        else:
            remember = 'else'
    remember = 'else'
    if remember != 'else':
        vyazkost = df1.loc["Вязкость при 50С", remember]
    else:
        vyazkost = df1.loc["Вязкость при 50С", remember]
    q = df.loc[your_choice, 'qn' + str(your_choice_year)]
    d = (df.loc[your_choice, 'диаметр'] - 2 * (df.loc[your_choice, 'толщина']))
    renolids = (q) / (math.pi * vyazkost * d * (1 / (10 ** 9)) * 21600)  # скорректировать
    kx = 1.3 * 0.6 * 1 * 1
    p_sr = round((df.loc[your_choice, 'вход'] + df.loc[your_choice, 'выход']) / 2, 3)
    Qg = df.loc[your_choice, 'q' + str(your_choice_year)]
    Gu = Qg / q
    Gr = 1.3 * Gu * p_sr / 22
    T_sr = (df.loc[your_choice, 'tk' + str(your_choice_year)] + 273 + df.loc[
        your_choice, 'tn' + str(your_choice_year)] + 273) / 2
    P_bez_deg_n = plotnost * 1000 - (1.825 - 0.00135 * plotnost * 1000) * (T_sr - 293)
    w = df.loc[your_choice, 'w' + str(your_choice_year)] / 100
    v = df.loc[your_choice, 'v' + str(your_choice_year)]
    Qzh = v * (w / 1000 + (1 - w) / P_bez_deg_n) / 86.4
    Bn = 0.0022 * Gr * P_bez_deg_n * (1 / 10 ** 4) + 0.00075 * (T_sr - 273) * 100 + 0.992
    z = 1 - abs(((df.loc[your_choice, 'вход'] + df.loc[your_choice, 'выход']) * 5 - 6) * 0.0124) * abs(
        1.3 - 0.0144 * (T_sr - 283))
    Qzhr = Qzh * abs((1 - w) * (Bn - 1) + 1)
    Qgr = (1 - w) * Qzh * ((df.loc[your_choice, 'вход'] * T_sr) / (
            p_sr * (df.loc[your_choice, 'tn' + str(your_choice_year)] + 273))) * (Gu - Gr)
    Q_sm = Qzhr + Qgr
    v_smm = round(float(((Q_sm * 4) / (86400 * plotnost * math.pi * d ** 2 * (1 / 10 ** (6)))) * 100000), 3)
    if v_smm > 3.0:
        v_smm = 1.3
    Betta = Qgr / Q_sm
    vkr = round((0.159 / ((1 - w) ** 2) * 9.8 * d * (1 / (10 ** 3))) ** (1 / 2), 3)
    otnoshenie = round(v_smm / vkr, 1)
    massiv = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2]
    d377 = [0.8, 0.4, 0.5, 1.2, 0.6, 0.7, 0.5, 0.9, 0.4, 0.4, 0.08]
    d530 = [0.8, 0.5, 0.7, 0.6, 0.8, 1.5, 0.7, 0.6, 0.6, 0.3, 0.08]
    d531 = [1.0, 0.6, 0.7, 1.0, 1.4, 1.0, 0.6, 0.3, 0.3, 0.3, 0.06]
    if otnoshenie > 1.2:
        kk = 0.06
    elif d <= 377:
        ind = 0
        index = 10000
        for i in massiv:
            if i == otnoshenie:
                index = ind
            ind += 1
        if index == 10000:
            kk = 0.06
        else:
            kk = d377[index]
    elif d > 377 and d <= 530:
        ind = 0
        index = 10000
        for i in massiv:
            if i == otnoshenie:
                index = ind
            ind += 1
        if index == 10000:
            kk = 0.06
        else:
            kk = d530[index]
    elif d > 530:
        ind = 0
        index = 10000
        for i in massiv:
            if i == otnoshenie:
                index = ind
            ind += 1
        if index == 10000:
            kk = 0.06
        else:
            kk = d531[index]
    p_sr_okrug = round(p_sr, 1)
    pp = [0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0]
    kp = [0.6, 0.8, 0.9, 1.0, 1.1, 1.15, 1.2, 1.25, 1.3, 1.3]
    if p_sr_okrug > 2.0:
        kpp = 1.3
    else:
        ind = 0
        index = 10000
        for i in pp:
            if p_sr_okrug == i:
                index = ind
            ind += 1
        if index == 10000:
            kpp = 1.3
        else:
            kpp = kp[index]
    kg = kpp * kk * v_smm
    v_korosia = round(kg * kx, 3)

    ukr = round(7 * (163 / (10 ** 6 * 265)) ** (1 / 3) * (2 * 10 ** 5 * 0.8) ** (1 / 6) * (d) ** (1 / 3), 3)
    if d > 89 and d < 325:
        tmin = 1.5
    if d >= 325 and d < 530:
        tmin = 2
    if d >= 530:
        tmin = 2.5
    df2 = pd.read_excel('ингибируемые.xlsx', index_col=0)
    truba_list = df2.index.tolist()
    if your_choice in truba_list:
        ki = 0.93
    else:
        ki = 1
    n = your_choice_year - df.loc[your_choice, 'год']
    v_korosia_massiv = []
    tost = df.loc[your_choice, 'толщина'] - v_korosia * ki
    N_2 = abs(int((tost - tmin) / (v_korosia * ki * (n - 2))))  # сколько осталось ей работать
    N_god = your_choice_year - df.loc[your_choice, 'год']  # сколько она работает
    if v_korosia > 0.3:
        rezim_tech = "коррозионный"
        if your_choice in truba_list:
            rezim_tech = "коррозионный"
        else:
            rezim_tech = "коррозионный, установите ингибитор"
    else:
        rezim_tech = "антикоррозионный"

    if renolids > 2300:
        rezim = "Турбулентный режим"
    elif renolids > 2100:
        rezim = "Переходный режим"
    if renolids < 2100:
        rezim = "Ламинарный режим"
    Nacop_isnos = abs(
        int(((df.loc[your_choice, 'толщина'] - N_god * v_korosia) / (df.loc[your_choice, 'толщина'])) * 100))
    # Qн-q (т/сут); Qг-Qg(m^3/сут); Qв-v(m^3/сут); P-p_sr(МПа); T-T_sr(°С)
    # режим течения трубопровода rezim, rezim_tech
    # фактическая скорость движения жидкой фазы v_smm (м/с)
    # критическая скорость перехода в расслоенный поток vkr(м/с)
    # накопленный износ Nacop_isnos (%)
    # критическая скорость расслоенного потока ukr(м/с)
    # остаточный ресурс годы N_2 (лет)
    # скорость коррозии v_korosia(мм/год)
    # return(your_choice,your_choice_year,q,rezim,rezim_tech,v_korosia,ukr,vkr,N,Nacop_isnos)
    return (q, Qg, v, round(p_sr,5), round(T_sr,5), rezim +', '+ rezim_tech, '', round(v_smm,5), round(vkr,5), abs(Nacop_isnos), round(ukr,5), N_2, round(v_korosia,5))


def create_figure(your_choice_year):
    # введите имя тут должно быть
    df = pd.read_excel('data.xlsx', index_col=0)
    df1 = pd.read_excel('data_chemical.xlsx', index_col=0)

    name_list = df.index.tolist()
    nacop_isnos_hist = []
    for i in range(len(name_list)):
        your_choice = name_list[i]
        q, Qg, v, p_sr, T_sr, rezim, rezim_tech, v_smm, vkr, Nacop_isnos, ukr, N_2, v_korosia = f(your_choice, your_choice_year, df, df1)
        nacop_isnos_hist.append([Nacop_isnos, your_choice])
        sort = sorted(nacop_isnos_hist)
        sort_new = [sort[i] for i in range(len(sort) - 1, 10, -3)]

    y = []
    x = []
    for i in range(len(sort_new)):
        y.append(sort_new[i][0])
        x.append(sort_new[i][1])

    # Draw plot
    fig, ax = plt.subplots(figsize=(16, 10), facecolor='white', dpi=80)
    ax.vlines(x=x, ymin=0, ymax=y, color='firebrick', alpha=0.7, linewidth=20)

    # Annotate Text
    for i, cty in enumerate(y):
        ax.text(i, cty + 0.5, round(cty, 3), horizontalalignment='center')

    # Title, Label, Ticks and Ylim
    ax.set_title('Трубопроводы с наибольшим накопленным износом в ' + str(your_choice_year) + ' году',
                 fontdict={'size': 22})
    ax.set(ylabel='Накопленный износ, %', ylim=(0, 100))
    plt.xticks(x, rotation=60, horizontalalignment='right', fontsize=12)

    # Add patches to color the X axis labels
    p1 = patches.Rectangle((.57, -0.02), width=.33, height=.13, alpha=.1, facecolor='green', transform=fig.transFigure)
    p2 = patches.Rectangle((.124, -0.02), width=.446, height=.13, alpha=.1, facecolor='red', transform=fig.transFigure)
    fig.add_artist(p1)
    fig.add_artist(p2)

    return plt