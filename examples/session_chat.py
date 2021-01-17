'''
Example of a simple CLI script that creates a persistent
chat session untill closed.
'''

import cleverbotfree.cbfree
import sys

cb = cleverbotfree.cbfree.Cleverbot()


def main():
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


if __name__ == '__main__':
    main()
