from datetime import datetime as dt

updated = dt (2023, 11, 21, 23, 28, 48, 54514)
created = dt(2023, 11, 21, 23, 28, 33, 386987)
published = dt(2023, 11, 21, 23, 28, 36, 786985)

updated_to_minutes = updated.replace(second=0,microsecond=0)
created_to_minutes = created.replace(second=0,microsecond=0)
published_to_minutes = published.replace(second=0,microsecond=0)
