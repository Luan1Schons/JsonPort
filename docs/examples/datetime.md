# DateTime

JsonPort provides seamless handling of Python datetime objects with automatic ISO format conversion and timezone support.

## Basic DateTime Usage

### Simple DateTime

```python
from dataclasses import dataclass
from datetime import datetime
from jsonport import dump, load

@dataclass
class Event:
    name: str
    start_time: datetime
    end_time: datetime

# Create event
event = Event(
    name="Team Meeting",
    start_time=datetime(2025, 1, 14, 10, 30, 0),
    end_time=datetime(2025, 1, 14, 11, 30, 0)
)

# Serialize
data = dump(event)
print(data)
# Output:
# {
#   "name": "Team Meeting",
#   "start_time": "2025-01-14T10:30:00",
#   "end_time": "2025-01-14T11:30:00"
# }

# Deserialize
restored_event = load(data, Event)
print(restored_event.start_time)  # 2025-01-14 10:30:00
print(restored_event.end_time)  # 2025-01-14 11:30:00
```

### Date Objects

```python
from dataclasses import dataclass
from datetime import date
from jsonport import dump, load

@dataclass
class User:
    name: str
    birth_date: date
    registration_date: date

# Create user
user = User(
    name="John Doe",
    birth_date=date(1990, 5, 15),
    registration_date=date(2024, 1, 1)
)

# Serialize
data = dump(user)
print(data)
# Output:
# {
#   "name": "John Doe",
#   "birth_date": "1990-05-15",
#   "registration_date": "2024-01-01"
# }

# Deserialize
restored_user = load(data, User)
print(restored_user.birth_date)  # 1990-05-15
print(restored_user.registration_date)  # 2024-01-01
```

### Time Objects

```python
from dataclasses import dataclass
from datetime import time
from jsonport import dump, load

@dataclass
class Schedule:
    name: str
    start_time: time
    end_time: time

# Create schedule
schedule = Schedule(
    name="Work Hours",
    start_time=time(9, 0, 0),
    end_time=time(17, 30, 0)
)

# Serialize
data = dump(schedule)
print(data)
# Output:
# {
#   "name": "Work Hours",
#   "start_time": "09:00:00",
#   "end_time": "17:30:00"
# }

# Deserialize
restored_schedule = load(data, Schedule)
print(restored_schedule.start_time)  # 09:00:00
print(restored_schedule.end_time)  # 17:30:00
```

## Timezone-Aware DateTime

### With Timezone Information

```python
from dataclasses import dataclass
from datetime import datetime
import pytz
from jsonport import dump, load

@dataclass
class Meeting:
    title: str
    scheduled_time: datetime
    timezone: str

# Create timezone-aware datetime
utc_tz = pytz.UTC
ny_tz = pytz.timezone('America/New_York')

meeting = Meeting(
    title="Global Team Sync",
    scheduled_time=datetime(2025, 1, 14, 15, 0, 0, tzinfo=utc_tz),
    timezone="UTC"
)

# Serialize
data = dump(meeting)
print(data)
# Output:
# {
#   "title": "Global Team Sync",
#   "scheduled_time": "2025-01-14T15:00:00+00:00",
#   "timezone": "UTC"
# }

# Deserialize
restored_meeting = load(data, Meeting)
print(restored_meeting.scheduled_time)  # 2025-01-14 15:00:00+00:00
print(restored_meeting.scheduled_time.tzinfo)  # UTC
```

### Converting Between Timezones

```python
from dataclasses import dataclass
from datetime import datetime
import pytz
from jsonport import dump, load

@dataclass
class Appointment:
    description: str
    local_time: datetime
    utc_time: datetime

# Create appointment in local timezone
local_tz = pytz.timezone('America/New_York')
utc_tz = pytz.UTC

local_time = local_tz.localize(datetime(2025, 1, 14, 10, 0, 0))
utc_time = local_time.astimezone(utc_tz)

appointment = Appointment(
    description="Doctor Visit",
    local_time=local_time,
    utc_time=utc_time
)

# Serialize
data = dump(appointment)
print(data)
# Output:
# {
#   "description": "Doctor Visit",
#   "local_time": "2025-01-14T10:00:00-05:00",
#   "utc_time": "2025-01-14T15:00:00+00:00"
# }

# Deserialize
restored_appointment = load(data, Appointment)
print(restored_appointment.local_time)  # 2025-01-14 10:00:00-05:00
print(restored_appointment.utc_time)  # 2025-01-14 15:00:00+00:00
```

## Complex DateTime Structures

### Nested DateTime Objects

