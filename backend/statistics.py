import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("outputs/runtime_stats.csv")

print(df.describe())

# Average Speed
plt.figure(figsize=(10,5))
plt.plot(df["step"], df["avg_speed"])
plt.xlabel("Simulation Step")
plt.ylabel("Average Speed (m/s)")
plt.title("Average Speed Over Time")
plt.grid(True)
plt.show()

# Average Waiting Time
plt.figure(figsize=(10,5))
plt.plot(df["step"], df["avg_waiting"])
plt.xlabel("Simulation Step")
plt.ylabel("Average Waiting Time (s)")
plt.title("Average Waiting Time Over Time")
plt.grid(True)
plt.show()

# Queue Length
if "queue_length" in df.columns:

    plt.figure(figsize=(10,5))
    plt.plot(df["step"], df["queue_length"])
    plt.xlabel("Simulation Step")
    plt.ylabel("Queue Length")
    plt.title("Queue Length Over Time")
    plt.grid(True)
    plt.show()

else:
    print("queue_length column not found.")