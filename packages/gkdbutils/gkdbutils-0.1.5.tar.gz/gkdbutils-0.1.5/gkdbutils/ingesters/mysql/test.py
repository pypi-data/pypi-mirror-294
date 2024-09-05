import pandas as pd
from gkutils.commonutils import readGenericDataFile

columns = open('tcs_transient_objects_columns.csv').readlines()[0].strip().split(',')
filename = 'tcs_transient_objects_pandas.csv'
data = pd.read_csv(filename, names=columns, dtype='string', quotechar='"', sep=',', escapechar='\\', keep_default_na=False)
print(data[['id', 'observation_status']].head(200))

datadict = data.to_dict('records')
for row in datadict:
    print(row['observation_status'])
