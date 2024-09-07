"""
This module provides secure password input functionality for both Windows and Unix-like systems. 
It includes functions to prompt the user for a password and optionally mask the input.

Functions:
- win_termipass(prompt: str, mask: str) -> str: Prompts for a password in a Windows environment, with optional masking.
- unix_termipass(prompt: str, mask: str, stream=None) -> str: Prompts for a password in Unix-like environments, with optional masking.
- fallback_getpass(prompt='Password: ', stream=None) -> str: Fallback password prompt when no terminal control is available.
- _raw_input(prompt="", stream=None, input=None) -> str: Reads input from the user without saving it to the history.

The module automatically selects the appropriate password prompt function based on the operating system.
"""

import sys


def win_termipass(prompt: str = 'enter your password: ', mask: str = '*') -> str:
    """
    Prompts the user to enter a password in a Windows environment with support for masked input,
    arrow key navigation, and the delete key.

    Args:
        prompt (str): password prompt for the user.
        mask (str, optional): mask for the password.

    Returns:
        str: password entered by the user.
        
    Raises:
        TypeError: If `prompt` or `mask` is not a string.
        ValueError: If `mask` is more than one character.
        KeyboardInterrupt: If the user interrupts the input (Ctrl+C).
    """
    
    if not isinstance(prompt, str):
        raise TypeError(f'prompt argument must be a str, not{type(prompt).__name__}')
    if not isinstance(mask, str):
        raise TypeError(f'mask argument must be a zero- or one-character str, not {type(mask).__name__}')
    if len(mask) > 1:
        raise ValueError('mask argument must be a zero- or one-character str')
    if mask == '' or mask == None:
        from getpass import getpass
        return getpass(prompt)

    password = []
    cursor_pos = 0  # Keeps track of where the cursor is in the password
    sys.stdout.write(prompt)
    sys.stdout.flush()

    while True:
        c = msvcrt.getwch()

        if c == '\r' or c == '\n':  # Enter key
            sys.stdout.write('\n')
            sys.stdout.flush()
            return ''.join(password)
        if c == '\003':  # Ctrl+C to interrupt
            raise KeyboardInterrupt
        if c == '\b' or c == '\x08':  # Backspace key
            if cursor_pos > 0:
                cursor_pos -= 1
                password.pop(cursor_pos)
                # Move cursor back and clear the last character on the screen
                sys.stdout.write('\b \b')
                sys.stdout.write(''.join([mask] * len(password[cursor_pos:])))
                sys.stdout.write(' ')
                sys.stdout.write('\b' * (len(password) - cursor_pos + 1))
                sys.stdout.flush()
        elif c == '\x00' or c == '\xe0':  # Special key sequence (arrow keys, delete, etc.)
            special_key = msvcrt.getwch()

            if special_key == 'K':  # Left Arrow key
                if cursor_pos > 0:
                    cursor_pos -= 1
                    sys.stdout.write('\b')
                    sys.stdout.flush()

            elif special_key == 'M':  # Right Arrow key
                if cursor_pos < len(password):
                    sys.stdout.write(mask)
                    cursor_pos += 1
                    sys.stdout.flush()

            elif special_key == 'S':  # Delete key
                if cursor_pos < len(password):
                    password.pop(cursor_pos)
                    sys.stdout.write(''.join([mask] * len(password[cursor_pos:])))
                    sys.stdout.write(' ')
                    sys.stdout.write('\b' * (len(password) - cursor_pos + 1))
                    sys.stdout.flush()
        else:  # Normal character input
            password.insert(cursor_pos, c)
            cursor_pos += 1
            sys.stdout.write(mask + ''.join([mask] * (len(password) - cursor_pos)))
            sys.stdout.write('\b' * (len(password) - cursor_pos))
            sys.stdout.flush()

 
def unix_termipass(prompt: str = 'enter your password: ', mask: str = '*') -> str:
    """
    Prompts the user to enter a password in Unix-like environments with support for masked input,
    arrow key navigation, and the delete key.

    Args:
        prompt (str): password prompt for the user.
        mask (str, optional): mask for the password.

    Returns:
        str: password entered by the user.
        
    Raises:
        TypeError: If `prompt` or `mask` is not a string.
        ValueError: If `mask` is more than one character.
        KeyboardInterrupt: If the user interrupts the input (Ctrl+C).
    """
    
    if not isinstance(prompt, str):
        raise TypeError(f'prompt argument must be a str, not {type(prompt).__name__}')
    if not isinstance(mask, str):
        raise TypeError(f'mask argument must be a zero- or one-character str, not {type(mask).__name__}')
    if len(mask) > 1:
        raise ValueError('mask argument must be a zero- or one-character str')
    if mask == '' or mask == None:
        from getpass import getpass
        return getpass(prompt)
    
    def getchar():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    password = []
    cursor_pos = 0  # Keeps track of where the cursor is in the password
    sys.stdout.write(prompt)
    sys.stdout.flush()

    while True:
        c = getchar()

        if c == '\r' or c == '\n':  # Enter key
            sys.stdout.write('\n')
            sys.stdout.flush()
            return ''.join(password)
        if c == '\003':  # Ctrl+C to interrupt
            raise KeyboardInterrupt
        if c == '\x7f':  # Backspace key
            if cursor_pos > 0:
                cursor_pos -= 1
                password.pop(cursor_pos)
                # Move cursor back and clear the last character on the screen
                sys.stdout.write('\b \b')
                sys.stdout.write(''.join([mask] * len(password[cursor_pos:])))
                sys.stdout.write(' ')
                sys.stdout.write('\b' * (len(password) - cursor_pos + 1))
                sys.stdout.flush()
        elif c == '\x1b':  # Special key sequence (starts with ESC in Unix)
            next1, next2 = getchar(), getchar()
            if next1 == '[':
                if next2 == 'D':  # Left Arrow key
                    if cursor_pos > 0:
                        cursor_pos -= 1
                        sys.stdout.write('\b')
                        sys.stdout.flush()
                elif next2 == 'C':  # Right Arrow key
                    if cursor_pos < len(password):
                        sys.stdout.write(mask)
                        cursor_pos += 1
                        sys.stdout.flush()
                elif next2 == '3':  # Delete key (ESC [ 3 ~)
                    getchar()  # To consume the '~' character
                    if cursor_pos < len(password):
                        password.pop(cursor_pos)
                        sys.stdout.write(''.join([mask] * len(password[cursor_pos:])))
                        sys.stdout.write(' ')
                        sys.stdout.write('\b' * (len(password) - cursor_pos + 1))
                        sys.stdout.flush()
        else:  # Normal character input
            password.insert(cursor_pos, c)
            cursor_pos += 1
            sys.stdout.write(mask + ''.join([mask] * (len(password) - cursor_pos)))
            sys.stdout.write('\b' * (len(password) - cursor_pos))
            sys.stdout.flush()  
  
  
  
  
          
    
# Select the appropriate password prompt function based on the operating system
try:
    import termios, tty  # For Unix-like environments
except (ImportError, AttributeError):
    try:
        import msvcrt  # For Windows environments
    except ImportError:
        from getpass import getpass as fallback_getpass
        termipass = fallback_getpass
    else:
        termipass = win_termipass
else:
    termipass = unix_termipass
