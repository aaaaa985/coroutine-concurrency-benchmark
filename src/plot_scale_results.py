import os

import pandas as pd
import matplotlib.pyplot as plt


FIG_DIR = "figures"
os.makedirs(FIG_DIR, exist_ok=True)

py_path = "results/python_asyncio_scale_results.csv"
java_path = "results/java_virtual_scale_results.csv"

py = pd.read_csv(py_path)
java = pd.read_csv(java_path)

py["model"] = "Python asyncio"
java["model"] = "Java virtual thread"

py_sub = py[[
    "model",
    "total_tasks",
    "concurrency",
    "io_ms",
    "total_time_s",
    "qps",
    "avg_latency_ms",
    "p95_latency_ms",
    "p99_latency_ms",
    "peak_memory_mb",
]].copy()

java_sub = java[[
    "model",
    "total_tasks",
    "concurrency",
    "io_ms",
    "total_time_s",
    "qps",
    "avg_latency_ms",
    "p95_latency_ms",
    "p99_latency_ms",
    "used_memory_mb",
]].copy()

java_sub = java_sub.rename(columns={"used_memory_mb": "peak_memory_mb"})

df = pd.concat([py_sub, java_sub], ignore_index=True)

plt.figure()
for model in sorted(df["model"].unique()):
    m = df[df["model"] == model].sort_values("concurrency")
    plt.plot(m["concurrency"], m["qps"], marker="o", label=model)
plt.xlabel("Concurrency")
plt.ylabel("QPS")
plt.title("Scalability observation under 50ms simulated I/O")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(f"{FIG_DIR}/scale_qps.png", dpi=200)
plt.close()

plt.figure()
for model in sorted(df["model"].unique()):
    m = df[df["model"] == model].sort_values("concurrency")
    plt.plot(m["concurrency"], m["peak_memory_mb"], marker="o", label=model)
plt.xlabel("Concurrency")
plt.ylabel("Memory MB")
plt.title("Memory usage in scalability observation")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(f"{FIG_DIR}/scale_memory.png", dpi=200)
plt.close()

plt.figure()
for model in sorted(df["model"].unique()):
    m = df[df["model"] == model].sort_values("concurrency")
    plt.plot(m["concurrency"], m["p95_latency_ms"], marker="o", label=model)
plt.xlabel("Concurrency")
plt.ylabel("P95 Latency ms")
plt.title("P95 latency in scalability observation")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(f"{FIG_DIR}/scale_p95.png", dpi=200)
plt.close()

df.to_csv("results/scale_merged_results.csv", index=False)

print("Scale figures generated in figures/")
print("Merged CSV saved to results/scale_merged_results.csv")