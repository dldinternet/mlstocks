from __future__ import print_function

import getpass
import sys


def get_input(*args, **kwargs):
    try:
        builtin = raw_input
    except NameError:
        builtin = input

    try:
        ret = builtin(*args, **kwargs)
    except SystemExit:
        raise
    return ret


def get_string(prompt, default=None):
    prompt = "{}{}: ".format(
        prompt,
        "" if default is None else " [{}]".format(default)
    )

    value = None

    while value is None or len(value) == 0:
        try:
            value = get_input(prompt) or default
        except KeyboardInterrupt:
            print("")
            sys.exit()
        except EOFError:
            print("")
            sys.exit()
        except SystemExit:
            raise
        except:
            pass

    return value


def get_password(prompt):
    while True:
        try:
            password = getpass.getpass("{}: ".format(prompt))
            if len(password) > 0:
                return password
        except KeyboardInterrupt:
            print("")
            sys.exit()
        except EOFError:
            print("")
            sys.exit()
        except SystemExit:
            raise
        except:
            pass


def get_yn(prompt, default=True):
    choice = None

    choices = "[yn]"

    if default is True:
        choices = choices.replace("y", "Y")
    elif default is False:
        choices = choices.replace("n", "N")

    prompt = "{} {}: ".format(
        prompt,
        choices
    )

    while choice is None:
        try:
            s = get_input(prompt)

            if len(s) == 0 and default is not None:
                return default

            if len(s) > 1:
                continue

            s = s.lower()

            if s == "y":
                return True

            if s == "n":
                return False

        except KeyboardInterrupt:
            print("")
            sys.exit()
        except EOFError:
            print("")
            sys.exit()
        except SystemExit:
            raise
        except:
            pass


def get_from_list(choices, title, prompt, default=0):
    choice = None

    prompt = "{}{}: ".format(
        prompt,
        "" if default is None else " [{}]".format(default)
    )

    if title is not None:
        print(title)

    for i, c in enumerate(choices):
        print("[{}] {}".format(i, c))

    while choice is None:
        try:
            s = get_input(prompt) or default

            i = int(s)

            if i >= 0 and i < len(choices):
                choice = choices[i]
        except KeyboardInterrupt:
            print("")
            sys.exit()
        except EOFError:
            print("")
            sys.exit()
        except SystemExit:
            raise
        except:
            pass

    return choice
