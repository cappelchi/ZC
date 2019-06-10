# -*- coding: utf-8 -*-
"""
Created on Mon Jun 10 05:57:04 2019

@author: Mikhail Kosaretskiy
"""
import numpy as np
import pandas as pd
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
    HPrI = LPrI = 0
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
    HPrI = LPrI = 0
    HMark = np.zeros (np.shape(df)[0])
    LMark = np.zeros (np.shape(df)[0])
    LMark2 = np.zeros (np.shape(df)[0])
    Y = pd.Series(df.index)
    Y[:] = 0
    Profit = Trades = 0
        
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
                if LowChange:
                    High1 = CurHigh
                    if High1 / Low1 > TakeUp:
                        HighI = i
                        HPrI = CurHigh
                        Low2 = CurLow

                if Low2Change:
                    Low2 = CurLow
                    if High2 / Low1 > TrailDown:
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
