[![Python 3.8](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/release/python-380/)
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

Example of a simple CLI script that creates a single use, one message chat session. <br />
```python
import cleverbotfree

def chat():
    with cleverbotfree.sync_playwright() as p_w:
        c_b = cleverbotfree.Cleverbot(p_w)
        user_input = input("User: ")
        response = c_b.single_exchange(user_input)
        print("Cleverbot:", response)
        c_b.browser.close()

chat()
```

Example of a simple CLI script that creates a persistent chat session untill closed. <br />
```python
import cleverbotfree


def chat():
    with cleverbotfree.sync_playwright() as p_w:
        c_b = cleverbotfree.Cleverbot(p_w)
        while True:
            user_input = input("User: ")
            if user_input == 'quit':
                break
            c_b.send_input(user_input)
            bot = c_b.get_response()
            print('Cleverbot:', bot)
        c_b.browser.close()

chat()
```
