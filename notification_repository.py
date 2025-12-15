from dataclasses import dataclass
from bisect import insort_left
from operator import attrgetter


@dataclass
class Notification:
    due: int
    message: str


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
