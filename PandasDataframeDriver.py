import pandas as pd
import os
import matplotlib.pyplot as plt
# pd.set_option('display.max_rows', None)

class manipulator():
    """
    A class for manipulating and analyzing data using Pandas DataFrame.
    """

    def __init__(self, folderPath, calibrationFolderPath=None, csvDatasetName=None):
        """
        Initializes the manipulator object.

        Parameters:
        - folderPath (str): The path to the folder containing the data files.
        - calibrationFolderPath (str, optional): The path to the folder containing the calibration data files.
        """
        self.data = pd.DataFrame()
        if calibrationFolderPath is not None:
            self.load_calibrated_data(folderPath, calibrationFolderPath)
        else:
            self.load_data(folderPath)

        if csvDatasetName is not None:
            csvData = self.data.copy()
            csvData.reset_index(inplace=True)
            csvData.to_csv(os.path.join('PresetDatasets', csvDatasetName), index=False)

    def load_calibrated_data(self, folderPath, calibrationFolderPath):
        """
        Loads and processes the calibrated data.

        Parameters:
        - folderPath (str): The path to the folder containing the data files.
        - calibrationFolderPath (str): The path to the folder containing the calibration data files.
        """

        variation = [0.9, 1, 1.1]

        pathList = []
        for root, dirs, files in os.walk(folderPath):
            for file in files:
                pathList.append(os.path.join(root, file))

        calibrationPathList = []
        for root, dirs, files in os.walk(calibrationFolderPath):
            for file in files:
                calibrationPathList.append(os.path.join(root, file))

        for calibrationPath in calibrationPathList:
            if not calibrationPath.endswith('.csv'):
                continue
            calibrationData = pd.read_csv(calibrationPath)
            calibrationData = calibrationData.iloc[:, [0] + list(range(1, len(calibrationData.columns), 2))]
            calibrationData.columns = ['rock_id'] + list(calibrationData.columns[1:])
            calibrationData = calibrationData.transpose()
            calibrationData.columns = calibrationData.iloc[0]
            calibrationData.index = [calibrationPath.split('/')[-1].split('.')[0] + '_' + str(i-1) for i in range(1, len(calibrationData)+1)]
            calibrationData = calibrationData[1:]

        for multiplier in variation:
            for calibrationRow in calibrationData.iterrows():
                row = calibrationRow[1]
                row_index = calibrationRow[0].split('_')[1]

                for path in pathList:
                    if not path.endswith('.csv'):
                        continue
                    data = pd.read_csv(path)
                    data = data.iloc[:, [0] + list(range(1, len(data.columns), 2))]
                    data.columns = ['rock_id'] + list(data.columns[1:])
                    data = data.transpose()
                    data.columns = data.iloc[0]
                    data.index = [path.split('/')[-1].split('.')[0] + '_' + str(row_index) + '_' + str(multiplier) + '_' + str(i-1) for i in range(1, len(data)+1)]
                    data = data[1:]

                    # Calibration Divide for the white paper
                    data = data.div(row, axis=1)

                    # Averaging out the values a bit more to smooth it out
                    data = data.rolling(window=11, center=True, min_periods=1).mean()
                    
                    # Trimming the data to only include the first 800 columns
                    data = data.loc[:, data.columns.map(lambda x: int(x) <= 800)]

                    # Multiplier for the variance
                    data = data.mul(multiplier)

                    # Divide every data point in the row by the mean value of the row
                    data = data.div(data.mean(axis=1), axis=0)

                    self.data = pd.concat([self.data, data])


        file_paths = [path.split('\\')[-1][:3] for path in pathList]
        unique_file_paths = list(set(file_paths))
        unique_file_paths.sort()
        

        self.data['target'] = self.data.index.map(lambda x: unique_file_paths.index(x.split('\\')[-1][:3]))


    def load_data(self, folderPath):
        """
        Loads and processes the data.

        Parameters:
        - folderPath (str): The path to the folder containing the data files.
        """
        pathList = []
        for root, dirs, files in os.walk(folderPath):
            for file in files:
                pathList.append(os.path.join(root, file))

        for path in pathList:
            if not path.endswith('.csv'):
                continue
            data = pd.read_csv(path)
            data = data.iloc[:, [0] + list(range(1, len(data.columns), 2))]
            data.columns = ['rock_id'] + list(data.columns[1:])
            data = data.transpose()
            data.columns = data.iloc[0]
            data.index = [path.split('/')[-1].split('.')[0] + '_' + str(i-1) for i in range(1, len(data)+1)]
            data = data[1:]

            # Averaging out the values a bit more to smooth it out
            data = data.rolling(window=11, center=True, min_periods=1).mean()

            # Divide every data point in the row by the mean value of the row
            data = data.div(data.mean(axis=1), axis=0)
            
            # Trimming the data to only include the first 800 columns
            data = data.loc[:, data.columns.map(lambda x: int(x) <= 800)]


            self.data = pd.concat([self.data, data])
        file_paths = [path.split('\\')[-1][:3] for path in pathList]
        unique_file_paths = list(set(file_paths))
        unique_file_paths.sort()
        
        self.data['target'] = self.data.index.map(lambda x: unique_file_paths.index(x.split('\\')[-1][:3]))

    def plot_rows(self, row_names):
        """
        Plots the specified rows.

        Parameters:
        - row_names (list): A list of row names to plot.
        """
        for row_name in row_names:
            row = self.data.loc[row_name]
            
            # removes the target column
            row = row.iloc[:-1]
            
            row.plot(kind='line')
            plt.xlabel('Columns')
            plt.ylabel('Values')
            plt.title(f'Plot of Row {row_name}')
            plt.show()
            