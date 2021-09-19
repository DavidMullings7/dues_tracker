import pandas as pd

df = pd.read_csv('/Users/davidmullings/Downloads/Paid Members 2021-2022 - Fall.csv')
df.drop(columns = df.columns[4], inplace=True)
df.drop(index = df.rows[], inplace=True)
print(df)