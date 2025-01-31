# -*- coding: utf-8 -*-
"""cappelchi_functions.ipynb

@author: Mikhail Kosaretskiy
"""

import numpy as np
import pandas as pd
from tqdm import tqdm

def short_label_equity(df, TakeUp, TrailDown, setY = False):
    #warnings.simplefilter(action='ignore', category=FutureWarning)
    # df - DataFrame with OHLC, Open, High, Low, Close
    # TakeUp - Take profit in form 1 + (% expected profit) / 100
    # TrailDown - Max Drawdown in form 1 +(% max drawdown) / 100
    # setY set to True if need labaling
    # return:
    # i -  bars calculated
    # Trades - max potential trades counted 
    # Profit - max potential profit calculated
    # Y - pd.series with labels for prediction
    
    CurLow = Low1 = df.at[0, 'Low']
    CurHigh = High1 = High2 = df.at[0, 'High']
    LowChange = HighChange = High2Chang = 0
    Flag = LowI = HighI = 0
    HPrI = df.at[0, 'High']
    LPrI = df.at[0, 'Low']
    HMark = np.zeros (np.shape(df)[0])
    HMark2 = np.zeros (np.shape(df)[0])
    LMark = np.zeros (np.shape(df)[0])
    Y = pd.Series(df.index)
    Y[:] = 0
    Profit = Trades = 0
        
    for i in range(1, np.shape(df)[0]):
        if df.at[i, 'Low'] and df.at[i, 'High']:
            CurLow = df.at[i, 'Low']
            CurHigh = df.at[i, 'High']
            if CurLow < Low1:
                LowChange = 1
            if CurHigh > High1:
                HighChange = 1
            if CurHigh > High2:
                High2Change = 1     
            if not Flag:
                if LowChange:
                    Low1 = CurLow
                    if High1 / Low1 > TakeUp:
                        LowI = i
                        LPrI = CurLow
                        High2 = CurHigh
                        Flag = 2
                    elif High1 /Low1 > TrailDown:
                        High2 = Low1 * TrailDown
                        Flag = 1

                if HighChange:
                    High1 = HPrI = CurHigh
                    HighI = i
                    if High1 / Low1 > TrailDown:
                        Low1 = CurLow
            elif Flag == 1:                    
                if LowChange:
                    Low1 = CurLow
                    High2 = Low1 * TrailDown
                    if High1 / Low1 > TakeUp:
                        LowI = i
                        LPrI = CurLow
                        High2 = CurHigh
                        Flag = 2

                if HighChange:
                    High = CurHigh
                    if High1 / Low1 > TrailDown:
                        HighI = i
                        HPrI = High1 = High2 = CurHigh
                        Low1 = CurLow
                        Flag = 0
                if High2Change:
                    High2 = CurHigh
                    if High2 / Low1 > TrailDown:
                        HMark2[i] = High2
                        Low1 = LPrI = CurLow
                        High1 = High2 = HPrI = CurHigh
                        LowI = HighI = i
                        Flag = 0

            elif Flag == 2:
                if LowChange:
                    Low1 = CurLow
                    if High1 / Low1 > TakeUp:
                        LowI = i
                        LPrI = CurLow
                        High2 = CurHigh

                if High2Change:
                    High2 = CurHigh
                    if High2 / Low1 > TrailDown:
                        LMark[LowI] = LPrI
                        HMark[HighI] = HPrI
                        HMark2[i] = High2
                        Profit = Profit + (HPrI - LPrI)
                        Trades = Trades + 1
                        if setY:
                            for j in range(HighI, LowI + 1):
                                Y[j] = 1
                        High1 = High2 = HPrI = CurHigh
                        Low1 = LPrI = CurLow
                        LowI = HighI = i
                        Flag = 0
            High2Change = 0
            HighChange = 0
            LowChange = 0
                    
                    
    return i, Profit, Trades, Y
'''
TakeUp = 1.098 #@param {type:"number"}
TrailDown = 1.025 #@param {type:"number"}
Labeling = True #@param ["True", "False"] {type:"raw"}
Bars, Prft, Trds, Y = short_label_equity(df, TakeUp, TrailDown, setY = Labeling)
print()
print('Результаты разметки')
print (f'TakeUp = {TakeUp}, TrailDown = {TrailDown}')
print(f'Кол-во бар просмотрено = {Bars}, Прибыль на 1$ входа = {Prft}')
print (f'Потенциальных сделок = {Trds}, Размечено бар = {Y.sum()}')                            
df['Y'] = pd.Series(Y.values, index = df.index) 
'''

