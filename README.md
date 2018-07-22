# cleverbotfree
Cleverbot.com used to have a free API for their chatbot application. They have <br />
removed their free API in place of a tiered subscription API service. <br />
cleverbotfree is a free alternative to that API that uses a headless Firefox <br />
browser to communicate with their chatbot application. You can use this module <br />
to create applications/bots that send a recieve messages to the Cleverbot <br />
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
requires geckodriver, which needs to be installed berfore this module can be <br />
used. Make sure it’s in your PATH, e. g., place it in /usr/bin or /usr/local/bin. <br />

You can download the geckodriver at https://github.com/mozilla/geckodriver/releases <br />

Failure to observe this step will give you the error <br />
"Message: ‘geckodriver’ executable needs to be in PATH." <br />


## Usage
<b>Examples</b>

Example of a simple CLI script that creates a single use, one message chat session. <br />
```python
from cleverbotfree.cbfree import Cleverbot
send = Cleverbot().single_exchange

def chat():
    userInput = input('User: ')
    response = send(userInput)
    print(response)
    Cleverbot().browser.close()

chat()
```

Example of a simple CLI script that creates a persistent chat session untill closed. <br />
```python
import cleverbotfree.cbfree
cb = cleverbotfree.cbfree.Cleverbot()

def chat():
    try:
        print('[-] Connecting to Cleverbot.com...\n')
        cb.browser.get(cb.url)
        print('[-] Type "quit" at any time to exit.\n')
        while True:
            cb.get_form()
            userInput = input('User: ')
            if userInput == 'quit':
                break
            cb.send_input(userInput)
            print('\nCleverbot: ' + cb.get_response() + '\n')
        cb.browser.close()
    except KeyboardInterrupt:
        print('\nThanks for chatting!\n')
        cb.browser.close()

chat()
```
