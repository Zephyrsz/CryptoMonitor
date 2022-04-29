import asyncio
import time

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

#### in sequence
async def main1():
    print(f"started at {time.strftime('%X')}")

    await say_after(2, 'hello')
    await say_after(1, 'world')

    print(f"finished at {time.strftime('%X')}")

asyncio.run(main1())


## create task run in concurrent
async def main2():
    task1 = asyncio.create_task(
        say_after(3, 'hello'))

    task2 = asyncio.create_task(
        say_after(2, 'world'))

    print(f"started at {time.strftime('%X')}")

    # Wait until both tasks are completed (should take
    # around 2 seconds.)
    await task1
    await task2

    print(f"finished at {time.strftime('%X')}")

asyncio.run(main())