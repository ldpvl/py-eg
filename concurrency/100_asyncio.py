
import asyncio


async def parent_function():
    variable = 1

    async def inner_function(sleep_time):
        await asyncio.sleep(sleep_time)
        print(variable)

    await inner_function(2)


# asyncio.run(parent_function())

def blah(msg=''):
    print(msg)


blah(msg=f'adsfasd'
         f'asdfasdf')