'''
Example of a simple CLI script that creates a single use,
one message chat session.
'''

import asyncio
import cleverbotfree


def main():
    """Example code using cleverbotfree sync api."""
    with cleverbotfree.sync_playwright() as p_w:
        c_b = cleverbotfree.Cleverbot(p_w)
        user_input = input("User: ")
        response = c_b.single_exchange(user_input)
        print("Cleverbot:", response)
        c_b.browser.close()


async def async_main():
    """Example code using cleverbotfree async api."""
    async with cleverbotfree.async_playwright() as p_w:
        c_b = await cleverbotfree.CleverbotAsync(p_w)
        user_input = input("User: ")
        response = await c_b.single_exchange(user_input)
        print("Cleverbot:", response)
        await c_b.browser.close()


if __name__ == '__main__':
    main()
    # asyncio.run(async_main())
