'''
This module is a free alternative to Cleverbot.com's subscription API.
It uses a headless Firefox browser to run Cleverbot's JavaScript code
and send and retreive to/from HTML elements.

Copyright (C) 2018  plasticuproject@pm.me

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
'''

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import re


class Cleverbot:
    '''
    Constructs a Cleverbot chat session. Initializes the options
    to connect to Cleverbot.com via a headless Firefox browser using
    selenium, and contains the functions to connect and create chat
    sessions. Every request has the possiblity for a BrokenPipeError
    so I looped all requests until there is no error received.
    '''

    def __init__(self):

        # initialize selenium options/arguments
        self.opts = Options()
        self.opts.add_argument("--headless")
        self.browser = webdriver.Firefox(options=self.opts)
        self.url = 'https://www.cleverbot.com'
        self.hacking = False
        self.count = -1

    def get_form(self):

        # find the form tag to enter your message
        try:
            self.browser.find_element_by_id('noteb').click()
        except:
            pass

        while True:
            try:
                self.elem = self.browser.find_element_by_class_name('stimulus')
            except BrokenPipeError:
                continue
            break

    def send_input(self, userInput):

        # submits your message
        fOne = '<\/?[a-z]+>|<DOCTYPE'
        fTwo = '/<[^>]+>/g'
        if re.search(fOne, userInput) != None or re.search(fTwo, userInput) != None:
            self.hacking = True
            userInput = 'I will hack you'
        while True:
            try:
                self.elem.send_keys(userInput + Keys.RETURN)
            except BrokenPipeError:
                continue
            break

    def get_response(self):

        '''
        The DOM is updated with every individual character
        received from the Cleverbot app. This tries to make 
        sure that the DOM element has receive the full text
        before continuing the function.
        '''

        # retrieves Cleverbots response message
        while self.hacking == False:
            try:
                while True:
                    try:
                        if "opacity: 0.1" in self.browser.find_element_by_xpath("//span[@id='snipTextIcon']").get_attribute(
                                "style"):
                            line = self.browser.find_element_by_id('line1')
                            break
                    except NoSuchElementException:
                        continue
                    except StaleElementReferenceException:
                        self.url = self.url + '/?' + str(int(self.count + 1))
                        continue
            except BrokenPipeError:
                continue
            break
        if self.hacking is True:
            self.botResponse = 'Silly rabbit, html is for skids.'
        elif self.hacking is False:
            self.botResponse = line.text
        self.hacking = False
        return self.botResponse

    def single_exchange(self, userInput):

        '''
        This fuction is used to create a single send a receive chat
        session via a headless Firefox browser, sending your input
        as an argument to the DOM Form to be passed to the JS
        cleverbot.sendAI() function and retrieving it's response
        from the DOM.

        '''

        while True:
            try:
                self.browser.get(self.url)
            except BrokenPipeError:
                continue
            break
        self.get_form()
        self.send_input(userInput)
        self.get_response()
        return self.botResponse
