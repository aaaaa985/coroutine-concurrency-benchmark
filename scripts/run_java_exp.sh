#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/.."

mkdir -p results

rm -f results/java_results.csv

echo "mode,total_tasks,concurrency,io_ms,total_time_s,qps,avg_latency_ms,p95_latency_ms,p99_latency_ms,used_memory_mb" > results/java_results.csv

TOTAL=10000
CPU_ROUNDS=100

javac src/JavaThreadBench.java

for IO_MS in 50
do
  for CONCURRENCY in 100 500 1000 2000 3000
  do
    echo "Running platform thread: io=${IO_MS}ms concurrency=${CONCURRENCY}"
    java -cp src JavaThreadBench platform ${TOTAL} ${CONCURRENCY} ${IO_MS} ${CPU_ROUNDS} | tail -n 1 >> results/java_results.csv

    echo "Running virtual thread: io=${IO_MS}ms concurrency=${CONCURRENCY}"
    java -cp src JavaThreadBench virtual ${TOTAL} ${CONCURRENCY} ${IO_MS} ${CPU_ROUNDS} | tail -n 1 >> results/java_results.csv
  done
done