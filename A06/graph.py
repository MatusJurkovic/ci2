import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('graph.csv', sep=';', decimal=',')
plt.figure(figsize=(8, 4))
plt.plot(df.iloc[:, 0], df.iloc[:, 1], marker='o', color='royalblue', linewidth=2)
plt.ylim(-1.2, 1.2)
plt.axhline(0, color='black', linewidth=1, linestyle='--')
plt.xlabel(df.columns[0])
plt.ylabel(df.columns[1])
plt.title('Y = cos(X)')
plt.grid(True, alpha=0.3)
plt.savefig('graph.png', dpi=300, bbox_inches='tight')
plt.show()