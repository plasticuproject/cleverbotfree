'''
Example of a simple CLI script that creates a persistent
chat session untill closed.
'''

import asyncio
import cleverbotfree


def main():
    """Example code using cleverbotfree sync api."""
    with cleverbotfree.sync_playwright() as p_w:
        c_b = cleverbotfree.Cleverbot(p_w)
        while True:
            user_input = input("User: ")
            if user_input == 'quit':
                break
            c_b.send_input(user_input)
            bot = c_b.get_response()
            print('Cleverbot: ', bot)
        c_b.browser.close()


async def async_main():
    """Example code using cleverbotfree async api."""
    async with cleverbotfree.async_playwright() as p_w:
        c_b = await cleverbotfree.CleverbotAsync(p_w)
        while True:
            user_input = input("User: ")
            if user_input == 'quit':
                break
            await c_b.send_input(user_input)
            bot = await c_b.get_response()
            print('Cleverbot:', bot)
        await c_b.browser.close()

if __name__ == '__main__':
    main()
    # asyncio.run(async_main())
