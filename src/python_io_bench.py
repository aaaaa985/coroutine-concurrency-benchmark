import argparse
import asyncio
import concurrent.futures
import csv
import math
import os
import statistics
import time
from typing import List

import psutil


def small_cpu_work(rounds: int) -> int:
    """
    模拟每个请求中少量 CPU 工作。
    rounds 不宜过大，否则实验会变成 CPU 密集型。
    """
    x = 0
    for i in range(rounds):
        x += (i * i) % 97
    return x


def percentile(values: List[float], p: float) -> float:
    if not values:
        return 0.0
    values = sorted(values)
    k = math.ceil(len(values) * p / 100) - 1
    k = max(0, min(k, len(values) - 1))
    return values[k]


def thread_task(io_ms: int, cpu_rounds: int) -> float:
    start = time.perf_counter()
    small_cpu_work(cpu_rounds)
    time.sleep(io_ms / 1000.0)
    end = time.perf_counter()
    return end - start


async def asyncio_task(io_ms: int, cpu_rounds: int) -> float:
    start = time.perf_counter()
    small_cpu_work(cpu_rounds)
    await asyncio.sleep(io_ms / 1000.0)
    end = time.perf_counter()
    return end - start


async def run_asyncio(total_tasks: int, concurrency: int, io_ms: int, cpu_rounds: int):
    sem = asyncio.Semaphore(concurrency)
    latencies = []

    async def wrapped_task():
        async with sem:
            latency = await asyncio_task(io_ms, cpu_rounds)
            latencies.append(latency)

    tasks = [asyncio.create_task(wrapped_task()) for _ in range(total_tasks)]
    await asyncio.gather(*tasks)
    return latencies


def run_threads(total_tasks: int, concurrency: int, io_ms: int, cpu_rounds: int):
    latencies = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = [
            executor.submit(thread_task, io_ms, cpu_rounds)
            for _ in range(total_tasks)
        ]
        for fut in concurrent.futures.as_completed(futures):
            latencies.append(fut.result())
    return latencies


def monitor_memory(stop_flag, interval: float = 0.02):
    process = psutil.Process(os.getpid())
    peak_rss = 0
    while not stop_flag["stop"]:
        rss = process.memory_info().rss
        peak_rss = max(peak_rss, rss)
        time.sleep(interval)
    stop_flag["peak_rss"] = peak_rss


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["thread", "asyncio"], required=True)
    parser.add_argument("--total", type=int, default=10000)
    parser.add_argument("--concurrency", type=int, default=1000)
    parser.add_argument("--io-ms", type=int, default=50)
    parser.add_argument("--cpu-rounds", type=int, default=100)
    parser.add_argument("--output", type=str, default="results/python_results.csv")
    args = parser.parse_args()

    stop_flag = {"stop": False, "peak_rss": 0}

    import threading
    monitor = threading.Thread(target=monitor_memory, args=(stop_flag,), daemon=True)
    monitor.start()

    begin = time.perf_counter()

    if args.mode == "thread":
        latencies = run_threads(
            args.total,
            args.concurrency,
            args.io_ms,
            args.cpu_rounds,
        )
    else:
        latencies = asyncio.run(
            run_asyncio(
                args.total,
                args.concurrency,
                args.io_ms,
                args.cpu_rounds,
            )
        )

    end = time.perf_counter()

    stop_flag["stop"] = True
    monitor.join()

    total_time = end - begin
    qps = args.total / total_time
    avg_latency = statistics.mean(latencies)
    p95_latency = percentile(latencies, 95)
    p99_latency = percentile(latencies, 99)
    peak_memory_mb = stop_flag["peak_rss"] / 1024 / 1024

    row = {
        "mode": args.mode,
        "total_tasks": args.total,
        "concurrency": args.concurrency,
        "io_ms": args.io_ms,
        "cpu_rounds": args.cpu_rounds,
        "total_time_s": total_time,
        "qps": qps,
        "avg_latency_ms": avg_latency * 1000,
        "p95_latency_ms": p95_latency * 1000,
        "p99_latency_ms": p99_latency * 1000,
        "peak_memory_mb": peak_memory_mb,
    }

    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    file_exists = os.path.exists(args.output)
    with open(args.output, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

    print(row)


if __name__ == "__main__":
    main()