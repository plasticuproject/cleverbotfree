'''
Example of a simple CLI script that creates a single use,
one message chat session.
'''

import cleverbotfree


def main():
    """Example code."""
    with cleverbotfree.sync_playwright() as p_w:
        c_b = cleverbotfree.Cleverbot(p_w)
        user_input = input("User: ")
        response = c_b.single_exchange(user_input)
        print("Cleverbot:", response)
        c_b.browser.close()


if __name__ == '__main__':
    main()
