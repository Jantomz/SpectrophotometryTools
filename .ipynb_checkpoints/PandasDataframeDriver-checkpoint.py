import pandas as pd
pd.set_option('display.max_rows', None)

class manipulator():
    def __init__(self, pathList):
        self.data = pd.DataFrame()
        for path in pathList:
            data = pd.read_csv(path)
            data = data.iloc[:, [0] + list(range(1, len(data.columns), 2))]
            data.columns = ['rock_id'] + list(data.columns[1:])
            data = data.transpose()
            data.columns = data.iloc[0]
            data.index = [path.split('/')[-1].split('.')[0] + '_' + str(i-1) for i in range(1, len(data)+1)]
            data = data[1:]
            self.data = pd.concat([self.data, data])
        self.data['target'] = self.data.index.map(lambda x: 0 if x[0] == 'H' else 1)