def long_label_equity(df, TakeUp, TrailDown, setY = False):
    #warnings.simplefilter(action='ignore', category=FutureWarning)
    # df - DataFrame with OHLC, Open, High, Low, Close
    # TakeUp - Take profit in form 1 + (% expected profit) / 100
    # TrailDown - Max Drawdown in form 1 +(% max drawdown) / 100
    # setY set to True if need labaling
    # return:
    # i -  bars calculated
    # Trades - max potential trades counted 
    # Profit - max potential profit calculated
    # Y - pd.series with labels for prediction
    CurHigh = High1 = df.at[0, 'High']
    CurLow = Low1 = Low2 = df.at[0, 'Low']    
    LowChange = Low2Change = HighChange = 0
    Flag = LowI = HighI = 0
    HPrI = df.at[0, 'High']
    LPrI = df.at[0, 'Low']
    HMark = np.zeros (np.shape(df)[0])
    LMark = np.zeros (np.shape(df)[0])
    LMark2 = np.zeros (np.shape(df)[0])
    Y = pd.Series(df.index)
    Y[:] = 0
    Profit = Trades = 0
    '''
    trace.append(dict(
                    id = i,
                    event ='',
                    flg = Flag,                    
                    hich = HighChange,
                    loch = LowChange,
                    lo2ch = Low2Change,
                    chigh = CurHigh,
                    clow = CurLow,
                    cond = High1 / Low1
                    conf = Takeup
                    )                
                )
    
    df['HighChange'] =  df['LowChange'] =  df['Low2Change'] = 0
    df['Flag_in'] = 0
    df['Low1'] = df['Low2'] = df['High1'] = 0
    df['HighI'] = df['LowI'] = df['LPrI'] = df['HPrI'] = 0
    '''
    for i in range(1, np.shape(df)[0]):
        if df.at[i, 'Low'] and df.at[i, 'High']:        
            CurLow = df.at[i, 'Low']
            CurHigh = df.at[i, 'High']
            if CurHigh > High1:
                HighChange = 1                
            if CurLow < Low1:
                LowChange = 1                
            if CurLow < Low2:
                Low2Change = 1  
            '''
            df.at[i, 'Flag_in'] = Flag
            df.at[i, 'HighChange'] = HighChange
            df.at[i, 'LowChange'] = LowChange
            df.at[i, 'Low2Change'] = Low2Change
            df.at[i, 'Low1'] = Low1
            df.at[i, 'Low2'] = Low2
            df.at[i, 'High1'] = High1
            df.at[i, 'LowI'] = LowI
            df.at[i, 'HighI'] = HighI
            df.at[i, 'HPrI'] = HPrI
            df.at[i, 'LPrI'] = LPrI
            '''
            if not Flag:
                if HighChange:
                    High1 = CurHigh
                    if High1 / Low1 > TakeUp:                        
                        HighI = i
                        HPrI = CurHigh
                        Low2 = CurLow
                        Flag = 2
                    elif High1 /Low1 > TrailDown:
                        Low2 = High1 * (2 - TrailDown)
                        Flag = 1

                if LowChange:
                    Low1 = LPrI = CurLow
                    LowI = i
                    if High1 / Low1 > TrailDown:
                        High1 = CurHigh
            elif Flag == 1:                    
                if HighChange:
                    High1 = CurHigh
                    Low2 = High1 * (2 - TrailDown)
                    if High1 / Low1 > TakeUp:
                        HighI = i
                        HPrI = CurLow
                        Low2 = CurLow
                        Flag = 2

                if LowChange:
                    Low1 = CurLow
                    if High1 / Low1 > TrailDown:
                        LowI = i
                        LPrI = Low1 = Low2 = CurLow
            ##продолжить здесь
            ##################                        
                        High1 = CurHigh
                        Flag = 0
                if Low2Change:
                    Low2 = CurLow
                    if High1 / Low2 > TrailDown:
                        LMark2[i] = Low2
                        High1 = HPrI = CurHigh
                        Low1 = Low2 = LPrI = CurLow
                        LowI = HighI = i
                        Flag = 0

            elif Flag == 2:
                if HighChange:
                    High1 = CurHigh
                    if High1 / Low1 > TakeUp:
                        HighI = i
                        HPrI = CurHigh
                        Low2 = CurLow

                if Low2Change:
                    Low2 = CurLow
                    if High1 / Low2 > TrailDown:
                        HMark[LowI] = HPrI
                        LMark[HighI] = LPrI
                        LMark2[i] = Low2
                        Profit = Profit + (HPrI - LPrI)
                        Trades = Trades + 1
                        if setY:
                            for j in range(LowI, HighI + 1):
                                Y[j] = 1
                        Low1 = Low2 = LPrI = CurLow
                        High1 = HPrI = CurHigh
                        LowI = HighI = i
                        Flag = 0
            
            Low2Change = 0
            HighChange = 0
            LowChange = 0
                    
                    
    return i, Profit, Trades, Y

