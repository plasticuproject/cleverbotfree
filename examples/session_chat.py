'''
Example of a simple CLI script that creates a persistent
chat session untill closed.
'''

import cleverbotfree


def main():
    """Example code."""
    with cleverbotfree.sync_playwright() as p_w:
        c_b = cleverbotfree.Cleverbot(p_w)
        while True:
            user_input = input("User: ")
            if user_input == 'quit':
                break
            c_b.send_input(user_input)
            bot = c_b.get_response()
            print('Cleverbot: ', bot)
        c_b.browser.close()


if __name__ == '__main__':
    main()
