"""Check the newest manual RDS snapshot for an instance.

Exits 0 when a snapshot exists and is younger than --max-age-hours,
1 otherwise, so a scheduler can alert on the exit code.
"""

import argparse
import sys
from datetime import datetime, timezone

import boto3


def newest_snapshot(client, instance_id):
    resp = client.describe_db_snapshots(
        DBInstanceIdentifier=instance_id,
        SnapshotType="manual",
    )
    snaps = sorted(
        resp.get("DBSnapshots", []),
        key=lambda s: s["SnapshotCreateTime"],
    )
    return snaps[-1] if snaps else None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--instance", required=True)
    parser.add_argument("--max-age-hours", type=int, default=26)
    args = parser.parse_args()

    client = boto3.client("rds")
    snap = newest_snapshot(client, args.instance)
    if snap is None:
        print(f"{args.instance}: no manual snapshots found")
        return 1
    age = (
        datetime.now(timezone.utc) - snap["SnapshotCreateTime"]
    ).total_seconds() / 3600
    print(
        f"{args.instance}: {snap['DBSnapshotIdentifier']} "
        f"created {snap['SnapshotCreateTime']} ({age:.1f}h ago)"
    )
    if age > args.max_age_hours:
        print(f"WARNING: newest snapshot is older than {args.max_age_hours}h")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
