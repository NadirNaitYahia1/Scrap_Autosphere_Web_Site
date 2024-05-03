import pandas as pd

df1 = pd.read_csv('datasets/data1.csv')
df2 = pd.read_csv('datasets/data2.csv')
df3 = pd.read_csv('datasets/data3.csv')
df4 = pd.read_csv('datasets/data4.csv')
df5 = pd.read_csv('datasets/data5.csv')
df6 = pd.read_csv('datasets/data6.csv')


# Créer une liste contenant tous les ensembles de données
datasets = [df1, df2, df3, df4, df5,df6]

# Concaténer les ensembles de données en un seul DataFrame
concatenated_df = pd.concat(datasets, ignore_index=True)
concatenated_df.to_csv('dataset.csv', index=False)