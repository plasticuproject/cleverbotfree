'''
This module is a free alternative to Cleverbot.com's subscription API.
It uses a headless Firefox browser to run Cleverbot's JavaScript code
and retrieve a reply.

Copyright (C) 2021  plasticuproject@pm.me

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
'''

import re
import asyncio
from time import sleep
from functools import wraps
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
from playwright._impl._api_types import TimeoutError as PwTimeout
from fake_useragent import UserAgent


class AsyncObject():
    """Inheriting this class allows me to define an async
    __init__, So you can create an async Cleverbot object
    by doing `await CleverbotAsync(p_w)`"""

    # pylint: disable=too-few-public-methods
    # pylint: disable=invalid-overridden-method
    # Because we've created an async init hack
    async def __new__(cls, *a, **kw):
        instance = super().__new__(cls)
        await instance.__init__(*a, **kw)
        return instance

    async def __init__(self):
        """Async init."""


class Cleverbot():
    """ Constructs a Cleverbot chat session. Initializes the options
    to connect to Cleverbot.com via a headless Firefox browser using
    playwright, and contains the functions to connect and create chat
    sessions. Every request has the possiblity for a BrokenPipeError
    so I looped all requests until there is no error received."""

    # pylint: disable=too-many-instance-attributes
    # Eight is reasonable in this case.

    # pylint: disable=unnecessary-lambda
    # It is in fact necessary.

    # pylint: disable=attribute-defined-outside-init
    # This needs to be defined here to work properly
    def __init__(self, p_w: object):
        """ Initialize playwright and connect to cleverbot.com."""
        self.p_w: object = p_w
        self.url: str = "https://www.cleverbot.com"
        self.reply: str = "id=line1"
        self.hacking: bool = False
        self.bot_response: str = ""
        self.response_string: str = ""
        self.browser: object = self.p_w.firefox.launch()
        self.context: object = self.browser.new_context(
            user_agent=UserAgent().random)

    def get_form(self):
        """Open new browser context page."""
        while True:
            try:
                self.page: object = self.context.new_page()
                self.page.goto(self.url,
                               timeout=10000,
                               wait_until="networkidle")
            except (PwTimeout, BrokenPipeError):
                self.page.close()
                continue
            break

    def send_input(self, user_input: str):
        """ Submits your message through an input filter."""
        f_one: str = r"<\/?[a-z]+>|<DOCTYPE"
        f_two: str = r"/<[^>]+>/g"
        if re.search(f_one, user_input) is not None or re.search(
                f_two, user_input) is not None:
            self.hacking: bool = True
            user_input: str = "I will hack you"
        while True:
            try:
                self.page.evaluate(f'cleverbot.sendAI("{user_input}")')
                sleep(0.25)
            except BrokenPipeError:
                continue
            break

    def _parse_response(self, response: object):
        """Helper method to parse network responses for reply."""
        if "talking.txt" in response.url:
            cookies: str = response.request.headers["cookie"]
            cookie_list: list = cookies.split("; ")
            for cookie in cookie_list:
                if cookie.startswith("CBALT"):
                    self.bot_response: str = cookie[8:]

    def get_response(self) -> str:
        """The DOM is updated with every individual character
        received from the Cleverbot app. This captures network
        requests made after sending input, tries to make sure
        that the DOM element has received text then retrieves
        the reply."""
        if self.hacking is True:
            self.hacking: bool = False
            return "No hax bro."
        self.page.on("response",
                     lambda response: self._parse_response(response))
        line: str = self.page.text_content(self.reply)
        while len(line) <= 1 and line != self.bot_response:
            line: str = self.page.text_content(self.reply)
            sleep(0.1)
        self.page.close()
        return self.bot_response

    def single_exchange(self, user_input: str) -> str:
        """This fuction is used to create a single send a receive chat
        session via a headless Firefox browser, sending your input
        as an argument to the cleverbot.sendAI() function and
        retrieving it's reply."""
        self.get_form()
        self.send_input(user_input)
        reply: str = self.get_response()
        if reply == "":
            self.single_exchange(user_input)
        return reply

    def close(self):
        """Close the headless browser."""
        self.browser.close()

    @staticmethod
    def connect(func):
        """Decorator for connecting and starting a browser session."""
        @wraps(func)
        def inner(*args, **kwargs):
            """Initialize playwright."""
            with sync_playwright() as p_w:
                c_b = Cleverbot(p_w)
                return func(c_b, *args, **kwargs)

        return inner


