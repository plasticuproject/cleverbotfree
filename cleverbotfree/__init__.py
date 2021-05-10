'''
This module is a free alternative to Cleverbot.com's subscription API.
It uses a headless Firefox browser to run Cleverbot's JavaScript code
and retrieve HTML elements.

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
from time import sleep
from playwright.sync_api import sync_playwright
from playwright._impl._api_types import TimeoutError as PwTimeout
from fake_useragent import UserAgent


class Cleverbot():
    """ Constructs a Cleverbot chat session. Initializes the options
    to connect to Cleverbot.com via a headless Firefox browser using
    playwright, and contains the functions to connect and create chat
    sessions. Every request has the possiblity for a BrokenPipeError
    so I looped all requests until there is no error received."""
    def __init__(self, p_w: object):
        """ Initialize playwright and connect to cleverbot.com."""
        self.p_w: object = p_w
        self.url: str = 'https://www.cleverbot.com'
        self.hacking: bool = False
        self.browser: object = self.p_w.firefox.launch()
        self.page: object = self.browser.new_page(
            user_agent=UserAgent().random)
        while True:
            try:
                self.page.goto(self.url,
                               timeout=10000,
                               wait_until="domcontentloaded")
                self.page.wait_for_selector('#noteb')
                self.page.click('#noteb')
                self.page.wait_for_selector('#conversationcontainer')
            except (PwTimeout, BrokenPipeError):
                continue
            break

    def send_input(self, user_input: str):
        """ Submits your message through an input filter."""
        f_one: str = r'<\/?[a-z]+>|<DOCTYPE'
        f_two: str = r'/<[^>]+>/g'
        if re.search(f_one, user_input) is not None or re.search(
                f_two, user_input) is not None:
            self.hacking: bool = True
            user_input: str = 'I will hack you'
        while True:
            try:
                self.page.evaluate(f'cleverbot.sendAI("{user_input}")')
            except BrokenPipeError:
                continue
            break

    def get_response(self) -> str:
        """The DOM is updated with every individual character
        received from the Cleverbot app. This tries to make
        sure that the DOM element has receive the full text
        before continuing the function."""
        while self.hacking is False:
            try:
                while True:
                    sleep(1)
                    line: str = self.page.text_content('id=line1')
                    sleep(3)
                    new_line: str = self.page.text_content('id=line1')
                    if line != new_line and new_line != '':
                        line: str = self.page.text_content('id=line1')
                        sleep(3)
                        break
            except BrokenPipeError:
                continue
            break
        if self.hacking is True:
            bot_response: str = 'Silly rabbit, html is for skids.'
        elif self.hacking is False:
            bot_response: str = line
        self.hacking: bool = False
        return bot_response

    def single_exchange(self, user_input: str) -> str:
        """This fuction is used to create a single send a receive chat
        session via a headless Firefox browser, sending your input
        as an argument to the cleverbot.sendAI() function and
        retrieving it's response from the DOM."""
        self.send_input(user_input)
        return self.get_response()
