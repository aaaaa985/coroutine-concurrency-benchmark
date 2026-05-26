#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/.."
source venv/bin/activate

mkdir -p results

rm -f results/python_cpu_results.csv

TOTAL=1000
WORK=200000

for CONCURRENCY in 1 2 4 8 16 32 64 100
do
  echo "Running CPU thread: concurrency=${CONCURRENCY}"
  python src/python_cpu_bench.py \
    --mode thread \
    --total ${TOTAL} \
    --concurrency ${CONCURRENCY} \
    --work ${WORK} \
    --output results/python_cpu_results.csv

  echo "Running CPU asyncio: concurrency=${CONCURRENCY}"
  python src/python_cpu_bench.py \
    --mode asyncio \
    --total ${TOTAL} \
    --concurrency ${CONCURRENCY} \
    --work ${WORK} \
    --output results/python_cpu_results.csv
done