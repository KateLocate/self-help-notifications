import asyncio
import time

from notification_repository import Scheduler


scheduler = Scheduler()


def create_notification(delta, message) -> None:
    due = time.time() + delta
    scheduler.create_notification(due, message)


async def wait_for_notification():
    notification = scheduler.get_next_notification()

    if notification:
        current_delta = notification.due - time.time()
        await asyncio.sleep(current_delta)

        print('\n' + notification.message)
    else:
        await asyncio.sleep(1)
        print('\n' + "nah")