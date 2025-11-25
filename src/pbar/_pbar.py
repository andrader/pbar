from rich.progress import MofNCompleteColumn, Progress, SpinnerColumn, TimeElapsedColumn

__CURRENT_PBAR = None


def progress_bar(
    iterable, desc: str, transient: bool = False, total: int | None = None, **kwargs
):
    """
    Wraps an iterable with a Rich progress bar, using a global progress bar instance.
    If a progress bar is already active, adds a new task to it instead of creating a new one.
    """
    global __CURRENT_PBAR

    progress = __CURRENT_PBAR

    desc_col, bar_col, percent_col, timeremaining_col = Progress.get_default_columns()

    # If no global progress bar exists, create one and start it
    if progress is None:
        progress = Progress(
            desc_col,
            SpinnerColumn(),
            MofNCompleteColumn(),
            bar_col,
            percent_col,
            TimeElapsedColumn(),
            timeremaining_col,
            transient=transient,
            **kwargs,
        )
        __CURRENT_PBAR = progress
        progress.start()

    # Add a new task for this iterable
    total = total or (len(iterable) if hasattr(iterable, "__len__") else None)
    task_id = progress.add_task(desc, total=total)

    def generator():
        global __CURRENT_PBAR

        try:
            for item in iterable:
                yield item
                progress.update(task_id, advance=1)
        finally:
            with progress._lock:
                task = progress._tasks[task_id]
            progress.update(
                task_id,
                total=task.completed,
                visible=not transient,
            )
            if transient:
                progress.remove_task(task_id)

            # If all tasks are finished, stop and reset the global progress bar
            if progress.finished:
                progress.stop()
                __CURRENT_PBAR = None

    return generator()
