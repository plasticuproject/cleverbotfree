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
    except:
        cb.browser.close()
        sys.exit()
    while True:
        try:
            cb.get_form()
        except:
            sys.exit()
        userInput = input('User: ')
        if userInput == 'quit':
            break
        cb.send_input(userInput)
        bot = cb.get_response()
        print('Cleverbot: ', bot)
    cb.browser.close()

    
if __name__ == '__main__':
    main()
