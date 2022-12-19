[![build](https://github.com/plasticuproject/cleverbotfree/actions/workflows/tests.yml/badge.svg)](https://github.com/plasticuproject/cleverbotfree/actions/workflows/tests.yml)
[![Python 3.8](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html)
[![PyPI version](https://badge.fury.io/py/cleverbotfree.svg)](https://badge.fury.io/py/cleverbotfree)
[![Downloads](https://pepy.tech/badge/cleverbotfree)](https://pepy.tech/project/cleverbotfree)
[![CodeQL](https://github.com/plasticuproject/cleverbotfree/actions/workflows/codeql.yml/badge.svg)](https://github.com/plasticuproject/cleverbotfree/actions/workflows/codeql.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=plasticuproject_cleverbotfree&metric=alert_status)](https://sonarcloud.io/dashboard?id=plasticuproject_cleverbotfree)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=plasticuproject_cleverbotfree&metric=security_rating)](https://sonarcloud.io/dashboard?id=plasticuproject_cleverbotfree)
# cleverbotfree
Cleverbot.com used to have a free API for their chatbot application. They have <br />
removed their free API in place of a tiered subscription API service. <br />
cleverbotfree is a free alternative to that API that uses a headless Firefox <br />
browser to communicate with their chatbot application. You can use this module <br />
to create applications/bots that send and receive messages to the Cleverbot <br />
chatbot application. <br />


## Installation
### Requirments
- node >= 14.16.1
- Python >= 3.8.0
- python3-pip >= 21.1.1
 
Once requirments are met, you can install this library through pip. <br />
```
pip install cleverbotfree
```

### Drivers
This library uses the Playwright library to interface the Cleverbot website <br />
with a headless Firefox browser. <br />
To download the Playwright Firefox browser binary simply run this command after <br />
installing cleverbotfree: <br />
```
playwright install firefox
```

## Usage
<b>Examples</b>

Example of a simple CLI script that creates a persistent chat session until closed. <br />
```python
import asyncio
import cleverbotfree

def chat():
    """Example code using cleverbotfree sync api."""
    with cleverbotfree.sync_playwright() as p_w:
        c_b = cleverbotfree.Cleverbot(p_w)
        while True:
            user_input = input("User: ")
            if user_input == 'quit':
                break
            bot = c_b.single_exchange(user_input)
            print('Cleverbot:', bot)
        c_b.close()

chat()


async def async_chat():
    """Example code using cleverbotfree async api."""
    async with cleverbotfree.async_playwright() as p_w:
        c_b = await cleverbotfree.CleverbotAsync(p_w)
        while True:
            user_input = input("User: ")
            if user_input == 'quit':
                break
            bot = await c_b.single_exchange(user_input)
            print('Cleverbot:', bot)
        await c_b.close()

asyncio.run(async_chat())
```

Example of a simple CLI script using the class decorator. <br />
```python
import asyncio
from cleverbotfree import CleverbotAsync
from cleverbotfree import Cleverbot

@Cleverbot.connect
def chat(bot, user_prompt, bot_prompt):
    """Example code using cleverbotfree sync api with decorator."""
    while True:
        user_input = input(user_prompt)
        if user_input == "quit":
            break
        reply = bot.single_exchange(user_input)
        print(bot_prompt, reply)
    bot.close()

chat("User: ", "Cleverbot:")


@CleverbotAsync.connect
async def async_chat(bot, user_prompt, bot_prompt):
    """Example code using cleverbotfree async api with decorator."""
    while True:
        user_input = input(user_prompt)
        if user_input == "quit":
            break
        reply = await bot.single_exchange(user_input)
        print(bot_prompt, reply)
    await bot.close()

asyncio.run(async_chat("User: ", "Cleverbot:"))
```
