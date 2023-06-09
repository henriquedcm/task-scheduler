# Task Scheduler

Simple task scheduler running in a daemon process.

## Running

Run the package as a module:

```bash
python3 -m scheduler
```

## Usage

```python
import time

from scheduler import Scheduler


def yell(message: str) -> None:
    message = f"{message.upper()}!!!!!"
    print(message)


scheduler = Scheduler()
scheduler.run()

scheduler.add_task(func=yell, kwargs={"message": "5 seconds later"}, delay=5)
scheduler.add_task(func=yell, args=("instant message",))

time.sleep(6)
scheduler.stop()
```
