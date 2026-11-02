# sql-automation-toolkit

Three scripts for routine DBA checks, plus the SQL I run by hand when
a database feels slow.

Portfolio implementation of patterns I use as an AWS DBA / data engineer.

## The scripts

- slow_query_report.py: top slow queries from pg_stat_statements.
- index_usage.py: indexes with few or no scans.
- backup_check.py: newest manual RDS snapshot age, exits 1 when too old.

## Run

```
export PGPASSWORD=<PASSWORD>
python slow_query_report.py --host <HOST> --dbname <DB> --user <USER>
python index_usage.py --host <HOST> --dbname <DB> --user <USER>
python backup_check.py --instance <DB_INSTANCE_ID> --max-age-hours 26
```
