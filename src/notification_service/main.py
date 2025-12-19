import asyncio
import sys

from notification_crud_operations import NotificationManager


class NotificationAsyncIO:
    def __init__(self):
        self.notification_manager = NotificationManager()

    async def wait_for_input(self):
        user_input = await asyncio.to_thread(input, "Enter your message:")

        if not user_input.strip():
            return

        timedelta = int(await asyncio.to_thread(input,"Enter time in seconds:"))

        self.notification_manager.create_notification(timedelta, user_input)

        await self.notify()

    async def notify(self):
        notification = self.notification_manager.get_next_notification()
        if notification:
            asyncio.create_task(notification.wait_then_output())


async def main():
    notification_io = NotificationAsyncIO()
    try:
        while True:
            await notification_io.wait_for_input()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    asyncio.run(main())
