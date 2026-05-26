#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/.."
source venv/bin/activate

mkdir -p results

rm -f results/python_asyncio_scale_results.csv

TOTAL=20000
IO_MS=50
CPU_ROUNDS=100

for CONCURRENCY in 1000 2000 3000 5000 8000 10000
do
  echo "Running asyncio scale: concurrency=${CONCURRENCY}"
  python src/python_io_bench.py \
    --mode asyncio \
    --total ${TOTAL} \
    --concurrency ${CONCURRENCY} \
    --io-ms ${IO_MS} \
    --cpu-rounds ${CPU_ROUNDS} \
    --output results/python_asyncio_scale_results.csv
done