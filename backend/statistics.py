import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("outputs/runtime_stats.csv")

print(df.describe())

plt.plot(df["step"], df["avg_speed"])
plt.xlabel("Simulation Step")
plt.ylabel("Average Speed")
plt.title("Traffic Speed Over Time")
plt.show()