from os import system

# ANSI CODES FOR COLORS
COLORS = {
            "Black": "\u001b[30m",
            "Red": "\u001b[31m",
            "Green": "\u001b[32m",
            "Yellow": "\u001b[33m",
            "Blue": "\u001b[34m",
            "Magenta": "\u001b[35m",
            "Cyan": "\u001b[36m",
            "White": "\u001b[37m",
            "ENDC": "\u001b[0m"
          }


def cprint(text, color):
    # Colored Print
    color = COLORS[color]
    system('')  # enable VT100 Escape Sequence for WINDOWS 10 Ver. 1607
    print(color + text + COLORS["ENDC"])


def all_low_tup(tup):
    # Turns all string elements
    # of a tuple to lower case
    low_tup = ()
    for el in tup:
        # You can't update a tuple
        # But you can perform addition
        # and reassignment
        #   low_tup = low_tup + tuple(el.lower())
        # You can also unpack a tupple using * operator
        low_tup = (*low_tup, el.lower())
    return low_tup


def sinput(prompt, allowed):
    # Sinput = Strong Input
    # Allows the User to Only Input the Given Words
    # List of Allowed Words is A Tuple
    allowed = all_low_tup(allowed)
    resp = input(prompt).strip().lower()
    while resp not in allowed:
        resp = input(prompt)
    return resp

if __name__ == "__main__":
    pass
