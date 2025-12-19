import time

from notification_repository import Scheduler


class NotificationManager:

    def __init__(self):
        self.scheduler = Scheduler()

    def create_notification(self, delta, message) -> None:
        due = time.time() + delta
        self.scheduler.create_notification(due, message)

    def get_next_notification(self):
        return self.scheduler.get_next_notification()
