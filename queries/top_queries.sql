-- Queries to run against pg_stat_statements when a database feels slow.

-- Top 20 by total time:
SELECT query, calls, total_exec_time, mean_exec_time
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 20;

-- Slowest on average, with at least 100 calls so one-offs don't dominate:
SELECT query, calls, mean_exec_time
FROM pg_stat_statements
WHERE calls >= 100
ORDER BY mean_exec_time DESC
LIMIT 20;
