import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('outputs\\curves\\island1.csv', sep=";")
print(df.iloc[:, 0])
plt.figure(figsize=(10, 6))
for column in df.columns[1:]:
    plt.plot(df.iloc[:, 0], df[column], label=column)
    plt.xlabel(df.columns[0])
    plt.legend()
    plt.grid()
    plt.show()