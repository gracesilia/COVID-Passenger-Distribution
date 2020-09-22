import pandas as pd
import numpy as np
import csv
from io import StringIO

def read_csv(file_path):
    """read_csv ver panda"""
    """col_list = ["Case_Num", "Month", "Date", "Country1", "Country2", "Country3", "Country4"]
    pddata = pd.read_csv(file_path, usecols=col_list)
    print(pddata["Case_Num"])
    print(pddata["Month"])
    print(pddata["Date"])
    print(pddata["Country1"])
    print(pddata["Country2"])
    print(pddata["Country3"])
    print(pddata["Country4"])"""

    """read_csv ver numpy"""
    """data = open(file_path , "r")
    x = data.read()
    data.close()
    tmpdata = np.genfromtxt(StringIO(x) , delimiter= ',')
    casenum = np.array(tmpdata[: , 0] , dtype = int)
    casemonth = np.array(tmpdata[: , 1] , dtype = int)
    casedate = np.array(tmpdata[: , 2] , dtype = int)    
    print(casenum)
    print(casemonth)
    print(casedate)
    print(tmpdata[: , 3])"""

    """read_csv ver csv"""
    with open(file_path, newline='') as datafile:
        data = csv.reader(datafile)
        data = list(data)
        return data