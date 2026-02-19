import asyncio

from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, HTTPException

from constants import MESSAGE
from notification_repository import NotificationOperations, MongoManager, NotificationRepository


class Container:

    def __init__(self, mongo_uri: str, db_name: str):
        self.mongo = MongoManager(mongo_uri, db_name)
        self.notification_repo = NotificationRepository(self.mongo)


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
notification_ops = NotificationOperations(container.notification_repo.collection)


@app.get('/received_notifications')
def get_received_notifications():
    notifications = notification_ops.get_ready_notifications()
    return {'notifications': notifications}

@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await notification_ops.get_next_notification_in_time()
        if data:
            await websocket.send_text(f'Notification text: {data}')
        else:
            await asyncio.sleep(1)


@app.post('/notification')
async def add_notification(body: dict):
    # e.g. {"message": "hi", "timedelta": 5}
    notification_text = body.get(MESSAGE)
    notification_timedelta = body.get('timedelta')
    if not notification_text or not notification_timedelta:
        raise HTTPException(status_code=400, detail='Both "text" and "timedelta" fields are required')

    await notification_ops.create_notification(due_time=notification_timedelta, message=notification_text)
    return {MESSAGE: 'Item added successfully', 'item': notification_text}
