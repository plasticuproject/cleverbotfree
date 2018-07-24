'''
Example of a simple CLI script that creates a single use,
one message chat session.
'''

import cleverbotfree.cbfree
import sys

cb = cleverbotfree.cbfree.Cleverbot()


def main():
    userInput = input('User: ')
    response = cb.single_exchange(userInput)
    print(response)
    cb.browser.close()
    sys.exit()
    
    
if __name__ == '__main__':
    main()
