from datetime import datetime, time, timezone


utcDate = datetime.now(timezone.utc)
timestamp1 = utcDate.strftime("%Y-%m-%dT%H:%M:%SZ")
timestamp2 = utcDate.strftime("2021-11-06T19:36:00Z")
print(timestamp1, timestamp2)
