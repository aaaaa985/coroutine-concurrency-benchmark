import os

import pandas as pd
import matplotlib.pyplot as plt


RESULT_PATH = "results/python_cpu_results.csv"
FIG_DIR = "figures"

os.makedirs(FIG_DIR, exist_ok=True)

df = pd.read_csv(RESULT_PATH)

plt.figure()
for mode in sorted(df["mode"].unique()):
    m = df[df["mode"] == mode].sort_values("concurrency")
    plt.plot(m["concurrency"], m["qps"], marker="o", label=mode)
plt.xlabel("Concurrency")
plt.ylabel("Tasks per second")
plt.title("CPU-bound workload: ThreadPoolExecutor vs asyncio")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(f"{FIG_DIR}/python_cpu_qps.png", dpi=200)
plt.close()

plt.figure()
for mode in sorted(df["mode"].unique()):
    m = df[df["mode"] == mode].sort_values("concurrency")
    plt.plot(m["concurrency"], m["total_time_s"], marker="o", label=mode)
plt.xlabel("Concurrency")
plt.ylabel("Total time seconds")
plt.title("CPU-bound workload total time")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(f"{FIG_DIR}/python_cpu_total_time.png", dpi=200)
plt.close()

plt.figure()
for mode in sorted(df["mode"].unique()):
    m = df[df["mode"] == mode].sort_values("concurrency")
    plt.plot(m["concurrency"], m["peak_memory_mb"], marker="o", label=mode)
plt.xlabel("Concurrency")
plt.ylabel("Peak RSS Memory MB")
plt.title("CPU-bound workload memory usage")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(f"{FIG_DIR}/python_cpu_memory.png", dpi=200)
plt.close()

print("CPU-bound figures generated in figures/")