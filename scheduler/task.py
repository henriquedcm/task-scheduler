import datetime
from typing import Callable, Sequence, Mapping


class Task:
    def __init__(
        self,
        func: Callable,
        args: Sequence | None = None,
        kwargs: Mapping | None = None,
        delay: int = 0
    ) -> None:
        self.func = func
        self.args = args if args else ()
        self.kwargs = kwargs if kwargs else {}
        self.run_at = (
            datetime.datetime.now()
            + datetime.timedelta(seconds=delay)
        )

    def execute(self) -> None:
        self.func(*self.args, **self.kwargs)

    def should_run(self) -> bool:
        return datetime.datetime.now() >= self.run_at
