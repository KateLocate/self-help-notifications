import asyncio
import sys

from notification_crud_operations import NotificationManager


class NotificationAsyncIO:
    def __init__(self):
        self.notification_manager = NotificationManager()

    @staticmethod
    async def async_input(string: str) -> str:
        await asyncio.to_thread(sys.stdout.write, f'{string} ')
        return (await asyncio.to_thread(sys.stdin.readline)).rstrip('\n')

    async def wait_for_input(self):
        message = await self.async_input("Enter your message:")
        timedelta = int(await self.async_input("Enter time in seconds:"))

        self.notification_manager.create_notification(timedelta, message)

    async def notify(self):
        notification = self.notification_manager.get_next_notification()
        if notification:
            await notification.wait_for_due()
            print(notification.message)


async def main():
    notification_io = NotificationAsyncIO()
    try:
        while True:
            # I suppose that one of the problems is hidden here:
            # loop should not enter context manager each iteration,
            # that's my best guess for why timer is blocking everything.
            async with asyncio.TaskGroup() as tg:
                tg.create_task(notification_io.notify())
                tg.create_task(notification_io.wait_for_input())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    asyncio.run(main())
