[![Python 3.7](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html)
[![PyPI version](https://badge.fury.io/py/cleverbotfree.svg)](https://badge.fury.io/py/cleverbotfree)
[![Downloads](https://pepy.tech/badge/cleverbotfree)](https://pepy.tech/project/cleverbotfree)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/plasticuproject/cleverbotfree.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/plasticuproject/cleverbotfree/context:python)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=plasticuproject_cleverbotfree&metric=alert_status)](https://sonarcloud.io/dashboard?id=plasticuproject_cleverbotfree)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=plasticuproject_cleverbotfree&metric=security_rating)](https://sonarcloud.io/dashboard?id=plasticuproject_cleverbotfree)
# cleverbotfree
Cleverbot.com used to have a free API for their chatbot application. They have <br />
removed their free API in place of a tiered subscription API service. <br />
cleverbotfree is a free alternative to that API that uses a headless Firefox <br />
browser to communicate with their chatbot application. You can use this module <br />
to create applications/bots that send and receive messages to the Cleverbot <br />
chatbot application <br />


## Installation
<b>Requirments</b>

You need to have Python 3.x, pip, and the latest Firefox browser installed. <br />
Once installed, you can install this library through pip. <br />
```
pip install cleverbotfree
```

<b>Drivers</b>

Selenium requires a driver to interface with the headless browser. Firefox <br />
requires geckodriver, which needs to be installed before this module can be <br />
used. Make sure it’s in your PATH, e. g., place it in /usr/bin or /usr/local/bin. <br />

You can download the geckodriver at https://github.com/mozilla/geckodriver/releases <br />

Failure to observe this step will give you the error <br />
"Message: ‘geckodriver’ executable needs to be in PATH." <br />


## Usage
<b>Examples</b>

Example of a simple CLI script that creates a single use, one message chat session. <br />
```python
import cleverbotfree.cbfree
import sys
cb = cleverbotfree.cbfree.Cleverbot()

def chat():
    userInput = input('User: ')
    response = cb.single_exchange(userInput)
    print(response)
    cb.browser.close()
    sys.exit()

chat()
```

Example of a simple CLI script that creates a persistent chat session untill closed. <br />
```python
import cleverbotfree.cbfree
import sys
cb = cleverbotfree.cbfree.Cleverbot()

def chat():
    try:
        cb.browser.get(cb.url)
        while True:
            cb.get_form()
            userInput = input('User: ')
            if userInput == 'quit':
                break
            cb.send_input(userInput)
            bot = cb.get_response()
            print('Cleverbot: ', bot)
        cb.browser.close()
    except KeyboardInterrupt:
        cb.browser.close()
        sys.exit()

chat()
```
