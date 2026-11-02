"""Indexes with few or no scans, per database.

Low scans alone is not a drop list. Check for monthly or quarterly jobs
first; an index that only matters once a quarter still matters.
"""

import argparse
import os

import psycopg2

QUERY = """
SELECT schemaname, relname, indexrelname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan < %s
ORDER BY idx_scan ASC
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", required=True)
    parser.add_argument("--dbname", required=True)
    parser.add_argument("--user", required=True)
    parser.add_argument("--max-scans", type=int, default=10)
    args = parser.parse_args()

    conn = psycopg2.connect(
        host=args.host,
        dbname=args.dbname,
        user=args.user,
        password=os.environ.get("PGPASSWORD"),
    )
    cur = conn.cursor()
    cur.execute(QUERY, (args.max_scans,))
    for schema, table, index, scans in cur.fetchall():
        print(f"{schema}.{table}  {index}  scans={scans}")
    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
