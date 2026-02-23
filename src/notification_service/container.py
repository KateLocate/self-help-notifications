from notification_service.repository import NotificationOperations, MongoManager, NotificationRepository


class Container:

    def __init__(self, mongo_uri: str, db_name: str):
        self.mongo = MongoManager(mongo_uri, db_name)
        self.notification_repo = NotificationRepository(self.mongo)
        self.notification_ops = NotificationOperations(self.notification_repo.collection)


container = Container(
    mongo_uri='mongodb://localhost:27017',
    db_name='notifications_db'
)
