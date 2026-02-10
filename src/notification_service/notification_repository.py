import asyncio
import time

from bisect import insort_left, bisect_right
from operator import attrgetter


class Notification:

    def __init__(self, delta: int, message: str):
        self.due = time.time() + delta
        self.message = message

    async def wait_then_output(self):
        current_delta = self.due - time.time()
        if current_delta > 0:
            await asyncio.sleep(current_delta)


class Scheduler:
    def __init__(self):
        self.ordered_notifications = []

    def create_notification(self, due: int, message: str) -> None:
        notification = Notification(due, message)
        insort_left(self.ordered_notifications, notification, key=attrgetter('due'))

    def get_next_notification(self) -> Notification | None:
        try:
            return self.ordered_notifications.pop(0)
        except IndexError:
            return None

    def get_ready_notifications(self):
        ready_idx = bisect_right(self.ordered_notifications, time.time(), key=attrgetter('due'))
        return self.ordered_notifications[:ready_idx+1]
