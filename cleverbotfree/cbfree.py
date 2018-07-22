'''
This module is a free alternative to Cleverbot.com's subscription API.
It uses a headless Firefox browser to run Cleverbots JavaScript code
and send and retrive for data HTML elements.
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
from time import sleep

elem = 0           # initialize varibles for
botResponse = 0    # globalization


class Cleverbot:

    '''
    Constructs a Cleverbot chat session. Initializes the options
    to connect to Cleverbot.com via a headless Firefox browser using
    selenium, and contains the functions to connect and create chat
    sessions. Every request has the possiblity for a BrokenPipeError
    so I looped all requests until there is no error recieved.

    :param userInput: str being sent to Cleverbot chat app
    :param return: str response from Cleverbot chat app
    '''

    def __init__(self):

        # initialize selenium options/arguments
        self.opts = Options()
        self.opts.add_argument("--headless")
        self.browser = webdriver.Firefox(options=self.opts)
        self.url = 'https://cleverbot.com'

    
    def single_exchange(self, userInput):

        '''
        This fuction is used to create a single send a recieve chat
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
        while True:
            try:
                elem = self.browser.find_element_by_class_name('stimulus')
            except BrokenPipeError:
                continue
            break
        while True:
            try:
                elem.send_keys(userInput + Keys.RETURN)
            except BrokenPipeError:
                continue
            break
        while True:
            try:
                while True:

                    '''
                    The DOM is updated with every individual character
                    recieved from the Cleverbot app. This tries to make 
                    sure that the DOM element has recieved the full text
                    before continuing the function.
                    '''

                    line = self.browser.find_element_by_id('line1')
                    sleep(2)
                    newLine = self.browser.find_element_by_id('line1')
                    if line.text != newLine and newLine.text != ' ' and newLine.text != '':
                        line = self.browser.find_element_by_id('line1')
                        sleep(2)
                        break
            except BrokenPipeError:
                continue
            break
        botResponse = line.text
        sleep(2)
        self.browser.close()
        return botResponse
    

    def get_form(self):

        # find the form tag to enter your message
        global elem
        while True:
            try:
                elem = self.browser.find_element_by_class_name('stimulus')
            except BrokenPipeError:
                continue
            break


    def send_input(self, userInput):

        # submits your message
        while True:
            try:
                elem.send_keys(userInput + Keys.RETURN)
            except BrokenPipeError:
                continue
            break


    def get_response(self):

        # retrieves Cleverbots response message
        global botResponse
        while True:
            try:
                while True:

                    '''
                    The DOM is updated with every individual character
                    recieved from the Cleverbot app. This tries to make 
                    sure that the DOM element has recieve the full text
                    before continuing the function.
                    '''

                    line = self.browser.find_element_by_id('line1')
                    sleep(3)
                    newLine = self.browser.find_element_by_id('line1')
                    if line.text != newLine and newLine.text != ' ' and newLine.text != '':
                        line = self.browser.find_element_by_id('line1')
                        sleep(2)
                        break
            except BrokenPipeError:
                continue
            break
        botResponse = line.text
        return botResponse