#@title Параметры разметки { vertical-output: true }
def TFSelect (TakeUp, TrailDown, df, setY = False):
    #Функция размечает только шорты
    
    # СТАРАЯ ВЕРСИЯ
    
    LArr = np.shape(df.Open)
    HMark = np.zeros (LArr)    # массивы в котором сохраняются Тейковые хаи в позицию бара (размер массива = кол-ву баров), остальные значения  = 0
    LMark = np.zeros (LArr)    # ---||----
    HMark2 = np.zeros (LArr)   # ---||----
    Y = pd.Series(df.index)
    
    Y[:] = 0
    HighChange = 0  # Флаг появления локального максимума в текущем баре
    LowChange = 0   # Флаг появления локального минимума в текущем баре
    Low2Change = 0  # Флаг наличия траэйл просадки от локального максимуму, флаг на сброс
    High2Change = 0 # Флаг наличия траэйл просадки от локального максимума, флаг на сброс,  если разметка в лонг
    HPrI = 0        # Запоминаем котировку последнего локального максимма
    HighI = 0       #(номер бара последнего локально максимума)
    LPrI = 0        # Запоминаем котировку последнего локального минимума
    LowI = 0        # (номер бара последнего локально минимума)
    Flag = 0        # Флаг состояния, 0- начальное состояние, 1 - текущая прибыль прошла барьер максимальной просадки (нужно, т.к. если просадка большая переходим в состояние 1)
                    # Текущая прибыль достигла минимального тейка
    Profit = 0
    Trades = 0
    Low1 = df.Low[0]
    Low2 =df.Low[0]
    High1 = df.High[0]
    High2 = df.High[0]
    #dtind = df.index[0]

    for count, op in tqdm(enumerate(df['Open'])):
    #for count in range(0, 1000):
        #pdb.set_trace()
        
        if df.Low[count] < Low1:
            LowChange = 1
            #pdb.set_trace()
        if df.High[count] > High1:
            HighChange = 1
            #pdb.set_trace()
        if df.High[count] >High2:
            High2Change = 1
            #pdb.set_trace()
        if not Flag:
            if LowChange:
                Low1 = df.Low[count]
                if High1 / Low1 > TakeUp:
                    #print (f'point1: Low1 = {Low1}, High1/Low1 = {High1/Low1} \
                    #TakeUp = {TakeUp}, Count = {count}')
                    LowI = count
                    LPrI = df.Low[count]
                    High2 = df.High[count]
                    Flag = 2
                elif High1 / Low1 > TrailDown: # активируем проверку на просадку, после прохода на % просадки                    
                    #High2 = df.High[count]
                    High2 = Low1 * TrailDown
                    Flag = 1
                    
            if HighChange:
                High1 = df.High[count]
                HighI = count
                HPrI = df.High[count]
                if High1 / Low1 > TrailDown:
                    Low1 = df.Low[count]
            
        elif Flag == 1:
            if LowChange:
                Low1 = df.Low[count]
                ########
                High2 = Low1 * TrailDown
                if High1 / Low1 > TakeUp:
                    #print('point2')
                    LowI = count
                    LPrI = df.Low[count]
                    High2 = df.High[count]
                    Flag = 2
                    
            if HighChange:
                High1 = df.High[count]
                if High1 / Low1 > TrailDown:
                    HighI = count
                    HPrI = df.High[count]
                    Low1 = df.Low[count]
                    High1 = df.High[count]
                    High2 = df.High[count]
                    Flag = 0
            if High2Change:
                High2 = df.High[count]
                if High2 / Low1 > TrailDown:                       
                    Low1 = df.Low[count]
                    High1 = df.High[count]
                    High2 = df.High[count]
                    HMark2[count] = High2                    
                    Flag = 0
                    #######
                    LPrI = df.Low[count]
                    HPrI = df.High[count]
                    LowI = count
                    HighI = count
                    
        elif Flag == 2:
            if LowChange:
                Low1 = df.Low[count]
                if High1 / Low1 > TakeUp:
                    #print (f'point3: Low1 = {Low1}, High1/Low1 = {High1/Low1} \
                    #TakeUp = {TakeUp}, Count = {count}')
                    LowI = count
                    LPrI = df.Low[count]
                    High2 = df.High[count]
                        
            if High2Change:
                High2 = df.High[count]
                if High2 / Low1 > TrailDown:
                    #print (f'point3D: High2 = {High2}, High2/Low1 = {High2/Low1} \
                    #TrailDown = {TrailDown}')
                    LMark[LowI] = LPrI
                    HMark[HighI] = HPrI
                    HMark2[count] = High2
                    Profit = Profit + (HPrI - LPrI)
                    Trades = Trades + 1
                    if setY:                       
                        for i in range(HighI, LowI+1):
                            Y[i] = 1
                       
                    High1 = df.High[count]
                    Low1 = df.Low[count]
                    High2 = df.High[count]
                    LowI = count
                    LPrI = df.Low[count]
                    HighI = count
                    HPrI = df.High[count]
                    Flag = 0
                        
        High2Change = 0
        HighChange = 0
        LowChange = 0
    return count, Profit, Trades, Y
