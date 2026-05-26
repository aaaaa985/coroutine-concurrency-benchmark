import os

import pandas as pd
import matplotlib.pyplot as plt


RESULT_PATH = "results/python_results.csv"
FIG_DIR = "figures"

os.makedirs(FIG_DIR, exist_ok=True)

df = pd.read_csv(RESULT_PATH)

for io_ms in sorted(df["io_ms"].unique()):
    sub = df[df["io_ms"] == io_ms]

    plt.figure()
    for mode in sorted(sub["mode"].unique()):
        m = sub[sub["mode"] == mode].sort_values("concurrency")
        plt.plot(m["concurrency"], m["qps"], marker="o", label=mode)
    plt.xlabel("Concurrency")
    plt.ylabel("QPS")
    plt.title(f"Throughput under {io_ms}ms simulated I/O")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{FIG_DIR}/python_qps_io_{io_ms}ms.png", dpi=200)
    plt.close()

    plt.figure()
    for mode in sorted(sub["mode"].unique()):
        m = sub[sub["mode"] == mode].sort_values("concurrency")
        plt.plot(m["concurrency"], m["peak_memory_mb"], marker="o", label=mode)
    plt.xlabel("Concurrency")
    plt.ylabel("Peak RSS Memory MB")
    plt.title(f"Memory usage under {io_ms}ms simulated I/O")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{FIG_DIR}/python_memory_io_{io_ms}ms.png", dpi=200)
    plt.close()

    plt.figure()
    for mode in sorted(sub["mode"].unique()):
        m = sub[sub["mode"] == mode].sort_values("concurrency")
        plt.plot(m["concurrency"], m["p95_latency_ms"], marker="o", label=mode)
    plt.xlabel("Concurrency")
    plt.ylabel("P95 Latency ms")
    plt.title(f"P95 latency under {io_ms}ms simulated I/O")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{FIG_DIR}/python_p95_io_{io_ms}ms.png", dpi=200)
    plt.close()

print("Python figures generated in figures/")