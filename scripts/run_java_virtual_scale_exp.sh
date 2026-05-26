#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/.."

mkdir -p results

rm -f results/java_virtual_scale_results.csv

echo "mode,total_tasks,concurrency,io_ms,total_time_s,qps,avg_latency_ms,p95_latency_ms,p99_latency_ms,used_memory_mb" > results/java_virtual_scale_results.csv

TOTAL=20000
IO_MS=50
CPU_ROUNDS=100

javac src/JavaThreadBench.java

for CONCURRENCY in 1000 2000 3000 5000 8000 10000
do
  echo "Running Java virtual thread scale: concurrency=${CONCURRENCY}"
  java -cp src JavaThreadBench virtual ${TOTAL} ${CONCURRENCY} ${IO_MS} ${CPU_ROUNDS} | tail -n 1 >> results/java_virtual_scale_results.csv
done