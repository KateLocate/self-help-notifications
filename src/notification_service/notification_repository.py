import asyncio
import time

from bisect import insort_left, bisect_right
from operator import attrgetter

from pymongo import MongoClient


class MongoNotifications:
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        mongo_client = MongoClient('mongodb://localhost:27017/')
        mongo_db = mongo_client['notification_app_db']
        collection = mongo_db['notifications']
        init_record = collection.insert_one({'test_record': 'hello world!'})


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
        return self.ordered_notifications[:ready_idx + 1]
