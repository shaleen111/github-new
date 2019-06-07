def sinput(prompt, allowed):
    # Sinput = Strong Input
    # Allows the User to Only Input the Given Words
    # List of Allowed Words is A Tuple
    resp = input(prompt)
    while resp not in allowed:
        resp = input(prompt)
    return resp