```python
from dataclasses import dataclass
from datetime import datetime, date
from typing import List, Optional

@dataclass
class LogEntry:
    message: str
    timestamp: datetime
    level: str

@dataclass
class SystemLog:
    system_name: str
    start_date: date
    entries: List[LogEntry]
    last_updated: Optional[datetime] = None

# Create system log
log = SystemLog(
    system_name="Web Server",
    start_date=date(2024, 1, 1),
    entries=[
        LogEntry("Server started", datetime(2024, 1, 1, 8, 0, 0), "INFO"),
        LogEntry("Database connected", datetime(2024, 1, 1, 8, 1, 0), "INFO"),
        LogEntry("Error in request", datetime(2024, 1, 1, 8, 5, 0), "ERROR")
    ],
    last_updated=datetime(2024, 1, 1, 8, 5, 0)
)

# Serialize
data = dump(log)
print(data)
# Output:
# {
#   "system_name": "Web Server",
#   "start_date": "2024-01-01",
#   "entries": [
#     {
#       "message": "Server started",
#       "timestamp": "2024-01-01T08:00:00",
#       "level": "INFO"
#     },
#     {
#       "message": "Database connected",
#       "timestamp": "2024-01-01T08:01:00",
#       "level": "INFO"
#     },
#     {
#       "message": "Error in request",
#       "timestamp": "2024-01-01T08:05:00",
#       "level": "ERROR"
#     }
#   ],
#   "last_updated": "2024-01-01T08:05:00"
# }

# Deserialize
restored_log = load(data, SystemLog)
print(len(restored_log.entries))  # 3
print(restored_log.entries[0].timestamp)  # 2024-01-01 08:00:00
```

### DateTime in Collections

```python
from dataclasses import dataclass
from datetime import datetime, date
from typing import Dict, List, Set

@dataclass
class TimeSeries:
    name: str
    dates: List[date]
    timestamps: List[datetime]
    date_counts: Dict[date, int]
    unique_times: Set[datetime]

# Create time series data
time_series = TimeSeries(
    name="Temperature Data",
    dates=[date(2024, 1, 1), date(2024, 1, 2), date(2024, 1, 3)],
    timestamps=[
        datetime(2024, 1, 1, 12, 0, 0),
        datetime(2024, 1, 1, 18, 0, 0),
        datetime(2024, 1, 2, 12, 0, 0)
    ],
    date_counts={
        date(2024, 1, 1): 2,
        date(2024, 1, 2): 1,
        date(2024, 1, 3): 0
    },
    unique_times={
        datetime(2024, 1, 1, 12, 0, 0),
        datetime(2024, 1, 1, 18, 0, 0),
        datetime(2024, 1, 2, 12, 0, 0)
    }
)

# Serialize
data = dump(time_series)
print(data)
# Output:
# {
#   "name": "Temperature Data",
#   "dates": ["2024-01-01", "2024-01-02", "2024-01-03"],
#   "timestamps": [
#     "2024-01-01T12:00:00",
#     "2024-01-01T18:00:00",
#     "2024-01-02T12:00:00"
#   ],
#   "date_counts": {
#     "2024-01-01": 2,
#     "2024-01-02": 1,
#     "2024-01-03": 0
#   },
#   "unique_times": [
#     "2024-01-01T12:00:00",
#     "2024-01-01T18:00:00",
#     "2024-01-02T12:00:00"
#   ]
# }

# Deserialize
restored_series = load(data, TimeSeries)
print(len(restored_series.dates))  # 3
print(restored_series.date_counts[date(2024, 1, 1)])  # 2
```

## DateTime Operations

### Date Arithmetic

```python
from dataclasses import dataclass
from datetime import datetime, timedelta
from jsonport import dump, load

@dataclass
class Task:
    name: str
    created_at: datetime
    due_date: datetime
    completed_at: datetime = None

# Create task
task = Task(
    name="Complete project",
    created_at=datetime.now(),
    due_date=datetime.now() + timedelta(days=7)
)

# Serialize
data = dump(task)
print(data)
# Output:
# {
#   "name": "Complete project",
#   "created_at": "2025-01-14T10:30:00",
#   "due_date": "2025-01-21T10:30:00",
#   "completed_at": null
# }

# Deserialize and perform operations
restored_task = load(data, Task)

# Calculate time remaining
if restored_task.completed_at is None:
    time_remaining = restored_task.due_date - datetime.now()
    print(f"Time remaining: {time_remaining.days} days")

# Mark as completed
restored_task.completed_at = datetime.now()

# Re-serialize
updated_data = dump(restored_task)
```

### Date Comparison

```python
from dataclasses import dataclass
from datetime import datetime, date
from jsonport import dump, load

@dataclass
class Event:
    name: str
    start_date: date
    end_date: date
    created_at: datetime

# Create event
event = Event(
    name="Conference",
    start_date=date(2025, 3, 15),
    end_date=date(2025, 3, 17),
    created_at=datetime.now()
)

# Serialize
data = dump(event)

# Deserialize and compare dates
restored_event = load(data, Event)

today = date.today()
if restored_event.start_date > today:
    print(f"Event '{restored_event.name}' is in the future")
elif restored_event.end_date < today:
    print(f"Event '{restored_event.name}' has ended")
else:
    print(f"Event '{restored_event.name}' is ongoing")

# Check if event is within a week
week_from_now = today + timedelta(days=7)
if restored_event.start_date <= week_from_now:
    print(f"Event '{restored_event.name}' is within a week")
```

