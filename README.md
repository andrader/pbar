# pbar

A simple progress bar for Python, built on top of Rich.

## Features

- Simple wrapper around iterables.
- Support for nested progress bars.
- `asyncio.gather` wrapper with progress tracking.
- Transient progress bars (disappear when done).

## Quickstart

### Installation

With `uv`:
```bash
uv add git+https://github.com/andrader/pbar.git
```

With `pip`:
```bash
pip install git+https://github.com/andrader/pbar.git
```


### Usage

#### Basic Progress Bar

```python
import time
from pbar import progress_bar

# Simple range
for i in progress_bar(range(100), "Processing"):
    time.sleep(0.05)

# With a list
items = [1, 2, 3, 4, 5]
for item in progress_bar(items, "Items"):
    time.sleep(0.1)
```

#### Nested Progress Bars

pbar automatically handles multiple nested bars by adding them as tasks to the existing progress instance.

```python
import time
from pbar import progress_bar

for i in progress_bar(range(3), "Outer Loop"):
    for j in progress_bar(range(5), f"Inner Loop {i}", transient=True):
        time.sleep(0.1)
```

#### Async Gather

Use `pbar.gather` to track concurrent async tasks.

```python
import asyncio
import pbar

async def task(n):
    await asyncio.sleep(n)
    return n * 2

async def main():
    tasks = [task(1), task(2), task(0.5)]
    results = await pbar.gather(*tasks, desc="Running tasks...")
    print(results)

if __name__ == "__main__":
    asyncio.run(main())
```
