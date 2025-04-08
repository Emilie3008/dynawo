import pandas as pd
import matplotlib.pyplot as plt

P_gen = ["B1-G1_generator_PGenPu", "B2-G1_generator_PGenPu"]
Q_gen = ["B1-G1_generator_QGenPu", "B2-G1_generator_QGenPu"]
U_gen = ["B1-G1_generator_UPu", "B2-G1_generator_UPu"]
omegaRef = ["B1-G1_generator_omegaRefPu", "B2-G1_generator_omegaRefPu"]

df = pd.read_csv('outputs\\curves\\island2.csv', sep=";")
print(df.iloc[:, 0])
plt.figure(figsize=(10, 6))
for curve in U_gen:
    plt.plot(df.iloc[:, 0], df[curve], label=curve)

plt.xlabel(df.columns[0])
plt.legend()
plt.grid()
plt.show()


P_gen = ["B13-G1_generator_PGenPu", "B22-G1_generator_PGenPu",
          "B23-G1_generator_PGenPu", "B27-G1_generator_PGenPu"]
Q_gen = ["B13-G1_generator_QGenPu", "B22-G1_generator_QGenPu",
         "B23-G1_generator_QGenPu", "B27-G1_generator_QGenPu"]
U_gen = ["B13-G1_generator_UPu", "B22-G1_generator_UPu",
         "B23-G1_generator_UPu", "B27-G1_generator_UPu"]
omegaRef = ["B13-G1_generator_omegaRefPu", "B22-G1_generator_omegaRefPu",
            "B23-G1_generator_omegaRefPu", "B27-G1_generator_omegaRefPu"]

df = pd.read_csv('outputs\\curves\\island1.csv', sep=";")
print(df.iloc[:, 0])
plt.figure(figsize=(10, 6))
for curve in Q_gen:
    plt.plot(df.iloc[:, 0], df[curve], label=curve)

plt.xlabel(df.columns[0])
plt.legend()
plt.grid()
plt.show()