## DateTime Formatting

### Custom Formatting

```python
from dataclasses import dataclass
from datetime import datetime
from jsonport import dump, load

@dataclass
class FormattedEvent:
    name: str
    timestamp: datetime
    
    def get_formatted_time(self):
        return self.timestamp.strftime("%B %d, %Y at %I:%M %p")
    
    def get_iso_format(self):
        return self.timestamp.isoformat()

# Create event
event = FormattedEvent(
    name="Team Meeting",
    timestamp=datetime(2025, 1, 14, 14, 30, 0)
)

# Serialize
data = dump(event)

# Deserialize and format
restored_event = load(data, FormattedEvent)
print(restored_event.get_formatted_time())  # "January 14, 2025 at 02:30 PM"
print(restored_event.get_iso_format())  # "2025-01-14T14:30:00"
```

### Timezone Conversion

```python
from dataclasses import dataclass
from datetime import datetime
import pytz
from jsonport import dump, load

@dataclass
class GlobalEvent:
    name: str
    utc_time: datetime
    
    def get_local_time(self, timezone_name):
        local_tz = pytz.timezone(timezone_name)
        return self.utc_time.astimezone(local_tz)
    
    def get_all_times(self):
        timezones = ['UTC', 'America/New_York', 'Europe/London', 'Asia/Tokyo']
        return {tz: self.get_local_time(tz) for tz in timezones}

# Create global event
event = GlobalEvent(
    name="Product Launch",
    utc_time=datetime(2025, 1, 14, 15, 0, 0, tzinfo=pytz.UTC)
)

# Serialize
data = dump(event)

# Deserialize and get times in different timezones
restored_event = load(data, GlobalEvent)
all_times = restored_event.get_all_times()

for tz, time in all_times.items():
    print(f"{tz}: {time.strftime('%Y-%m-%d %H:%M:%S %Z')}")
```

## Error Handling with DateTime

### Invalid Date Formats

```python
from dataclasses import dataclass
from datetime import datetime
from jsonport import load, DeserializationError

@dataclass
class Event:
    name: str
    date: datetime

# This will raise DeserializationError
try:
    event = load({"name": "Meeting", "date": "invalid-date"}, Event)
except DeserializationError as e:
    print(f"Error: {e}")
    # Output: Error: Cannot deserialize 'invalid-date' to datetime
```

### Handling Missing Timezone Information

```python
from dataclasses import dataclass
from datetime import datetime
import pytz
from jsonport import dump, load

@dataclass
class TimezoneEvent:
    name: str
    local_time: datetime
    timezone: str
    
    def get_utc_time(self):
        if self.local_time.tzinfo is None:
            # Assume local timezone if not specified
            local_tz = pytz.timezone(self.timezone)
            return local_tz.localize(self.local_time).astimezone(pytz.UTC)
        return self.local_time.astimezone(pytz.UTC)

# Create event with naive datetime
event = TimezoneEvent(
    name="Local Meeting",
    local_time=datetime(2025, 1, 14, 10, 0, 0),  # No timezone info
    timezone="America/New_York"
)

# Serialize
data = dump(event)

# Deserialize and handle timezone
restored_event = load(data, TimezoneEvent)
utc_time = restored_event.get_utc_time()
print(f"UTC time: {utc_time}")
```

## Performance Considerations

### Large DateTime Collections

```python
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List
import time

@dataclass
class TimeSeriesData:
    timestamps: List[datetime]
    values: List[float]

# Create large time series
base_time = datetime(2024, 1, 1)
timestamps = [base_time + timedelta(hours=i) for i in range(10000)]
values = [i * 0.1 for i in range(10000)]

time_series = TimeSeriesData(timestamps, values)

# Measure serialization performance
start_time = time.time()
data = dump(time_series)
serialization_time = time.time() - start_time

# Measure deserialization performance
start_time = time.time()
restored_series = load(data, TimeSeriesData)
deserialization_time = time.time() - start_time

print(f"Serialization time: {serialization_time:.3f}s")
print(f"Deserialization time: {deserialization_time:.3f}s")
print(f"Data points: {len(restored_series.timestamps)}")
```

### Memory Usage with DateTime

```python
import sys
from dataclasses import dataclass
from datetime import datetime
from typing import List

@dataclass
class DateTimeTest:
    timestamps: List[datetime]

# Test memory usage
original_data = DateTimeTest([datetime.now() for _ in range(1000)])
print(f"Original size: {sys.getsizeof(original_data)} bytes")

serialized = dump(original_data)
print(f"Serialized size: {sys.getsizeof(serialized)} bytes")

restored = load(serialized, DateTimeTest)
print(f"Restored size: {sys.getsizeof(restored)} bytes")
```

This comprehensive guide demonstrates how to effectively work with datetime objects in JsonPort, including timezone handling, complex structures, operations, and performance considerations. 