import asyncio

from notification_crud_operations import NotificationManager

from fastapi import FastAPI, HTTPException


class NotificationAsyncIO:
    def __init__(self):
        self.notification_manager = NotificationManager()

    async def wait_for_input(self):
        user_input = await asyncio.to_thread(input, "Enter your message:")

        if not user_input.strip():
            return

        timedelta = int(await asyncio.to_thread(input, "Enter time in seconds:"))

        self.notification_manager.create_notification(timedelta, user_input)

        await self.get_next_notification_in_time()

    async def get_next_notification_in_time(self) -> str:
        if notification := self.notification_manager.get_next_notification():
            await asyncio.create_task(notification.wait_then_output())
            return notification.message


app = FastAPI()
notificationsIO = NotificationAsyncIO()


@app.get("/received_notifications")
def get_received_notifications():
    notifications = notificationsIO.notification_manager.get_ready_notifications()
    return {"notifications": notifications}


@app.post("/notification")
def add_notification(body: dict):
    # {"text": "hi", "timedelta": 5}
    notification_text = body.get("text")
    notification_timedelta = body.get("timedelta")
    if not notification_text or not notification_timedelta:
        raise HTTPException(status_code=400, detail="'text' and 'timedelta' fields both are required")

    notificationsIO.notification_manager.create_notification(delta=notification_timedelta, message=notification_text)
    return {"message": "Item added successfully", "item": notification_text}
