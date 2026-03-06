import os

from dotenv import load_dotenv

from notification_service.repository import NotificationOperations, MongoManager, NotificationRepository


load_dotenv()

class Container:

    def __init__(self, mongo_uri: str, db_name: str):
        self.mongo = MongoManager(mongo_uri, db_name)
        self.notification_repo = NotificationRepository(self.mongo)
        self.notification_ops = NotificationOperations(self.notification_repo.collection)


container = Container(
    mongo_uri='mongodb://{}:{}@{}:{}'.format(os.getenv('MONGO_ROOT_USERNAME'), os.getenv('MONGO_ROOT_PASSWORD'), os.getenv('MONGO_HOST'), os.getenv('MONGO_PORT')),
    db_name=str(os.getenv('MONGO_DB_NAME'))
)
