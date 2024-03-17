import csv
import numpy as np
import pandas as pd

class datasets():
    def __init__(self):
        self.data = np.array([])
        self.target = np.array([])
        self.target_names = ['Fluorite', 'Hematite']
        self.feature_names = np.array([])

    def load_data(self, dataPathList, targetTypeList):
        self.feature_names = np.swapaxes(np.asarray(pd.read_csv(dataPathList[0])), 0, 1)[0, :]
        
        for i in range(0, len(dataPathList)):
            tempData = np.swapaxes(np.asarray(pd.read_csv(dataPathList[i])), 0, 1)
            for j in range(0, int(tempData.shape[0] / 2)):
                tempData = np.delete(tempData, j, 0)
                self.target = np.append(self.target, targetTypeList[i])

    
            if (i == 0):
                self.data = tempData
            else: 
                self.data = np.concatenate((self.data, tempData), axis=0)

        print(self.data.shape)
        print(self.target.shape)
        print(self.target)
        print(self.data)
        print(self.feature_names)

    def __str__(self):
        return f"data: {self.data}\nfeature names: {self.feature_names}\ntarget: {self.target}\ntarget names: {self.target_names}"
   