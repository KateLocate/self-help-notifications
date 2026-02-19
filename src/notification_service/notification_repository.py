import asyncio
import time

from typing import List

from pymongo import AsyncMongoClient, ASCENDING

from constants import TIME, MESSAGE


class MongoManager:

    def __init__(self, uri: str, db_name: str):
        self.client = AsyncMongoClient(uri)
        self.db = self.client[db_name]

    async def close(self):
        await self.client.close()


class NotificationRepository:
    
    def __init__(self, mongo: MongoManager):
        self.collection = mongo.db['notifications']

    async def ensure_indexes(self):
        await self.collection.create_index(
            [(TIME, ASCENDING)]
        )


class Notification:

    def __init__(self, delta: int, message: str):
        self.due = time.time() + delta
        self.message = message

    async def wait_then_output(self):
        current_delta = self.due - time.time()
        if current_delta > 0:
            await asyncio.sleep(current_delta)


class NotificationOperations:

    def __init__(self, notification_repository):
        self.notification_repository = notification_repository

    async def create_notification(self, due_time: int, message: str) -> None:
        notification = Notification(due_time, message)
        await self.notification_repository.insert_one({TIME: notification.due, MESSAGE: notification.message})

    async def get_next_notification(self) -> Notification | None:
        if mongo_doc := await self.notification_repository.find_one({TIME: {'$gt': time.time()}}):
            notification = Notification(mongo_doc[TIME], mongo_doc[MESSAGE])
            await self.notification_repository.delete_one(mongo_doc)
            return notification

    async def get_next_notification_in_time(self) -> str | None:
        if notification := await self.get_next_notification():
            await asyncio.create_task(notification.wait_then_output())
            return notification.message

    def get_ready_notifications(self) -> List[Notification] | None:
        if mongo_docs := self.notification_repository.find({TIME: {'$gt': time.time()}}):
            notifications = []
            for mongo_doc in mongo_docs:
                notifications.append(Notification(mongo_doc[TIME], mongo_doc[MESSAGE]))
            return notifications
