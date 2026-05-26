package src;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.*;

public class JavaThreadBench {
    static class Result {
        String mode;
        int totalTasks;
        int concurrency;
        int ioMs;
        double totalTimeS;
        double qps;
        double avgLatencyMs;
        double p95LatencyMs;
        double p99LatencyMs;
        double usedMemoryMb;

        @Override
        public String toString() {
            return String.format(
                "%s,%d,%d,%d,%.6f,%.2f,%.3f,%.3f,%.3f,%.3f",
                mode, totalTasks, concurrency, ioMs, totalTimeS, qps,
                avgLatencyMs, p95LatencyMs, p99LatencyMs, usedMemoryMb
            );
        }
    }

    static void smallCpuWork(int rounds) {
        long x = 0;
        for (int i = 0; i < rounds; i++) {
            x += (long) (i * i) % 97;
        }
    }

    static double percentile(List<Double> values, double p) {
        Collections.sort(values);
        int k = (int) Math.ceil(values.size() * p / 100.0) - 1;
        k = Math.max(0, Math.min(k, values.size() - 1));
        return values.get(k);
    }

    static Result runBench(String mode, int totalTasks, int concurrency, int ioMs, int cpuRounds) throws Exception {
        ExecutorService executor;

        if (mode.equals("platform")) {
            executor = Executors.newFixedThreadPool(concurrency);
        } else if (mode.equals("virtual")) {
            executor = Executors.newVirtualThreadPerTaskExecutor();
        } else {
            throw new IllegalArgumentException("mode must be platform or virtual");
        }

        Semaphore semaphore = new Semaphore(concurrency);
        List<Future<Double>> futures = new ArrayList<>();

        long begin = System.nanoTime();

        for (int i = 0; i < totalTasks; i++) {
            futures.add(executor.submit(() -> {
                semaphore.acquire();
                try {
                    long start = System.nanoTime();
                    smallCpuWork(cpuRounds);
                    Thread.sleep(ioMs);
                    long end = System.nanoTime();
                    return (end - start) / 1_000_000.0;
                } finally {
                    semaphore.release();
                }
            }));
        }

        List<Double> latencies = new ArrayList<>();
        for (Future<Double> f : futures) {
            latencies.add(f.get());
        }

        long end = System.nanoTime();
        executor.shutdown();

        Runtime runtime = Runtime.getRuntime();
        double usedMemoryMb = (runtime.totalMemory() - runtime.freeMemory()) / 1024.0 / 1024.0;

        double totalTimeS = (end - begin) / 1_000_000_000.0;
        double qps = totalTasks / totalTimeS;
        double avg = latencies.stream().mapToDouble(Double::doubleValue).average().orElse(0.0);
        double p95 = percentile(latencies, 95);
        double p99 = percentile(latencies, 99);

        Result result = new Result();
        result.mode = mode;
        result.totalTasks = totalTasks;
        result.concurrency = concurrency;
        result.ioMs = ioMs;
        result.totalTimeS = totalTimeS;
        result.qps = qps;
        result.avgLatencyMs = avg;
        result.p95LatencyMs = p95;
        result.p99LatencyMs = p99;
        result.usedMemoryMb = usedMemoryMb;

        return result;
    }

    public static void main(String[] args) throws Exception {
        String mode = args.length > 0 ? args[0] : "virtual";
        int totalTasks = args.length > 1 ? Integer.parseInt(args[1]) : 10000;
        int concurrency = args.length > 2 ? Integer.parseInt(args[2]) : 1000;
        int ioMs = args.length > 3 ? Integer.parseInt(args[3]) : 50;
        int cpuRounds = args.length > 4 ? Integer.parseInt(args[4]) : 100;

        System.out.println("mode,total_tasks,concurrency,io_ms,total_time_s,qps,avg_latency_ms,p95_latency_ms,p99_latency_ms,used_memory_mb");
        System.out.println(runBench(mode, totalTasks, concurrency, ioMs, cpuRounds));
    }
}