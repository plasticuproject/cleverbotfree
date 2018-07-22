'''
Example of a simple CLI script that creates a single use,
one message chat session.
'''

from cleverbotfree.cbfree import Cleverbot

send = Cleverbot().single_exchange


def main():

    userInput = input('User: ')
    response = send(userInput)
    print(response)
    Cleverbot().browser.close()


if __name__ == '__main__':
    main()
