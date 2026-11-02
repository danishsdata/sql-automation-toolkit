"""Top slow queries from pg_stat_statements, printed as a plain table.

Password comes from the PGPASSWORD environment variable, never from
the command line.
"""

import argparse
import os

import psycopg2

QUERY = """
SELECT query, calls, total_exec_time, mean_exec_time, rows
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT %s
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", required=True)
    parser.add_argument("--dbname", required=True)
    parser.add_argument("--user", required=True)
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()

    conn = psycopg2.connect(
        host=args.host,
        dbname=args.dbname,
        user=args.user,
        password=os.environ.get("PGPASSWORD"),
    )
    cur = conn.cursor()
    cur.execute(QUERY, (args.limit,))
    print(f"{'calls':>8} {'total_ms':>12} {'mean_ms':>10}  query")
    for query, calls, total, mean, rows in cur.fetchall():
        print(f"{calls:>8} {total:>12.1f} {mean:>10.1f}  {query[:120]}")
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