'''
TakeUp = 1.098 #@param {type:"number"}
TrailDown = 1.025 #@param {type:"number"}
Labeling = True #@param ["True", "False"] {type:"raw"}
Bars, Prft, Trds, Y = TFSelect(TakeUp, TrailDown, df, setY = Labeling)
print()
print('Результаты разметки')
print (f'TakeUp = {TakeUp}, TrailDown = {TrailDown}')
print(f'Кол-во бар просмотрено = {Bars}, Прибыль на 1$ входа = {Prft}')
print (f'Потенциальных сделок = {Trds}, Размечено бар = {Y.sum()}')                            
df['Y'] = pd.Series(Y.values, index = df.index) 
df.head()
'''

def get_rollover(df, df_OHLC, timeR = True, line_color = 'rgb(55, 128, 191)',\
                 line_width = 1, line_dash = 'dot'):
    if timeR:        
        values = df[(df.Rollover_date_based == 1)]
    else:
        values = df[(df.Rollover_volume_based == 1)]
        
    shape = []
    annotations = []
    line_color = line_color
    line_width = line_width
    line_dash = line_dash
    if timeR:
        
        for value, text in zip(values.index, values.Name_date):
            #print (value, text)
            shape.append(dict(
                                type = 'line',
                                x0 = value,
                                y0 = df_OHLC.Low.min() - 10,
                                x1 = value,
                                y1 = df_OHLC.High.max(),
                                line = dict(
                                            color = line_color,
                                            width = line_width,
                                            dash = line_dash
                                            )                        
                             )        
                        )
            annotations.append(dict(
                                text = text,
                                x = value,                       
                                y = df_OHLC.loc[value].High,                                          
                                   )        
                              )
    else:
        for value, text in zip(values.index, values.Name_vol):
            #print (value, text)
            shape.append(dict(
                                type = 'line',
                                x0 = value,
                                y0 = df_OHLC.Low.min() - 10,
                                x1 = value,
                                y1 = df_OHLC.High.max(),
                                line = dict(
                                            color = line_color,
                                            width = line_width,
                                            dash = line_dash
                                            )                        
                             )        
                        )
            annotations.append(dict(
                                text = text,
                                x = value,                       
                                y = df_OHLC.loc[value].High,                                          
                                   )        
                              )
    return shape, annotations

def invert_ts(df, offset = False):
    # переворачиваем котировку (аугментируем)
    invert = pd.DataFrame()
    offset = offset
    last = np.shape(df)[0]
    
    op = df.at[0, 'Open']
    hp = df.at[0, 'High']
    lp = df.at[0, 'Low']
    cp = df.at[0, 'Close']
    vp = df.at[0, 'Volume']
    
    h = hp
    l = lp
    o = op
    c = cp
    
    if offset:
        invert.at[0, 'Open'] = df.at[last - 1, 'Open']
        invert.at[0, 'High'] = df.at[last -1, 'High']
        invert.at[0, 'Low'] = df.at[last - 1, 'Low']
        invert.at[0, 'Close'] = df.at[last - 1, 'Close']
        invert.at[0, 'Volume'] = df.at[last - 1, 'Volume']
        
    else:
        invert.at[0, 'Open'] = op
        invert.at[0, 'High'] = hp
        invert.at[0, 'Low'] = lp
        invert.at[0, 'Close'] = cp
        invert.at[0, 'Volume'] = vp
    

    
    for i in tqdm(range(1, np.shape(df)[0])):
        hp = h
        lp = l
        op = o
        cp = c
        
        h = df.at[i, 'High'] 
        l = df.at[i, 'Low']
        o = df.at[i, 'Open']
        c = df.at[i, 'Close']
        
        invert.at[i, 'High'] = hr = invert.at[i - 1, 'High'] * lp / l
        invert.at[i, 'Low'] = lr = invert.at[i - 1, 'Low'] * hp /  h        
        invert.at[i, 'Open'] = l * hr / o
        invert.at[i, 'Close'] = l * hr / c
        invert.at[i, 'Volume'] = df.at[i, 'Volume']
        
    return invert
