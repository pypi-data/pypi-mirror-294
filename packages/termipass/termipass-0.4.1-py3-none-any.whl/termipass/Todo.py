import sys 
def unix_termipass(prompt: str = 'enter your password: ', mask: str = '*') -> str:
    """
    Prompts the user to enter a password in Unix-like environments.

    This function supports masked input, where the entered characters are replaced by a mask character (e.g., '*').
    If the mask is an empty string, the input will not be masked.

    Args:
        prompt (str): The password prompt to display to the user.
        mask (str, optional): The mask character to display instead of the actual password characters. Defaults to '*'.

    Returns:
        str: The password entered by the user.

    Raises:
        TypeError: If `prompt` or `mask` is not a string.
        ValueError: If `mask` is more than one character.
        KeyboardInterrupt: If the user interrupts the input (Ctrl+C).
    """
    if mask == '' or mask == None:
        from getpass import getpass
        return getpass(prompt)
    
    if not isinstance(prompt, str):
        raise TypeError(f'prompt argument must be a str, not{type(prompt).__name__}')
    if not isinstance(mask, str):
        raise TypeError(f'mask argument must be a zero- or one-character str, not {type(mask).__name__}')
    if len(mask) > 1:
        raise ValueError('mask argument must be a zero- or one-character str')
    
    def getchar():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    
    password = ''
    sys.stdout.write(prompt)
    sys.stdout.flush()
    while True:
        c = getchar()
        if c == '\r' or c == '\n':
            sys.stdout.write('\n')
            sys.stdout.flush()
            return password
        if c == '\003':
            raise KeyboardInterrupt
        if c == '\b' or c == '\x08' or c == '\x7f':
            password = password[:-1]
            sys.stdout.write('\b \b')
            sys.stdout.flush()
        else:
            password += c
            sys.stdout.write(mask)
            sys.stdout.flush()
  



def win_termipass(prompt: str = 'enter your password: ', mask: str = '*') -> str:
    """
    Prompts the user to enter a password in a Windows environment.

    This function supports masked input, where the entered characters are replaced by a mask character (e.g., '*'). 
    If the mask is an empty string, the input will not be masked.

    Args:
        prompt (str): password prompt for the user.
        mask (str, optional): mask for the password.

    Returns:
        str: password entered by the user (str)
        
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
    password = ''
    sys.stdout.write(prompt)
    sys.stdout.flush()
    
    while True:
        c = msvcrt.getwch()
        if c == '\r' or c == '\n':
            sys.stdout.write('\n')
            sys.stdout.flush()
            return password
        if c == '\003':
            raise KeyboardInterrupt
        
        
        if c == '\b' or c == '\x08':
            password = password[:-1]
            if len(password) == 0:
                continue
            sys.stdout.write('\b \b')
            sys.stdout.flush()
        if c =='\x00':
            pass #? ToDo: handle special keys (delete, arrow keys, etc.)
        else:
            password += c
            sys.stdout.write(mask)
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
    