def all_low_tup(tup):
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
