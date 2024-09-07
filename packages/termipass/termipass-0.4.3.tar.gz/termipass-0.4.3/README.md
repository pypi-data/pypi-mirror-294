# termipass

## Overview
`termipass` is a Python package that provides secure password input functionality for both Windows and Unix-like systems. It includes features such as masking the password input, supporting arrow key navigation, and handling the delete key during input.

This package automatically selects the appropriate method to prompt for a password based on the operating system (Windows or Unix-like).

## Features
- **Cross-platform support:** Works seamlessly on both Windows and Unix-like environments.
- **Optional masking:** Mask the password input with any character (e.g., `*` or `•`).
- **Arrow key navigation:** Move the cursor within the password input using left and right arrow keys.
- **Delete key handling:** Allows users to delete characters from the password input.

## Installation
You can install the package using `pip`:

```python
pip install termipass
```

## Quickstart Guide

Below is an example of how to use the `termipass` package to prompt the user for a password:

```python
from termipass.termipass import termipass

termipass()
Password: *************
'Thisisawesome'
termipass(prompt='YOUR PW HERE: ')
YOUR PW HERE: *************
'Thisisawesome'
termipass(mask='#')
Password: ###########
'Thisisawesome'
termipass(mask='') # Don't show anything calling getpass.getpass()
Password: 
'Thisisawesome'
```

## Author
Developed by [**Mahmoud Raouf**](https://www.linkedin.com/in/mahmoud-raouf21/). You can reach me at mahmoud.raouf21@gmail.com