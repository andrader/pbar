import asyncio
from typing import Any, Awaitable, List

from rich.progress import Progress


async def gather(
    *awaitables: Awaitable[Any],
    return_exceptions: bool = False,
    desc: str = "Processing...",
    **progress_kwargs: Any,
) -> List[Any]:
    """
    Wrapper around asyncio.gather that displays a progress bar.

    Args:
        *awaitables: Coroutines or awaitables to execute concurrently
        return_exceptions: If True, exceptions are returned as results instead of raising
        desc: Description text for the progress bar
        **progress_kwargs: Additional keyword arguments for Progress

    Returns:
        List of results from the awaitables
    """
    if not awaitables:
        return []

    with Progress(**progress_kwargs) as progress:
        task_id = progress.add_task(desc, total=len(awaitables))

        # Track completed tasks
        completed_count = 0
        results = [None] * len(awaitables)

        async def track_completion(index: int, awaitable: Awaitable[Any]) -> Any:
            nonlocal completed_count
            try:
                result = await awaitable
                results[index] = result
                completed_count += 1
                progress.update(task_id, completed=completed_count)
                return result
            except Exception as e:
                completed_count += 1
                progress.update(task_id, completed=completed_count)
                if return_exceptions:
                    results[index] = e  # type: ignore
                    return e
                else:
                    raise e

        # Create tracking tasks
        tracking_tasks = [
            track_completion(i, awaitable) for i, awaitable in enumerate(awaitables)
        ]

        # Wait for all tasks to complete
        await asyncio.gather(*tracking_tasks, return_exceptions=return_exceptions)

        return results


if __name__ == "__main__":

    async def example_task(duration: float, name: str) -> str:
        """Example async task for demonstration."""

        await asyncio.sleep(duration)
        if "2" in name:
            raise ValueError("ERRPRRR")
        return f"Completed {name}"

    async def main():
        """Example usage of gather_with_progress."""
        tasks = [
            example_task(1.0, "Task 1"),
            example_task(1.5, "Task 2"),
            example_task(0.8, "Task 3"),
            example_task(2.0, "Task 4"),
            example_task(1.2, "Task 5"),
        ]

        results = await gather(
            *tasks, desc="[cyan]Running example tasks...", return_exceptions=True
        )

        for res in results:
            if isinstance(res, Exception):
                print("error", str(res))
            else:
                print(res)

    asyncio.run(main())
