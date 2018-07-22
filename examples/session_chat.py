'''
Example of a simple CLI script that creates a persistent
chat session untill closed.
'''

import cleverbotfree.cbfree

cb = cleverbotfree.cbfree.Cleverbot()


def main():

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


if __name__ == '__main__':
    main()
