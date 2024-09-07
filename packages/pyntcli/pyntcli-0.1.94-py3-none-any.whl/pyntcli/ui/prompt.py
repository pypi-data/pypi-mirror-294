import signal
from pyntcli.ui import ui_thread


class TimeoutExpired(Exception):
    pass


def _timeout_handler(signum, frame):
    raise TimeoutExpired


def confirmation_prompt_with_timeout(question, default, timeout=10):
    """Prompt the user with a confirmation question (Yes/No) and return True for 'yes' or False for 'no'.

    Args:
        question (str): The question to present to the user.
        default (str): The default answer if the user just presses Enter. It should be 'yes' or 'no'.
        timeout (int): The timeout in seconds. If the user doesn't respond within the timeout, the default answer will be selected.

    Returns:
        bool: True if the answer is 'yes', False if the answer is 'no'.
    """
    valid = {"yes": True, "y": True, "no": False, "n": False}

    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError(f"Invalid default answer: '{default}'")

    signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(timeout)

    try:
        while True:
            choice = input(question + prompt).strip().lower()

            if choice == "" and default:  # Only 'Enter' with default will continue
                return valid[default]
            elif choice in valid:
                return valid[choice]
            else:
                ui_thread.print("Please respond with 'yes' or 'no' (or 'y' or 'n').")
    except TimeoutExpired:
        ui_thread.print(ui_thread.PrinterText(f"\nNo response within {timeout} seconds, defaulting to {'Yes' if default == 'yes' else 'No'}.\n" +
                        "You can use '--yes' flag for auto-confirm", ui_thread.PrinterText.WARNING))
        return valid[default]
    finally:
        signal.alarm(0)
