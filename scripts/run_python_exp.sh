#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/.."
source venv/bin/activate

mkdir -p results

rm -f results/python_results.csv

TOTAL=10000
CPU_ROUNDS=100

for IO_MS in 10 50 100
do
  for CONCURRENCY in 100 500 1000 2000 3000
  do
    echo "Running thread: io=${IO_MS}ms concurrency=${CONCURRENCY}"
    python src/python_io_bench.py \
      --mode thread \
      --total ${TOTAL} \
      --concurrency ${CONCURRENCY} \
      --io-ms ${IO_MS} \
      --cpu-rounds ${CPU_ROUNDS} \
      --output results/python_results.csv

    echo "Running asyncio: io=${IO_MS}ms concurrency=${CONCURRENCY}"
    python src/python_io_bench.py \
      --mode asyncio \
      --total ${TOTAL} \
      --concurrency ${CONCURRENCY} \
      --io-ms ${IO_MS} \
      --cpu-rounds ${CPU_ROUNDS} \
      --output results/python_results.csv
  done
done