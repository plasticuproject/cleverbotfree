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
from typing import List, Callable, Any
from functools import wraps
from playwright.sync_api import sync_playwright
from playwright.sync_api import TimeoutError as PwSyncTimeout
from playwright.async_api import async_playwright
from playwright.async_api import TimeoutError as PwAsyncTimeout
from fake_useragent import UserAgent


class AsyncObject:
    """Inheriting this class allows me to define an async
    __init__, So you can create an async Cleverbot object
    by doing `await CleverbotAsync(p_w)`"""

    async def __new__(cls, *a, **kw):  # type: ignore
        instance = super().__new__(cls)
        await instance.__init__(*a, **kw)  # type: ignore
        return instance

    async def __init__(self) -> None:  # type: ignore
        """Async init."""


class Cleverbot:
    """ Constructs a Cleverbot chat session. Initializes the options
    to connect to Cleverbot.com via a headless Firefox browser using
    playwright, and contains the functions to connect and create chat
    sessions. Every request has the possiblity for a BrokenPipeError
    so I looped all requests until there is no error received."""

    def __init__(self, p_w: Any) -> None:
        """ Initialize playwright and connect to cleverbot.com."""
        self.p_w = p_w
        self.url: str = "https://www.cleverbot.com"
        self.reply: str = "id=line1"
        self.hacking: bool = False
        self.bot_response: str = ""
        self.response_string: str = ""
        self.browser: Any = self.p_w.firefox.launch()
        self.context: Any = self.browser.new_context(user_agent=UserAgent(
            fallback="Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0)" +
            " Gecko/20100101 Firefox/96.0").random)

    def get_form(self) -> None:
        """Open new browser context page."""
        while True:
            try:
                self.page: Any = self.context.new_page()
                self.page.goto(self.url,
                               timeout=10000,
                               wait_until="networkidle")
            except (PwSyncTimeout, BrokenPipeError):
                self.page.close()
                continue
            break

    def send_input(self, user_input: str) -> None:
        """ Submits your message through an input filter."""
        f_one: str = r"<\/?[a-z]+>|<DOCTYPE"
        f_two: str = r"/<[^>]+>/g"
        if re.search(f_one, user_input) is not None or re.search(
                f_two, user_input) is not None:
            self.hacking = True
            user_input = "I will hack you"
        while True:
            try:
                self.page.evaluate(f'cleverbot.sendAI("{user_input}")')
                sleep(0.25)
            except BrokenPipeError:
                continue
            break

    def _parse_response(self, response: Any) -> None:
        """Helper method to parse network responses for reply."""
        if "talking.txt" in response.url:
            cookies: str = response.request.headers["cookie"]
            cookie_list: List[str] = cookies.split("; ")
            for cookie in cookie_list:
                if cookie.startswith("CBALT"):
                    self.bot_response = cookie[8:]

    def get_response(self) -> str:
        """The DOM is updated with every individual character
        received from the Cleverbot app. This captures network
        requests made after sending input, tries to make sure
        that the DOM element has received text then retrieves
        the reply."""
        if self.hacking is True:
            self.hacking = False
            return "No hax bro."
        self.page.on("response",
                     lambda response: self._parse_response(response))
        line: str = self.page.text_content(self.reply)
        while len(line) <= 1 and line != self.bot_response:
            line = self.page.text_content(self.reply)
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

    def close(self) -> None:
        """Close the headless browser."""
        self.browser.close()

    @staticmethod
    def connect(func: Callable[..., Any]) -> Callable[..., Any]:
        """Decorator for connecting and starting a browser session."""

        @wraps(func)
        def inner(*args: Any, **kwargs: Any) -> Any:
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

    async def __init__(self, p_w: Any):  # type: ignore
        """ Initialize playwright and connect to cleverbot.com."""
        self.p_w = p_w
        self.url: str = "https://www.cleverbot.com"
        self.reply: str = "id=line1"
        self.hacking: bool = False
        self.bot_response: str = ""
        self.browser: Any = await self.p_w.firefox.launch()
        self.context: Any = await self.browser.new_context(
            user_agent=UserAgent().random)

    async def get_form(self) -> None:
        """Open new browser context page."""
        while True:
            try:
                self.page: Any = await self.context.new_page()
                await self.page.goto(self.url,
                                     timeout=10000,
                                     wait_until="networkidle")
            except (PwAsyncTimeout, BrokenPipeError):
                await self.page.close()
                continue
            break

    async def send_input(self, user_input: str) -> None:
        """ Submits your message through an input filter."""
        f_one: str = r"<\/?[a-z]+>|<DOCTYPE"
        f_two: str = r"/<[^>]+>/g"
        if re.search(f_one, user_input) is not None or re.search(
                f_two, user_input) is not None:
            self.hacking = True
            user_input = "I will hack you"
        while True:
            try:
                await self.page.evaluate(f'cleverbot.sendAI("{user_input}")')
                await asyncio.sleep(0.25)
            except BrokenPipeError:
                continue
            break

    def _parse_response(self, response: Any) -> None:
        """Helper method to parse network responses for reply."""
        if "talking.txt" in response.url:
            cookies: str = response.request.headers["cookie"]
            cookie_list: List[str] = cookies.split("; ")
            for cookie in cookie_list:
                if cookie.startswith("CBALT"):
                    self.bot_response = cookie[8:]

    async def get_response(self) -> str:
        """The DOM is updated with every individual character
        received from the Cleverbot app. This captures network
        requests made after sending input, tries to make sure
        that the DOM element has received text then retrieves
        the reply."""
        if self.hacking is True:
            self.hacking = False
            return "No hax bro."
        self.page.on("response",
                     lambda response: self._parse_response(response))
        line: str = await self.page.text_content(self.reply)
        while len(line) <= 1 and line != self.bot_response:
            line = await self.page.text_content(self.reply)
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

    async def close(self) -> None:
        """Close the headless browser."""
        await self.browser.close()

    @staticmethod
    def connect(func: Callable[..., Any]) -> Callable[..., Any]:
        """Decorator for connecting and starting a browser session."""

        @wraps(func)
        async def inner(*args: Any, **kwargs: Any) -> Any:
            """Initialize playwright"""
            async with async_playwright() as p_w:
                c_b = await CleverbotAsync(p_w)  # type: ignore
                return await func(c_b, *args, **kwargs)

        return inner
