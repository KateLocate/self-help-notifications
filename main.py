import asyncio
import sys

from notification_manager import create_notification, wait_for_notification

async def async_input(string: str) -> str:
    await asyncio.to_thread(sys.stdout.write, f'{string} ')
    return (await asyncio.to_thread(sys.stdin.readline)).rstrip('\n')

async def wait_for_input():
    message = await async_input("Enter your message:")
    timedelta = int(await async_input("Enter time in seconds:"))
    create_notification(timedelta, message)

async def main():
    while True:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(wait_for_input())
            tg.create_task(wait_for_notification())


if __name__ == "__main__":
    asyncio.run(main())
