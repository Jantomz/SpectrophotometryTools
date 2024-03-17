import pandas as pd
import os
import matplotlib.pyplot as plt
pd.set_option('display.max_rows', None)

class manipulator():
    def __init__(self, folderPath):
        self.data = pd.DataFrame()

        pathList = []
        for root, dirs, files in os.walk(folderPath):
            for file in files:
                pathList.append(os.path.join(root, file))

        for path in pathList:
            data = pd.read_csv(path)
            data = data.iloc[:, [0] + list(range(1, len(data.columns), 2))]
            data.columns = ['rock_id'] + list(data.columns[1:])
            data = data.transpose()
            data.columns = data.iloc[0]
            data.index = [path.split('/')[-1].split('.')[0] + '_' + str(i-1) for i in range(1, len(data)+1)]
            data = data[1:]

            # Cleaning the data by normalizing it
            data = data.div(data.mean(axis=1), axis=0)

            # Averaging out the values a bit more to smooth it out
            data = data.rolling(window=11, center=True, min_periods=1).mean()
            
            # Trimming the data to only include the first 800 columns
            data = data.loc[:, data.columns.map(lambda x: int(x) <= 800)]

            self.data = pd.concat([self.data, data])
        file_paths = [path.split('\\')[-1][:3] for path in pathList]
        unique_file_paths = list(set(file_paths))
        unique_file_paths.sort()
        
        self.data['target'] = self.data.index.map(lambda x: unique_file_paths.index(x.split('\\')[-1][:3]))

    def plot_row(self, row_name):
        row = self.data.loc[row_name]
        row.plot(kind='line')
        plt.xlabel('Columns')
        plt.ylabel('Values')
        plt.title(f'Plot of Row {row_name}')
        plt.show()