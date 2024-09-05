import asyncio
import importlib.metadata


async def main():
    print_i()


async def print_i():
    for i in range(10):
        print(i)
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
