import asyncio

from fastapi import APIRouter, WebSocket, HTTPException
from notification_service.container import container


router = APIRouter(
    prefix='/notifications',
    tags=['notifications'],
    responses={404: {'description': 'Not found'}},
)


@router.get('/received_notifications')
async def get_received_notifications():
    notifications = await container.notification_ops.get_ready_notifications()
    return {'notifications': notifications}


@router.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await container.notification_ops.get_next_notification_in_time()
        if data:
            await websocket.send_text(f'Notification text: {data}')
        else:
            await asyncio.sleep(1)


@router.post('/notification')
async def add_notification(body: dict):
    # e.g. {"message": "hi", "timedelta": 5}
    notification_text = body.get('message')
    notification_timedelta = body.get('timedelta')
    if not notification_text or not notification_timedelta:
        raise HTTPException(status_code=400, detail='Both "message" and "timedelta" fields are required')

    await container.notification_ops.create_notification(due_time=notification_timedelta, message=notification_text)
    return {'message': 'Item added successfully', 'item': notification_text}
