import time

from notification_repository import Scheduler


class NotificationManager:

    def __init__(self):
        self.scheduler = Scheduler()

    def create_notification(self, delta, message) -> None:
        self.scheduler.create_notification(delta, message)

    def get_next_notification(self):
        return self.scheduler.get_next_notification()

    def get_ready_notifications(self):
        return self.scheduler.get_ready_notifications()