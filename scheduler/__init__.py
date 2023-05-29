import ctypes
import multiprocessing as mp
from typing import Callable, Sequence, Mapping

from scheduler.task import Task


class Scheduler:
    def __init__(self) -> None:
        self.manager = mp.Manager()
        self.tasks = self.manager.list()
        self.keep_running = self.manager.Value(ctypes.c_bool, False)
        self.process = mp.Process(
            target=self.loop_tasks,
            args=(self,),
            daemon=True
        )

    def run(self) -> None:
        self.keep_running.value = True
        self.process.start()

    def stop(self) -> None:
        self.keep_running.value = False
        self.process.join()

    def add_task(
        self,
        func: Callable,
        args: Sequence | None = None,
        kwargs: Mapping | None = None,
        delay: int = 0
    ) -> None:
        task = Task(func=func, args=args, kwargs=kwargs, delay=delay)
        self.tasks.append(task)

    @staticmethod
    def loop_tasks(scheduler: "Scheduler") -> None:
        while True:
            if not scheduler.keep_running.value:
                break

            if not scheduler.tasks:
                continue

            scheduler.execute_pending()

    def execute_pending(self) -> None:
        tasks = []

        for index, task in enumerate(self.tasks):
            if task.should_run():
                tasks.append(self.tasks.pop(index))

        for task in tasks:
            task.execute()
