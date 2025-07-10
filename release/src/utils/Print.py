import os, sys

def print_status(tag: str, message: str):
    COLORS = {
        "INF": "\033[94m",
        "ERR": "\033[91m",
        "WRN": "\033[93m",
        "OK":  "\033[92m",
        "ASK": "\033[96m",
        "INI": "\033[95m",
        "RST": "\033[0m",
    }

    tag = tag.upper()[:3]
    color = COLORS.get(tag, "\033[90m")
    reset = COLORS["RST"]
    print(f"{color}[{tag:<3}]{reset} {message}")

def wait_key():
    print_status("ASK", "Press any key to continue...")
    try:
        if os.name == 'nt':
            import msvcrt
            msvcrt.getch()
        else:
            import termios
            import tty
            fd = sys.stdin.fileno()
            old = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old)
    except Exception:
        input()  # fallback
    print()
