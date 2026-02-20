import asyncio

from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, HTTPException

from notification_service.notification_repository import NotificationOperations, MongoManager, NotificationRepository


class Container:

    def __init__(self, mongo_uri: str, db_name: str):
        self.mongo = MongoManager(mongo_uri, db_name)
        self.notification_repo = NotificationRepository(self.mongo)
        self.notification_ops = NotificationOperations(self.notification_repo.collection)

container = Container(
    mongo_uri='mongodb://localhost:27017',
    db_name='notifications_db'
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    mongo = container.mongo
    
    await container.notification_repo.ensure_indexes()

    app.state.mongo = mongo
    app.state.notification_repo = container.notification_repo

    yield

    await mongo.close()


app = FastAPI(lifespan=lifespan)


@app.get('/received_notifications')
async def get_received_notifications():
    notifications = await container.notification_ops.get_ready_notifications()
    return {'notifications': notifications}

@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await container.notification_ops.get_next_notification_in_time()
        if data:
            await websocket.send_text(f'Notification text: {data}')
        else:
            await asyncio.sleep(1)


@app.post('/notification')
async def add_notification(body: dict):
    # e.g. {"message": "hi", "timedelta": 5}
    notification_text = body.get('message')
    notification_timedelta = body.get('timedelta')
    if not notification_text or not notification_timedelta:
        raise HTTPException(status_code=400, detail='Both "text" and "timedelta" fields are required')

    await container.notification_ops.create_notification(due_time=notification_timedelta, message=notification_text)
    return {'message': 'Item added successfully', 'item': notification_text}