class CleverbotAsync(AsyncObject):  # lgtm[py/missing-call-to-init]
    """ Constructs a Cleverbot chat session. Initializes the options
    to connect to Cleverbot.com via a headless Firefox browser using
    playwright, and contains the functions to connect and create chat
    sessions. Every request has the possiblity for a BrokenPipeError
    so I looped all requests until there is no error received."""

    # pylint: disable=super-init-not-called
    # This is a hack to make an async init.

    # pylint: disable=too-many-instance-attributes
    # Eight is reasonable in this case.

    # pylint: disable=unnecessary-lambda
    # It is in fact necessary.

    # pylint: disable=attribute-defined-outside-init
    # This needs to be defined here to work properly
    async def __init__(self, p_w: object):
        """ Initialize playwright and connect to cleverbot.com."""
        self.p_w: object = p_w
        self.url: str = "https://www.cleverbot.com"
        self.reply: str = "id=line1"
        self.hacking: bool = False
        self.bot_response: str = ""
        self.browser: object = await self.p_w.firefox.launch()
        self.context: object = await self.browser.new_context(
            user_agent=UserAgent().random)

    async def get_form(self):
        """Open new browser context page."""
        while True:
            try:
                self.page: object = await self.context.new_page()
                await self.page.goto(self.url,
                                     timeout=10000,
                                     wait_until="networkidle")
            except (PwTimeout, BrokenPipeError):
                await self.page.close()
                continue
            break

    async def send_input(self, user_input: str):
        """ Submits your message through an input filter."""
        f_one: str = r"<\/?[a-z]+>|<DOCTYPE"
        f_two: str = r"/<[^>]+>/g"
        if re.search(f_one, user_input) is not None or re.search(
                f_two, user_input) is not None:
            self.hacking: bool = True
            user_input: str = "I will hack you"
        while True:
            try:
                await self.page.evaluate(f'cleverbot.sendAI("{user_input}")')
                await asyncio.sleep(0.25)
            except BrokenPipeError:
                continue
            break

    def _parse_response(self, response: object):
        """Helper method to parse network responses for reply."""
        if "talking.txt" in response.url:
            cookies: str = response.request.headers["cookie"]
            cookie_list: list = cookies.split("; ")
            for cookie in cookie_list:
                if cookie.startswith("CBALT"):
                    self.bot_response: str = cookie[8:]

    async def get_response(self) -> str:
        """The DOM is updated with every individual character
        received from the Cleverbot app. This captures network
        requests made after sending input, tries to make sure
        that the DOM element has received text then retrieves
        the reply."""
        if self.hacking is True:
            self.hacking: bool = False
            return "No hax bro."
        self.page.on("response",
                     lambda response: self._parse_response(response))
        line: str = await self.page.text_content(self.reply)
        while len(line) <= 1 and line != self.bot_response:
            line: str = await self.page.text_content(self.reply)
            await asyncio.sleep(0.1)
        await self.page.close()
        return self.bot_response

    async def single_exchange(self, user_input: str) -> str:
        """This fuction is used to create a single send a receive chat
        session via a headless Firefox browser, sending your input
        as an argument to the cleverbot.sendAI() function and
        retrieving it's reply."""
        await self.get_form()
        await self.send_input(user_input)
        reply: str = await self.get_response()
        if reply == "":
            await self.single_exchange(user_input)
        return reply

    async def close(self):
        """Close the headless browser."""
        await self.browser.close()

    @staticmethod
    def connect(func):
        """Decorator for connecting and starting a browser session."""
        @wraps(func)
        async def inner(*args, **kwargs):
            """Initialize playwright"""
            async with async_playwright() as p_w:
                c_b = await CleverbotAsync(p_w)
                return await func(c_b, *args, **kwargs)

        return inner
